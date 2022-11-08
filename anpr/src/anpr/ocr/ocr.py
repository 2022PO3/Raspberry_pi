

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





if __name__ == '__main__':
    import cv2
    from google_vision_ocr import GoogleVisionOCR
    ocr = GoogleVisionOCR()

    image = cv2.imread(
        'src/anpr/google_vision_image.png')

    print(ocr.getTextFromImage(image))
