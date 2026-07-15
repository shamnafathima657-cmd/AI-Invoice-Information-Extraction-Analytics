# AI-Powered-Invoice-Information-Extraction-System
AAI-powered invoice information extraction system using EasyOCR, Regex, Streamlit, and Python.


# AI-Powered Invoice Information Extraction System

## Overview

This project extracts important information from invoice images and PDF documents using EasyOCR and Regular Expressions (Regex).

## Features

- Upload invoice images and PDFs
- OCR using EasyOCR
- Extract:
  - Company Name
  - Invoice Number
  - Invoice Date
  - Tax Amount
  - Payment Method
  - Total Amount
- Save extracted data to CSV
- Analytics Dashboard
- Interactive Streamlit interface

## Technologies

- Python
- Streamlit
- EasyOCR
- Pandas
- Plotly
- OpenCV
- NumPy
- Regex

## Workflow

Invoice → OCR → Text Extraction → Regex → Structured Data → CSV → Analytics

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
