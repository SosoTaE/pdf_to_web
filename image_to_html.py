import os.path
import shutil
import tempfile
import pytesseract
from PIL import Image
from pdf_to_image import read_page_and_save_as_image
from config import tesseract_cmd
from logger import logger

pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

def image_to_data(image):
    if isinstance(image, str):
        image = Image.open(image)

    if not isinstance(image, Image.Image):
        raise TypeError("image should be string or Image class")

    return pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

def generate_html_page_from_image(image, default_height=0, line=False):
    if isinstance(image, str):
        image = Image.open(image)

    if not isinstance(image, Image.Image):
        logger.error("Invalid image type. Expected PIL Image.Image.")
        raise TypeError("image should be string or Image class")

    ocr_result = image_to_data(image)
    body_content = ''

    n_boxes = len(ocr_result['text'])
    for i in range(n_boxes):
        if int(ocr_result['conf'][i]) > 60:  # confidence threshold
            (x, y, w, h) = (
                ocr_result['left'][i], ocr_result['top'][i], ocr_result['width'][i], ocr_result['height'][i])
            word = ocr_result['text'][i]
            font_size = h  # Use height as an approximation of font size
            body_content += f'<div class="word" style="left:{x}px; top:{default_height + y}px; font-size:{font_size}px;">{word}</div>\n'
        else:
            logger.warning(f"Low OCR confidence for word at index {i}: {ocr_result['text'][i]}")
    if line:
        body_content += f'<hr class="borderline" style="left:{0}px; top:{default_height + image.height}px; width:{image.width}px;"></hr>\n'

    return body_content


def images_to_html(images):
    html_content = '''
    <!DOCTYPE html>
    <html>
    <head>
    <style>
      body {
        position: relative;
      }
      .word {
        position: absolute;
      }
      .borderline {
            position: absolute;
        }
    </style>
    </head>
    <body>
    '''
    height = 0
    for url in images:
        img = Image.open(url)
        html_content += generate_html_page_from_image(img, default_height=height, line=True)
        height += img.height

    html_content += '''
    </body>
    </html>
    '''

    return html_content
