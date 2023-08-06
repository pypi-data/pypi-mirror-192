import base64

from selenium.webdriver.remote.webelement import WebElement

from selenite.helpers.ocr_wrapper import recognize_text_in_image


class ElementJ(WebElement):
    """
    A subclass of WebElement with an additional method for recognizing text in element screenshots.
    """

    def __init__(self, parent, id_):
        super().__init__(parent, id_)

    def text_recognition(self) -> str:
        """
        Recognizes text in an element screenshot.

        :return: The recognized text in the screenshot.
        """
        image_bytes = base64.b64decode(self.screenshot_as_base64)
        return recognize_text_in_image(image_bytes)

