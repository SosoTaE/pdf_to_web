from dotenv import load_dotenv
import os

load_dotenv(".env")

tesseract_cmd = os.getenv("tesseract_cmd")

print(tesseract_cmd)

