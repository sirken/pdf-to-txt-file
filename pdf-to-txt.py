#!/usr/bin/env python3

import os
import io
import sys
from PIL import Image
import pytesseract
from wand.image import Image as wi
import gc
from glob import glob
import time

# List of pdf files to process
pdf_list = []

print("[[ PDF to txt ]]\r\n")

# Change directory to be in same folder as this script
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
os.chdir(__location__)

# Find files in folder with extension
def find_ext(dr, ext):
    return glob(os.path.join(dr,"*.{}".format(ext)))

# If no CLI arguments, search folder for pdf files
if len(sys.argv) == 1:
    pdf_list = find_ext(".", "pdf")
# Otherwise, get filenames from CLI
elif len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        pdf_list.append(arg)

# Function to do ocr > pdf > txt
def Get_text_from_image(pdf_path):
    print(f"Processing {pdf_path}...")
    pdf=wi(filename=pdf_path,resolution=300)
    pdfImg=pdf.convert('jpeg')
    imgBlobs=[]
    extracted_text=[]
    print(" - Generating images")
    for img in pdfImg.sequence:
        page=wi(image=img)
        imgBlobs.append(page.make_blob('jpeg'))
    print(" - Running OCR")
    for imgBlob in imgBlobs:
        im=Image.open(io.BytesIO(imgBlob))
        text=pytesseract.image_to_string(im,lang='eng')
        extracted_text.append(text)
    print(" - Saving txt file")
    return (extracted_text)


# Loop through list of pdf files
for file in pdf_list:

    # Get text from pdf
    output = Get_text_from_image(file)

    # Save output to a txt file
    with open(file + ".txt", 'w') as f:
        for item in output:
            f.write("%s\n" % item)
