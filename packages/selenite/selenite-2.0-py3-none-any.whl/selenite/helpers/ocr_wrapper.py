from io import BytesIO

import ddddocr
from PIL import Image


def recognize_text_in_image(image_bytes: bytes) -> str:
    """
    Recognizes text in an image.

    :param image_bytes: The binary data of the image.
    :return: The recognized text in the image.
    """
    with Image.open(BytesIO(image_bytes)) as img:
        ocr = ddddocr.DdddOcr(show_ad=False)
        return ocr.classification(img)
