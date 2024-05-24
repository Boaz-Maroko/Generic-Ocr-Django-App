import pytesseract
from PIL import Image


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def ocr_image(imag_path):
    try:
        image = Image.open(imag_path)

        text = pytesseract.image_to_string(image)

        return text
    
    except Exception as e:
        return str(e)
    
