from io import BytesIO

import ddddocr
from PIL import Image


def get_img_text(img_bytes: bytes) -> str:
    """
    识别图片中的文本。

    :param img_bytes: 图片的二进制数据。
    :return: 图片中识别出的文本。
    """
    img = Image.open(BytesIO(img_bytes))
    ocr = ddddocr.DdddOcr(show_ad=False)
    return ocr.classification(img)
