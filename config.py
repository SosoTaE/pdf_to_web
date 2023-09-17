from dotenv import load_dotenv
import os

load_dotenv(".env")

# get tesseract_cmd directory
tesseract_cmd = os.getenv("tesseract_cmd")

load_dotenv(".env.requirements")

# load server requirements
SERVER = os.getenv("SERVER")
PORT = os.getenv("PORT")
ADDRESS = os.getenv("ADDRESS")
PASSWORD = os.getenv("PASSWORD")

