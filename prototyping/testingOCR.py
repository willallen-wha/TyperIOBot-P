from PIL import Image
import pytesseract as pt

# Test pytesseract as an image to text processor.
# Provide screenshot of entire typer.io screen and see what results are provided.

# Set path to tesseract command if necessary
# TODO add try/catch for checking default path for tesseract install
# pt.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
# Set the image to get text from
path = 'prototyping/prompt.png'

# Convert processed image to words
outtype = pt.image_to_string(path)

# Process a bit of the string
print(outtype.replace('\n', ' ').replace('|',' I ').replace('  ', ' '))