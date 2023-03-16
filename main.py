import os
from PIL import Image
from pdf2image import convert_from_path
import pytesseract


print(pytesseract.image_to_string(Image.open('scans/1.pdf')))

filePath = '/Users/nazarii_mozol/projects/berta/pytess/scans/1.pdf'
doc = convert_from_path(filePath)
path, fileName = os.path.split(filePath)
fileBaseName, fileExtension = os.path.splitext(fileName)

for page_number, page_data in enumerate(doc):
    txt = pytesseract.image_to_string(Image.fromarray(page_data)).encode("utf-8")
    print("Page # {} - {}".format(str(page_number),txt))
