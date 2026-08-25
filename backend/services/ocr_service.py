import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes


POPPLER_PATH = r"C:\Users\soura\Downloads\Release-26.02.0-0\poppler-26.02.0\Library\bin"


def extract_text_from_image(image_path: str) -> str:
    """
    Takes an image file path and extracts text from the image.
    """

    text = pytesseract.image_to_string(Image.open(image_path))

    return text


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Takes PDF bytes and extracts text using OCR.
    """

    pages = convert_from_bytes(
        pdf_bytes,
        poppler_path=POPPLER_PATH
    )

    all_text = []

    for page in pages:
        text = pytesseract.image_to_string(page)
        all_text.append(text)

    return "\n".join(all_text)