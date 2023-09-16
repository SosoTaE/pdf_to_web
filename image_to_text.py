from PIL import Image
import pytesseract
from pytesseract import Output

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path

def create_matrix(size, item=" "):
    width, height = size

    matrix = []

    for i in range(height):
        matrix.append([item] * width)

    return matrix

def image_to_text(image):
    data = pytesseract.image_to_string(image)
    return data

def generate_text(matrix):
    text = ""
    for row in matrix:
        row_text = "".join(row).rstrip()  # Remove trailing spaces
        if row_text:  # Skip empty lines
            text += row_text + '\n'

    return text

def read_image_and_generate_text(url:str) -> str:
    if not isinstance(url,str):
        raise TypeError("url should be a string")

    image = Image.open(url)

    width, height = image.size
    matrix = create_matrix(size=image.size)

    # Perform OCR and get data as a text
    text = image_to_text(image)

    return text
