from os import mkdir
import fitz  # PyMuPDF
import io
from PIL import Image
from logger import logger


def arguments_type_checker(file_path, output_path, page):
    if not isinstance(file_path, str):
        raise TypeError("file_path should be a string")

    if not isinstance(output_path, str):
        raise TypeError("file_path should be a string")

    if page is not None and not isinstance(page, int):
        raise TypeError("page should be integer")

def read_images_and_save(pdf_file, output_path, page):
    for page_num in range(min(page,len(pdf_file))):
        # Get page
        print(page_num)
        page = pdf_file.load_page(page_num)

        image_list = page.get_images(full=True)

        print(image_list)

        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_file.extract_image(xref)
            image_bytes = base_image["image"]

            # Open the image with PIL
            image = Image.open(io.BytesIO(image_bytes))
            image.save(open(f"{output_path}/image{page_num}_{img_index}.jpg", "wb"), "JPEG")

def read_pages_and_save(pdf_file, output_path, pages):
    for page_num in pages:
        # Get page
        logger.info(f"currently loading page:{page_num}")
        page = pdf_file.load_page(page_num)

        # Using a scaling matrix to increase resolution
        zoom_x = 4.0  # horizontal zoom
        zoom_y = 4.0  # vertical zoom
        mat = fitz.Matrix(zoom_x, zoom_y)  # Create the scaling matrix

        # Render page to pixmap with higher resolution
        page_image = page.get_pixmap(matrix=mat, colorspace=fitz.csRGB)
        logger.info(f"currently getting page as a image page:{page_num}")

        logger.info(f"save image at directory:{output_path}/image{page_num}.jpg")
        page_image.save(f"{output_path}/image{page_num}.jpg")

def read_pdf(file_path):
    logger.info(f"start reading pdf file:{file_path}",)
    try:

        return fitz.open(file_path)
    except Exception as e:
        print(f"Error opening PDF file: {e}")
        exit()


def read_images_from_pdf_and_save(file_path:str, output_path:str, page=None) -> list:
    logger.info("start reading images from pdf file to save it as a image")
    arguments_type_checker(file_path, output_path, page)

    # Open the PDF file
    pdf_file = read_pdf(file_path)

    if page is None:
        page = len(pdf_file)

    # Iterate through PDF pages
    read_images_and_save(pdf_file,output_path,page)

def read_page_and_save_as_image(file_path:str, output_path:str, page=None):
    logger.info("start reading images from pdf file to save it as a image")
    arguments_type_checker(file_path, output_path, page)

    # Open the PDF file
    pdf_file = read_pdf(file_path)

    if page is None:
        page = list(range(len(pdf_file)))

    read_pages_and_save(pdf_file, output_path, page)

if __name__ == "__main__":
    path = "meta"
    try:
        mkdir(path)
    except FileExistsError  as e:
        print(e)
    read_page_and_save_as_image("Meta_#HE9D4T3TC2_09-06-2023_$900.pdf", path)
