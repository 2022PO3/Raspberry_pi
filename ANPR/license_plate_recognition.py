# import the necessary packages
from skimage.segmentation import clear_border
import numpy as np
import imutils
import cv2
import os
from easyocr import Reader
from google.cloud import vision
import io
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'parkeergarage-c76e9940c139.json'


class PyImageSearchANPR:

    def __init__(self, minAR=3, maxAR=7, psm=11, debug=False):
        # store the minimum and maximum rectangular aspect ratio
        # values along with whether or not we are in debug mode
        self.minAR = minAR
        self.maxAR = maxAR
        self.debug = debug

        # A string with all the possible characters in a license plate
        self.alphanumeric = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-"

        # Reader object for OCR
        self.reader = Reader(['en'], gpu=True, download_enabled=False,
                             model_storage_directory='/Users/runeverachtert/Documents/Universiteit/P&O/3/Backend/utils/ANPR/models')

    def debug_imshow(self, title, image, waitKey=False):
        # check to see if we are in debug mode, and if so, show the
        # image with the supplied title
        if self.debug:
            cv2.imshow(title, image)
            # check to see if we should wait for a keypress
            if waitKey:
                cv2.waitKey(0)

    def locate_license_plate_candidates(self, gray, keep=15):
        # perform a blackhat morphological operation that will allow
        # us to reveal dark regions (i.e., text) on light backgrounds
        # (i.e., the license plate itself)
        rectKern = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 5))
        blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rectKern)
        # self.debug_imshow("Blackhat", blackhat)

        # next, find regions in the image that are light
        squareKern = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        light = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, squareKern)
        light = cv2.threshold(light, 0, 255,
                              cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        # self.debug_imshow("Light Regions", light)

        # compute the Scharr gradient representation of the blackhat
        # image in the x-direction and then scale the result back to
        # the range [0, 255]
        gradX = cv2.Sobel(blackhat, ddepth=cv2.CV_32F,
                          dx=1, dy=0, ksize=-1)
        gradX = np.absolute(gradX)
        (minVal, maxVal) = (np.min(gradX), np.max(gradX))
        gradX = 255 * ((gradX - minVal) / (maxVal - minVal))
        gradX = gradX.astype("uint8")
        # self.debug_imshow("Scharr", gradX)

        # blur the gradient representation, applying a closing
        # operation, and threshold the image using Otsu's method
        gradX = cv2.GaussianBlur(gradX, (5, 5), 0)
        gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKern)
        thresh = cv2.threshold(gradX, 0, 255,
                               cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        # self.debug_imshow("Grad Thresh", thresh)

        # take the bitwise AND between the threshold result and the
        # light regions of the image
        thresh = cv2.bitwise_and(thresh, thresh, mask=light)
        thresh = cv2.dilate(thresh, None, iterations=2)
        thresh = cv2.erode(thresh, None, iterations=1)
        self.debug_imshow("Final", thresh, waitKey=True)

        # find contours in the thresholded image and sort them by
        # their size in descending order, keeping only the largest
        # ones
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:keep]
        # return the list of contours
        return cnts

    def pick_license_plate(self, gray, candidates,
                           clearBorder=False):
        """
        Pick the best estimation of the position of the license plate. Based on shape, contrast and presence of text.
        """

        # initialize the license plate contour and ROI
        lpCnt = None
        roi = None
        # Variable to remember length of the longest string in license plate candidates
        longest_text_length = 0

        # loop over the license plate candidate contours
        for c in candidates:
            # compute the bounding box of the contour and then use
            # the bounding box to derive the aspect ratio
            (x, y, w, h) = cv2.boundingRect(c)
            ar = w / float(h)

            # check to see if the aspect ratio is rectangular
            if self.minAR <= ar <= self.maxAR:
                # store the license plate contour and extract the
                # license plate from the grayscale image and then
                # threshold it
                licensePlate = gray[y:y + h, x:x + w]
                roi_temp = cv2.threshold(licensePlate, 0, 255,
                                         cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

                # check to see if we should clear any foreground
                # pixels touching the border of the image
                # (which typically, not but always, indicates noise)
                if clearBorder:
                    roi_temp = clear_border(roi_temp)

                # Select the license plate with the longest text on it
                lp_text_list = self.ocr(roi_temp) # Read text
                if len(lp_text_list) > 0:
                    self.debug_imshow("License Plate", licensePlate)
                    self.debug_imshow("ROI", roi_temp, waitKey=True)
                    text_length = sum(len(s) for s in lp_text_list)
                    if text_length is None or longest_text_length < text_length:
                        longest_text_length = text_length
                        lpCnt = c
                        roi = roi_temp

        # return a 2-tuple of the license plate ROI and the contour
        # associated with it
        if roi is not None:
            cv2.imshow("ROI", roi)
        return (roi, lpCnt)

    def _ocr_google(self, image):
        path = 'frame.png'
        cv2.imwrite(path, image)

        client = vision.ImageAnnotatorClient()

        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        response = client.text_detection(image=image)
        texts = response.text_annotations
        print('Texts:')

        """for text in texts:
            print('\n"{}"'.format(text.description))

            vertices = (['({},{})'.format(vertex.x, vertex.y)
                         for vertex in text.bounding_poly.vertices])

            print('bounds: {}'.format(','.join(vertices)))"""

        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))
        return [text.description for text in texts]

    def _ocr_easyocr(self, image):
        results = self.reader.readtext(image,
                                       decoder='greedy',
                                       allowlist=self.alphanumeric,
                                       paragraph=False)

        if len(results) > 0:

            print([result[1] for result in results])

            return [result[1] for result in results]

            results = sorted(results, key=lambda result: result[1])
            return results[0][1]
        else:
            return ""

    def ocr(self, image, useVisionAPI=False):
        """
        Perform text recognition on the given image. Can be done using EasyOCR (free) or Google Vision API
        :param image:
        :param useVisionAPI: boolean indicating if the funtion should use EasyOCR or Google Vision API
        :return: text on image
        """

        if useVisionAPI:
            return self._ocr_google(image)
        else:
           return self._ocr_easyocr(image)

    def find_and_ocr(self, image, clearBorder=False):
        # initialize the license plate text
        lp_text_list = None
        # convert the input image to grayscale, locate all candidate
        # license plate regions in the image, and then process the
        # candidates, leaving us with the *actual* license plate
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        candidates = self.locate_license_plate_candidates(gray)
        (lp, lpCnt) = self.pick_license_plate(gray, candidates,
                                              clearBorder=clearBorder)
        # only OCR the license plate if the license plate ROI is not
        # empty
        if lp is not None:
            # OCR the license plate
            lp_text_list = self.ocr(lp, useVisionAPI=True)
            self.debug_imshow("License Plate", lp)
        # return a 2-tuple of the OCR'd license plate text along with
        # the contour associated with the license plate region
        return lp_text_list, lpCnt


    def show_result(self, image, lp_text_list, lpCnt, waitKey=True):
        if lp_text_list is not None and len(lp_text_list) > 0 and lpCnt is not None:
            # fit a rotated bounding box to the license plate contour and
            # draw the bounding box on the license plate
            box = cv2.boxPoints(cv2.minAreaRect(lpCnt))
            box = box.astype("int")
            cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
            # compute a normal (unrotated) bounding box for the license
            # plate and then draw the OCR'd license plate text on the
            # image
            (x, y, w, h) = cv2.boundingRect(lpCnt)
            cv2.putText(image, cleanup_text(str(lp_text_list)), (x, y - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
            # show the output ANPR image
            print("[INFO] {}".format(lp_text_list))
            cv2.imshow("Output ANPR", image)
            if waitKey:
                cv2.waitKey(0)


def cleanup_text(text):
    # strip out non-ASCII text so we can draw the text on the image
    # using OpenCV
    return "".join([c if ord(c) < 128 else "" for c in text]).strip()


def detectLicensePlate(imagePath, anpr):
    # load the input image from disk and resize it
    image = cv2.imread(imagePath)
    image = imutils.resize(image, width=600)
    # apply automatic license plate recognition
    (lp_text_list, lpCnt) = anpr.find_and_ocr(image, clearBorder=True)
    anpr.show_result(image, lp_text_list, lpCnt)


if __name__ == "__main__":
    # initialize our ANPR class
    anpr = PyImageSearchANPR(debug=False)

    # imagePath = input("path to license plate image:")
    path = '/Users/runeverachtert/Documents/Universiteit/P&O/3/Backend/utils/ANPR/afbeeldingen/'
    directory = os.fsencode(path)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".png"):
            print(f"Detecting license plate in {filename}")
            detectLicensePlate(path + filename, anpr)
