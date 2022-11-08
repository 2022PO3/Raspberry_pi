# import the necessary packages
import re
import os
import requests
import subprocess

import cv2
import numpy
import numpy as np
from ocr.ocr import OCR, ResultLocation, OCRResult

from ocr import *

GARAGE_ID = 1


class LicensePlateResult:
    """
    This class contains the result of a license plate recognition detection algorithm. It stores the detected text and
    the location on the image. It also provides a function to find a given license plate format in the detected text.
    """

    def __init__(self, text: str, location: ResultLocation):
        self.text = text
        self.location = location

    def match_format(self, formats: list) -> list:
        """
        This function matches the detected text to the given regex patterns. It also creates new LicensePlateResult's
        based on the matching patterns.
        @param formats: list for regex patterns
        @return: list of LicensePlateResult's with matched strings
        """

        # Make list for new results
        matches = []
        # Go over each regex format and find all matching strings
        for f in formats:
            matches += re.findall(f, self.text)

        return [LicensePlateResult(text, self.location) for text in matches]


class ANPR:
    """
    This class can perform Automatic Number Plate Recognition (ANPR) on given images.
    """

    def __init__(self, selection_ocr: OCR, result_ocr: OCR, formats: list[str] = None, minAR=3,
                 maxAR=7, verbosity: int = 4, ):
        # Store the minimum and maximum rectangular aspect ratio
        self.minAR = minAR
        self.maxAR = maxAR

        # Variable to store how much debug output the class should give
        #        Levels of verbosity:
        #   * -1: nothing
        #   *  0: prints detected license plates
        #   *  1: show result image
        #   *  2: show all detected license plate candidates
        #   *  3: show result of black/white transformation to find license plate shapes
        #   *  4: show all steps

        self.verbosity = verbosity

        # Text recognition classes to use for selecting license plates out of multiple candidates and for giving the
        # final result
        self.selection_ocr = selection_ocr
        self.result_ocr = result_ocr

        # Transform custom format to regex ex. 'N-LLL-NNN' -> '[0-9]-[A-Z][A-Z][A-Z]-[0-9][0-9][0-9]'
        if formats is not None:
            formats = [f.replace("N", "[0-9]") for f in formats]
            formats = [f.replace("L", "[A-Z]") for f in formats]
            self.debug_print(formats, verbosity=0)
        self.formats = formats

    def debug_imshow(self, title, image, verbosity: int, waitKey=False):
        """
        Method to show debug or result images.


        @param title: Title of image window
        @param image: Image to show
        @param verbosity: level of verbosity required to show the image
        @param waitKey: boolean indicating whether the program should sleep until the user presses a key.
        """

        # Check if the verbosity of the image is below the verbosity specified by the user. A low verbosity means the
        # image is more important
        if verbosity <= self.verbosity:
            cv2.imshow(title, image)
            # Check to see if we should wait for a keypress
            if waitKey:
                cv2.waitKey(0)

    def debug_print(self, text, verbosity) -> None:
        """
        Method print debug or result text
        @param text: Text to be printed
        @param verbosity: level of verbosity required to show the image
        """
        if verbosity <= self.verbosity:
            print(text)

    def locate_license_plate_candidates(self, gray, keep=15) -> list[numpy.array]:
        # perform a blackhat morphological operation that will allow
        # us to reveal dark regions (i.e., text) on light backgrounds
        # (i.e., the license plate itself)
        rectKern = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 5))
        blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rectKern)
        self.debug_imshow("Blackhat", blackhat, 4)

        # next, find regions in the image that are light
        squareKern = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        light = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, squareKern)
        light = cv2.threshold(light, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        self.debug_imshow("Light Regions", light, 4)

        # compute the Scharr gradient representation of the blackhat
        # image in the x-direction and then scale the result back to
        # the range [0, 255]
        gradX = cv2.Sobel(blackhat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
        gradX = np.absolute(gradX)
        (minVal, maxVal) = (np.min(gradX), np.max(gradX))
        gradX = 255 * ((gradX - minVal) / (maxVal - minVal))
        gradX = gradX.astype("uint8")
        self.debug_imshow("Scharr", gradX, 4)

        # blur the gradient representation, applying a closing
        # operation, and threshold the image using Otsu's method
        gradX = cv2.GaussianBlur(gradX, (5, 5), 0)
        gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKern)
        thresh = cv2.threshold(gradX, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        self.debug_imshow("Grad Thresh", thresh, 4)

        # take the bitwise AND between the threshold result and the
        # light regions of the image
        thresh = cv2.bitwise_and(thresh, thresh, mask=light)
        thresh = cv2.dilate(thresh, None, iterations=2)
        thresh = cv2.erode(thresh, None, iterations=1)
        self.debug_imshow("Final", thresh, 3, waitKey=True)

        # find contours in the thresholded image and sort them by
        # their size in descending order, keeping only the largest
        # ones
        cnts = cv2.findContours(
            thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        cnts = cnts[0]
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:keep]
        # return the list of contours
        return cnts

    def pick_license_plate_location(self, gray, candidates):
        """
        Pick the best estimation of the position of the license plate. Based on shape, contrast and presence of text.
        """

        # initialize the license plate contour and ROI
        lp_location = None
        roi = None
        # Variable to remember length of the longest string in license plate candidates
        longest_text_length = 0

        # loop over the license plate candidate contours
        self.debug_print(f"Picking out of {len(candidates)} candidates.", 2)
        for c in candidates:
            # compute the bounding box of the contour and then use
            # the bounding box to derive the aspect ratio
            (x, y, w, h) = cv2.boundingRect(c)
            location = ResultLocation((x, y), w, h)
            ar = w / float(h)

            # check to see if the aspect ratio is rectangular
            if self.minAR <= ar <= self.maxAR:
                # store the license plate contour and extract the
                # license plate from the grayscale image and then
                # threshold it
                licensePlate = gray[y : y + h, x : x + w]
                roi_temp = cv2.threshold(
                    licensePlate, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
                )[1]

                # Select the license plate with the longest text on it
                ocr_results = self.selection_ocr.getTextFromImage(roi_temp)  # Read text
                self.debug_print(
                    f"Found Text on Candidate: {[r.text for r in ocr_results]}", 3
                )
                if len(ocr_results) > 0:
                    self.debug_imshow("License Plate Candidate", licensePlate, 3)
                    self.debug_imshow(
                        "ROI",
                        roi_temp,
                        3,
                        waitKey=True,
                    )
                    text_length = sum(len(r.text) for r in ocr_results)
                    if text_length is None or longest_text_length < text_length:
                        longest_text_length = text_length
                        lp_location = location
                        roi = roi_temp

        # return a 2-tuple of the license plate ROI and the contour
        # associated with it
        if roi is not None:
            cv2.imshow("ROI", roi)
        return roi, lp_location

    def find_and_ocr(self, image, doSelection=True):
        # convert the input image to grayscale, locate all candidate
        # license plate regions in the image, and then process the
        # candidates, leaving us with the *actual* license plate
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        location = None
        if doSelection:
            candidates = self.locate_license_plate_candidates(gray)
            (lp_image, location) = self.pick_license_plate_location(gray, candidates)
        else:
            lp_image = gray

        # only OCR the license plate if the license plate ROI is not
        # empty
        if lp_image is not None:
            # OCR the license plate
            ocr_results = self.result_ocr.getTextFromImage(lp_image)

            lp_results = [
                LicensePlateResult(result.text, result.location)
                for result in ocr_results
            ]

            if self.formats is not None:
                formatted_results = []
                for result in lp_results:
                    new_results = result.match_format(self.formats)
                    formatted_results += new_results
                lp_results = formatted_results

            if location is not None:
                for r in lp_results:
                    r.location.moveByLocation(location)

            if self.verbosity >= 1:
                for index, result in enumerate(lp_results):
                    show_text_on_image(
                        image,
                        result.text,
                        result.location,
                        waitKey=index == len(lp_results) - 1,
                    )

            self.debug_imshow("License Plate", lp_image, 2, waitKey=True)

            self.debug_print([lp.text for lp in lp_results], 0)

            return lp_results


def cleanup_text(text):
    # strip out non-ASCII text so we can draw the text on the image
    # using OpenCV
    return "".join([c if ord(c) < 128 else "" for c in text]).strip()


def show_text_on_image(image, text, location: ResultLocation, waitKey=True):
    image = image.copy()
    if text is not None and location is not None:
        # fit a rotated bounding box to the license plate contour and
        # draw the bounding box on the license plate
        cv2.rectangle(image, location.topLeft, location.bottomRigth, (0, 255, 0), 2)

        # compute a normal (unrotated) bounding box for the license
        # plate and then draw the OCR'd license plate text on the
        # image
        cv2.putText(
            image,
            cleanup_text(text),
            (location.topLeft[0], location.topLeft[1] - 15),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (0, 255, 0),
            2,
        )
        # show the output ANPR image
        cv2.imshow(text, image)
        if waitKey:
            cv2.waitKey(0)


def detectLicensePlate(imagePath, anpr):
    # load the input image from disk and resize it
    image = cv2.imread(imagePath)
    # image = imutils.resize(image, width=600)
    # apply automatic license plate recognition
    lp_results = anpr.find_and_ocr(image, doSelection=True)


def takePhoto(path: str):
    subprocess.run(
        ["libcamera-still", "-n", "--vflip=1", "--hflip=1", "--verbose=0", "-o", path]
    )


def send_backend_request(
    licence_plate: str, url: str = "http://192.168.49.1:8000/api/licence-plates/"
) -> None:
    """
    Sends the detected licence plate with a POST-request to the backend. The header is
    needed for the backend to verify that the request came from the Raspberry Pi.
    """

    headers = {"PO3-HEADER": os.environ["RASPBERRY_PI_KEY"]}
    body = {"licencePlate": licence_plate, "garageId": GARAGE_ID}
    requests.post(url, json=body, headers=headers)


if __name__ == "__main__":
    from src.anpr.ocr.google_vision_ocr import GoogleVisionOCR
    from src.anpr.ocr.easy_ocr import EasyOCR
    # initialize our ANPR class
    anpr = ANPR(EasyOCR(), GoogleVisionOCR(), formats=["N-LLL-NNN"], verbosity=4)
    print("taking photo")
    path = "img.png"
    takePhoto(path)
    # Initialize our ANPR class.
    anpr = ANPR(EasyOCR(), GoogleVisionOCR(), formats=["N-LLL-NNN"], verbosity=4)
    licence_plate = detectLicensePlate(path, anpr)
    send_backend_request(licence_plate)
