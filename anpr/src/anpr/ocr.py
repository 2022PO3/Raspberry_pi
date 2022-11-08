import cv2
from easyocr import Reader
from google.cloud import vision
import io
import os


class ResultLocation:

    @classmethod
    def fromTopLeftBottomRight(cls, topLeft, bottomRight):
        return cls(topLeft=topLeft, width=bottomRight[0] - topLeft[0], height=bottomRight[1] - topLeft[1])

    def __init__(self, topLeft, width, height):
        self.topLeft = topLeft
        self.width = width
        self.height = height

    @property
    def topRight(self):
        return self.topLeft[0] + self.width, self.topLeft[1]

    @property
    def bottomLeft(self):
        return self.topLeft[0], self.topLeft[1] + self.height

    @property
    def bottomRigth(self):
        return self.topLeft[0] + self.width, self.topLeft[1] + self.height

    def getCorners(self):
        return [self.topLeft, self.topRight, self.bottomRigth, self.bottomLeft]

    def moveBy(self, x, y):
        self.topLeft = (self.topLeft[0] + x, self.topLeft[1] + y)

    def moveByLocation(self, location):
        self.topLeft = (self.topLeft[0] + location.topLeft[0], self.topLeft[1] + location.topLeft[1])


class OCRResult:

    def __init__(self, text: str, location: ResultLocation, confidence: float):
        self.text = text
        self.location = location
        self.confidence = confidence


class OCR:

    def getTextFromImage(self, image) -> list[OCRResult]:
        pass


class EasyOCR(OCR):

    def __init__(self, model_storage_directory: str = '../../src/anpr/models'):
        # A string with all the possible characters in a license plate
        self.alphanumeric = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-"

        # Reader object for OCR
        self.reader = Reader(['en'], gpu=True, download_enabled=False,
                             model_storage_directory=model_storage_directory)

    def getTextFromImage(self, image) -> list[OCRResult]:
        results = self.reader.readtext(image,
                                       decoder='greedy',
                                       allowlist=self.alphanumeric,
                                       paragraph=False)

        return [self.createOCRResult(result) for result in results]

    def createOCRResult(self, result) -> OCRResult:
        text = result[1]
        location = ResultLocation.fromTopLeftBottomRight(topLeft=result[0][0], bottomRight=result[0][2])
        confidence = result[2]
        return OCRResult(text, location, confidence)


class GoogleVisionOCR(OCR):

    def __init__(self, default_image_path='src/anpr/google_vision_image.png', default_confidence=1):

        self.default_confidence = default_confidence  # Google Vision API doesn't return a confidence level but is really accurate

        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'src/anpr/parkeergarage-c76e9940c139.json'

        self.default_image_path = default_image_path
        self.client = vision.ImageAnnotatorClient()

    def getTextFromImagePath(self, path):

        if path is None:
            path = self.default_image_path

        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        response = self.client.text_detection(image=image)

        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))

        return [self.createOCRResult(text_annotation) for text_annotation in response.text_annotations]

    def getTextFromImage(self, image) -> list[OCRResult]:
        cv2.imwrite(self.default_image_path, image)

        return self.getTextFromImagePath(self.default_image_path)

    def createOCRResult(self, text_annotation):
        text = text_annotation.description
        vertices = text_annotation.bounding_poly.vertices
        topLeft = (vertices[0].x, vertices[0].y)
        bottomRight = (vertices[2].x, vertices[2].y)
        location = ResultLocation.fromTopLeftBottomRight(topLeft=topLeft, bottomRight=bottomRight)
        confidence = self.default_confidence  # Google Vision API doesn't return a confidence level but is really accurate
        return OCRResult(text, location, confidence)


if __name__ == '__main__':
    ocr = GoogleVisionOCR()

    image = cv2.imread(
        'src/anpr/google_vision_image.png')

    print(ocr.getTextFromImage(image))
