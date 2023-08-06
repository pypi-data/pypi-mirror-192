import numpy as np
import pytesseract
from PIL import Image
import cv2


def extract_text(image, top_left=None, bottom_right=None):
    """
    Function to extract text from an image

    Parameters:
        image (PIL.Image.Image or numpy.ndarray): Image.
        top_left (tuple, optional): Tuple of left top coordinates of the bounding box.
        bottom_right (tuple, optional): Tuple of right bottom coordinates of the bounding box.

    Returns:
        str: Extracted text.
    """
    if isinstance(image, Image.Image):
        image = np.array(image)
    if top_left is not None and bottom_right is not None:
        x1, y1 = top_left
        x2, y2 = bottom_right
        roi = image[y1:y2, x1:x2]
    else:
        roi = image
    text = pytesseract.image_to_string(roi)
    return text


def extract_text_from_small_image(image):
    if isinstance(image, Image.Image):
        image = np.array(image)
    roi = image
    roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, roi_thresh = cv2.threshold(roi_gray, 200, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    roi_dilate = cv2.dilate(roi_thresh, kernel, iterations=1)
    roi_erode = cv2.erode(roi_dilate, kernel, iterations=1)
    config = r'--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789of'
    text = pytesseract.image_to_string(roi_erode, lang='eng', config=config)
    return text


