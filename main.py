import os
from PIL import Image
from pdf2image import convert_from_path
import pytesseract


print(pytesseract.image_to_string(Image.open('new_scans/1.png')))
