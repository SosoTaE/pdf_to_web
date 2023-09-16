import os
import shutil
import tempfile

from image_to_html import images_to_html
from logger import logger
from pdf_to_image import read_page_and_save_as_image


def read_pdf_and_save_as_html(pdf_file, result_file_path):
    logger.info("Started reading PDF and saving as HTML.")
    if not isinstance(pdf_file, str):
        message = "pdf_file should be a string"
        logger.error(message)
        raise TypeError(message)

    if not isinstance(result_file_path, str):
        message = "output_file should be a string"
        logger.error(message)
        raise TypeError(message)

    output_file = tempfile.mkdtemp()

    logger.info(f"Temporary directory created at {output_file}")

    logger.info(f"Reading PDF from {pdf_file}")
    read_page_and_save_as_image(pdf_file, output_file)

    images = [f"{output_file}/{url}" for url in os.listdir(output_file)]

    logger.info(f"{len(images)} images will be processed.")

    html = images_to_html(images)
    logger.info(f"html processing was done")

    shutil.rmtree(output_file)
    logger.info(f"Removing temporary directory {output_file}")

    with open(result_file_path, "w", encoding="utf-8") as file:
        file.write(html)
