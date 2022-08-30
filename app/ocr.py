import cv2
import numpy as np
import pytesseract
from PIL import Image

from .utils import get_image_from_url


class OCR:
    def __init__(self, image_url: str) -> None:
        self.image_url = image_url

    def clear_image_before_ocr(self, img_arr):
        norm_img = np.zeros((img_arr.shape[0], img_arr.shape[1]))
        img_arr = cv2.normalize(img_arr, norm_img, 0, 255, cv2.NORM_MINMAX)
        img_arr = cv2.threshold(img_arr, 100, 255, cv2.THRESH_BINARY)[1]
        img_arr = cv2.GaussianBlur(img_arr, (1, 1), 0)
        return img_arr

    def get_ocr_result(self, img):
        result = pytesseract.image_to_string(image=img)
        return result

    def get_fields_wise_result(self, text: str):
        result = (
            text.strip("").split("Permanent Account Number Card")[1][:10].strip("\n")
        )
        return result

    def get_data_form_image(self):
        try:
            img11: Image = get_image_from_url(url=self.image_url)
            np_img_arr = np.array(img11)
            clear_img = self.clear_image_before_ocr(img_arr=np_img_arr)
            text = self.get_ocr_result(clear_img)
            result = self.get_fields_wise_result(text)
            return result
        except Exception as e:
            raise e
