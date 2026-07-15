import easyocr
import numpy as np
import cv2
from PIL import Image
from pdf2image import convert_from_bytes

POPPLER_PATH = r"C:\poppler\poppler-24.08.0\Library\bin"

reader = easyocr.Reader(['en'])


def preprocess_image(image):

    # Convert PIL image to numpy array
    image = np.array(image)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # Reduce noise
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    # Improve contrast
    gray = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        10
    )

    return gray


def extract_text(uploaded_file):

    text = ""

    # -----------------------------
    # PDF
    # -----------------------------
    if uploaded_file.name.lower().endswith(".pdf"):

        pages = convert_from_bytes(
            uploaded_file.read(),
            poppler_path=POPPLER_PATH
        )

        for page in pages:

            image = preprocess_image(page)

            result = reader.readtext(
                image,
                detail=0,
                paragraph=True
            )

            text += "\n".join(result) + "\n"

    # -----------------------------
    # Image
    # -----------------------------
    else:

        image = Image.open(uploaded_file)

        image = preprocess_image(image)

        result = reader.readtext(
            image,
            detail=0,
            paragraph=True
        )

        text = "\n".join(result)

    return text.strip()