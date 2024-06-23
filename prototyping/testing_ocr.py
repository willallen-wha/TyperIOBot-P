import pytesseract as pt

# Test pytesseract as an image to text processor.
# Provide screenshot of entire typer.io screen and see what results are provided.

# Set path to tesseract command if necessary
# TODO add try/catch for checking default path for tesseract install
# pt.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
# Set the image to get text from
PATH = 'prototyping/prompt.png'

# Convert processed image to words
outtype = pt.image_to_string(PATH)
# Process a bit of the string
outtype = outtype.replace('\n', ' ').replace('|',' I ').replace('  ', ' ').strip()

# Write string to file to be written
sourceFile = open("prototyping/prompt.txt", "wt", encoding="utf-8")
sourceFile.write(outtype)
sourceFile.close()
