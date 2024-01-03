from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import os
import json

def perform_ocr(image_path):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    # Ensure image_path is a valid path to an existing image file
    if os.path.exists(image_path):
        return pytesseract.image_to_string(Image.open(image_path))
    else:
        return "File not found"

def create_json_file(pdf_path, text, additional_arg):
    pdf_name = os.path.basename(pdf_path)
    json_data = {'text': text}

    # Get the directory of the Python script
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Create a new directory in the script directory with the name of the PDF
    json_folder = os.path.join(script_dir, pdf_name.replace('.pdf', ''))
    os.makedirs(json_folder, exist_ok=True)

    # Create the path to the JSON file
    json_file_path = os.path.join(json_folder, pdf_name.replace('.pdf', '.json'))

    # Write the JSON data to the file
    with open(json_file_path, 'w') as json_file:
        json.dump(json_data, json_file)

def pdf_to_images(pdf_path, output_folder):
    images = convert_from_path(pdf_path)
    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f"page_{i + 1}.png")
        image.save(image_path, 'PNG')
        yield image_path

def main(pdf_path):
    output_folder = os.path.dirname(pdf_path)
    text = ""

    for image_path in pdf_to_images(pdf_path, output_folder):
        ocr_text = perform_ocr(image_path)
        text += ocr_text

    create_json_file(pdf_path, text, output_folder)
    print(f'Text extracted and saved to {os.path.join(output_folder, pdf_path.replace(".pdf", ""))}')

if __name__ == "__main__":
    main('C:/Users/uribrown/OneDrive - Microsoft/ATS/cloud cost report - anodot.pdf')
