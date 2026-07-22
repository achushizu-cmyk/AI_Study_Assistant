"""
utils/ocr_engine.py
---------------------
OCR engine for handwritten notes and scanned images, backed by EasyOCR.

EasyOCR model loading is expensive, so the `Reader` instance is created only
once and cached for the lifetime of the Streamlit process.
"""

import streamlit as st
import numpy as np
from PIL import Image


@st.cache_resource(show_spinner=False)
def _load_reader():
    import easyocr
    return easyocr.Reader(["en"], gpu=False, verbose=False)


class OCREngine:
    """Extracts text from images, including handwritten notes."""

    def __init__(self):
        self.reader = _load_reader()

    def extract_text(self, image_path: str) -> str:
        """Run OCR on an image file and return the recognized text."""
        image = Image.open(image_path).convert("RGB")
        image_array = np.array(image)
        results = self.reader.readtext(image_array, detail=0, paragraph=True)
        return "\n".join(results).strip()

    def extract_text_from_pil(self, image: Image.Image) -> str:
        """Run OCR directly on a PIL Image object."""
        image_array = np.array(image.convert("RGB"))
        results = self.reader.readtext(image_array, detail=0, paragraph=True)
        return "\n".join(results).strip()
