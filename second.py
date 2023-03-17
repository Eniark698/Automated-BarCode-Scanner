from PIL import Image
import PIL.ImageOps
Image.MAX_IMAGE_PIXELS = 1000000000
image = Image.open('./new_scans/1-2.png')

inverted_image = PIL.ImageOps.invert(image.convert('RGB'))

inverted_image.save('./new_name.png')
