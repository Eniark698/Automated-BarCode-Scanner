import os
from PIL import Image
import pytesseract


print(pytesseract.image_to_string(Image.open('new_scans/1.png')))
