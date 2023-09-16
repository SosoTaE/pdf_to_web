import os.path
import shutil
import tempfile
import pytesseract
from PIL import Image
from pdf_to_image import read_page_and_save_as_image
from config import tesseract_cmd
from logger import logger
import fitz

pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

def image_to_data(image):
    if isinstance(image, str):
        image = Image.open(image)

    if not isinstance(image, Image.Image):
        raise TypeError("image should be string or Image class")

    return pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
def image_to_pdf(images):
    pdf_file = fitz.open()
    for image in images:
        img = Image.open(image)
        ocr_result = image_to_data(img)
        page = pdf_file.new_page(width=img.width,height=img.height)
        for i in range(len(ocr_result["text"])):
            text = ocr_result["text"][i]
            left = ocr_result["left"][i]
            top = ocr_result["top"][i]
            h = ocr_result["height"][i]
            if text.strip():
                page.insert_text((left,top), text, fontsize=h)

    return pdf_file





