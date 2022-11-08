from ocr import OCR, OCRResult, ResultLocation
from easyocr import Reader


def createOCRResult(result) -> OCRResult:
    text = result[1]
    location = ResultLocation.fromTopLeftBottomRight(topLeft=result[0][0], bottomRight=result[0][2])
    confidence = result[2]
    return OCRResult(text, location, confidence)


class EasyOCR(OCR):

    def __init__(self, model_storage_directory: str = 'src/anpr/models'):
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

        return [createOCRResult(result) for result in results]

