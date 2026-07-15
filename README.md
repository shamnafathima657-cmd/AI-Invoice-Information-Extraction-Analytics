# AI-Powered-Invoice-Information-Extraction-System
AAI-powered invoice information extraction system using EasyOCR, Regex, Streamlit, and Python.

#  AI-Powered Invoice Information Extraction System

##  Project Overview

The AI-Powered Invoice Information Extraction System is a web-based application developed using Python and Streamlit. It automates the extraction of important information from invoice images and PDF documents using Optical Character Recognition (OCR) and intelligent pattern-based information extraction.

The application reads invoice documents, extracts relevant information, stores the extracted data in CSV format, and provides an interactive analytics dashboard for visualization.

---

#  Project Objectives

- Automate invoice information extraction.
- Reduce manual data entry.
- Improve processing speed and accuracy.
- Store extracted invoice information in CSV format.
- Visualize invoice data using an analytics dashboard.

---

#  Features

- Upload invoice images (JPG, JPEG, PNG)
- Upload PDF invoices
- Automatic text extraction using EasyOCR
- Extract Company Name
- Extract Invoice Number
- Extract Invoice Date
- Extract Tax Amount
- Detect Payment Method
- Extract Total Amount
- Store extracted data in CSV
- Interactive Analytics Dashboard
- Simple and user-friendly Streamlit interface

---

#  Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Programming Language |
| Streamlit | Web Application Framework |
| EasyOCR | Optical Character Recognition |
| Regex | Invoice Information Extraction |
| Pandas | Data Processing |
| Plotly | Interactive Charts |
| OpenCV | Image Processing |
| NumPy | Numerical Computation |

---

#  Project Structure

```
AI-Powered-Invoice-Information-Extraction-System/

│
├── app.py
├── extract.py
├── ocr.py
├── invoice_data.csv
├── requirements.txt
├── README.md
│
└── screenshots/
    ├── home.png
    ├── upload.png
    ├── extraction.png
    ├── analytics.png
```

---

#  System Workflow

```
Invoice Image / PDF
        │
        ▼
Image Preprocessing
        │
        ▼
EasyOCR
        │
        ▼
Extracted Text
        │
        ▼
Regex Information Extraction
        │
        ▼
Structured Invoice Data
        │
        ▼
CSV Storage
        │
        ▼
Analytics Dashboard
```

---

#  Extracted Invoice Fields

The application extracts the following information:

- Company Name
- Invoice Number
- Invoice Date
- Tax Amount
- Payment Method
- Total Amount

---

#  Analytics Dashboard

The dashboard provides:

- Total Number of Invoices
- Total Revenue
- Average Invoice Value
- Total Tax Collected
- Revenue by Company
- Payment Method Distribution
- Invoice Summary Table

---

#  Installation

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Application

```bash
streamlit run app.py
```

---

#  Sample Workflow

1. Open the application.
2. Upload an invoice image or PDF.
3. OCR extracts text.
4. Regex extracts invoice information.
5. Data is displayed.
6. Data is saved to CSV.
7. Analytics dashboard is updated automatically.

---

#  Limitations

- OCR accuracy depends on image quality.
- Works best with printed invoices.
- Different invoice layouts may require additional Regex rules.
- Handwritten invoices are not fully supported.
- Multi-page PDFs are processed one page at a time.

---

#  Future Enhancements

- Support multiple invoice layouts.
- Improve OCR accuracy using advanced AI models.
- Handwritten invoice recognition.
- Export to Excel and PDF.
- Cloud database integration.
- Duplicate invoice detection.
- User authentication.
- Multi-language invoice support.

#  Conclusion
The AI-Powered Invoice Information Extraction System automates the extraction of key invoice details from invoice images and PDF documents using EasyOCR and Regex. It reduces manual data entry, stores extracted information in CSV format, and provides an analytics dashboard for easy data visualization. The project demonstrates an efficient, accurate, and user-friendly solution for invoice processing, with scope for future improvements such as support for more invoice formats and advanced AI-based extraction techniques.

AI-Powered Invoice Information Extraction System

Academic Project – 2026
