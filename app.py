import streamlit as st
import pandas as pd
import plotly.express as px
import os
from PIL import Image

from utils.ocr import extract_text
from models.invoice_extractor import extract_invoice_data


# ---------------------------------
# Page Configuration
# ---------------------------------

st.set_page_config(
    page_title="AI Invoice Information Extraction",
    page_icon="🧾",
    layout="wide"
)
# -----------------------------
# Custom Theme
# -----------------------------
st.markdown("""
<style>

/* Main background */
.stApp {
    background: linear-gradient(135deg,#0f172a,#1e293b);
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background: linear-gradient(180deg,#111827,#1f2937);
}

section[data-testid="stSidebar"] *{
    color:white;
}

/* Main Title */
h1{
    color:#38bdf8;
    font-weight:700;
}

/* Sub Headings */
h2,h3{
    color:#60a5fa;
}

/* Buttons */
.stButton>button{
    background:#2563eb;
    color:white;
    border-radius:10px;
    border:none;
    padding:10px 25px;
    transition:0.3s;
}

.stButton>button:hover{
    background:#1d4ed8;
    transform:scale(1.05);
}

/* Download button */
.stDownloadButton>button{
    background:#16a34a;
    color:white;
    border-radius:10px;
}

.stDownloadButton>button:hover{
    background:#15803d;
}

/* File uploader */
[data-testid="stFileUploader"]{
    border:2px dashed #38bdf8;
    border-radius:12px;
    padding:20px;
    background:#1e293b;
}

/* Dataframe */
[data-testid="stDataFrame"]{
    border-radius:12px;
    overflow:hidden;
}

/* Success box */
.stSuccess{
    border-radius:10px;
}

/* Info box */
.stInfo{
    border-radius:10px;
}

/* Metric cards */
[data-testid="metric-container"]{
    background:#1f2937;
    border:1px solid #334155;
    padding:15px;
    border-radius:15px;
    box-shadow:0 0 10px rgba(0,0,0,0.4);
}

/* Expanders */
.streamlit-expanderHeader{
    background:#1e293b;
    border-radius:8px;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------
# Sidebar
# ---------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Choose a Page",
    [
        "🏠 Home",
        "📤 Upload Invoice",
        "📊 Analytics",
        "ℹ️ About"
    ]
) 

# ---------------------------------
# CSV File
# ---------------------------------

CSV_FILE = "outputs/invoices.csv"

os.makedirs("outputs", exist_ok=True)

# ---------------------------------
# Home Page
# ---------------------------------
if page == "🏠 Home":

    st.title("🧾 AI-Powered Invoice Information Extraction System")

    st.markdown("""
    ### Welcome 👋

    This application automatically extracts important information from invoice
    images using **EasyOCR** and **pattern-based information extraction (Regex)**.

    The extracted invoice details are stored in CSV format and visualized
    through an interactive analytics dashboard.

    Upload your invoices and receive structured information within seconds.
    """)

    st.divider()

    # Dashboard Cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📄 Supported Files", "JPG / PDF / png")

    with col2:
        st.metric("🤖 OCR Engine", "EasyOCR")

    with col3:
        st.metric("📊 Output", "CSV")

    with col4:
        st.metric("⚡ Extraction", "Regex")

    st.divider()

    col1, col2 = st.columns([1, 1])

    with col1:

        st.subheader("✨ Features")

        st.markdown("""
        ✅ Upload Invoice Images

        ✅ Upload PDF Invoices

        ✅ Automatic Text Recognition (EasyOCR)

        ✅ Extract Key Invoice Details

        ✅ Multiple Invoice Upload

        ✅ Save Results to CSV

        ✅ Analytics Dashboard

        ✅ Download Extracted Data
        """)

    with col2:

        st.subheader("📌 Extracted Information")

        st.markdown("""
        🏢 Company Name

        🧾 Invoice Number

        📅 Invoice Date

        🧮 Tax Amount

        💳 Payment Method

        💰 Total Amount
        """)

    st.divider()

    st.info("📤 Select **Upload Invoice** from the left sidebar to begin processing your invoices.")
    st.subheader("🔄 System Workflow")

    st.markdown("""
    ```text
    📄 Invoice Image / PDF
        │
        ▼
    🖼 Image Preprocessing
        │
        ▼
    🤖 EasyOCR
        │
        ▼
    📝 Extracted Text
        │
        ▼
   🔍 Regex 
        │
        ▼
   📋 Structured Invoice Data
        │
        ▼
   💾 CSV Storage
        │
        ▼
   📊 Analytics Dashboard
                """)
    

    ### 6. Add a project objective

    st.subheader("🎯 Project Objective")

    st.success("""
    To automate invoice information extraction from invoice images
    using OCR and pattern matching, reducing manual data entry and
    providing summarized analytics for business records.
    """)

# ---------------------------------
# Upload Page
# ---------------------------------
elif page == "📤 Upload Invoice":

    st.title("📤 Upload Invoice")
    st.write("Upload one or more invoice images or PDF files.")

    uploaded_files = st.file_uploader(
        "Choose Invoice(s)",
        type=["jpg", "jpeg", "png", "pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:

        results = []

        progress = st.progress(0)

        total = len(uploaded_files)

        for index, uploaded_file in enumerate(uploaded_files):

            progress.progress((index + 1) / total)

            st.divider()

            st.header(f"📄 Invoice {index+1}")

            st.write(f"**File Name:** {uploaded_file.name}")

            # -----------------------------
            # Display Image
            # -----------------------------
            if uploaded_file.name.lower().endswith(("jpg", "jpeg", "png")):

                image = Image.open(uploaded_file)

                col1, col2 = st.columns([1, 1])

                with col1:
                    st.image(
                        image,
                        caption="Uploaded Invoice",
                        use_container_width=True
                    )

                uploaded_file.seek(0)

            else:

                col1, col2 = st.columns([1, 1])

                with col1:
                    st.info("📄 PDF uploaded successfully.")
            

            # -----------------------------
            # OCR
            # -----------------------------

            with st.spinner("🔍 Processing invoice..."):
                text = extract_text(uploaded_file)


            # -----------------------------
            # Extraction
            # -----------------------------
            invoice_data = extract_invoice_data(text)

            results.append(invoice_data)

            with col2:

                st.subheader("📋 Extracted Details")

                st.write("🏢 **Company Name:**", invoice_data["Company Name"])
                st.write("🧾 **Invoice Number:**", invoice_data["Invoice Number"])
                st.write("📅 **Invoice Date:**", invoice_data["Invoice Date"])
                st.write("🧮 **Tax:**", invoice_data["Tax"])
                st.write("💳 **Payment Method:**", invoice_data["Payment Method"])
                st.write("💰 **Total Amount:**", invoice_data["Total Amount"])

            # -----------------------------
            # OCR Text
            # -----------------------------
            with st.expander("📄 View OCR Text"):

                st.text(text)

        # -----------------------------
        # Summary
        # -----------------------------
        st.divider()

        st.success("✅ All invoices processed successfully.")

        # Create DataFrame
        df = pd.DataFrame(results)

        st.subheader("📊 Extracted Invoice Summary")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
       )

       # Save to CSV
        if os.path.exists(CSV_FILE):
            old_df = pd.read_csv(CSV_FILE)

            # Optional: remove duplicates if the same files are uploaded again
            df = pd.concat([old_df, df], ignore_index=True)
            df = df.drop_duplicates()

        # Save
        df.to_csv(CSV_FILE, index=False)

        st.success("📁 Data saved successfully!")

        # Download button
        with open(CSV_FILE, "rb") as file:
           st.download_button(
           label="📥 Download CSV",
           data=file,
           file_name="invoices.csv",
           mime="text/csv"
        )
# ---------------------------------
# Analytics Page
# ---------------------------------

elif page == "📊 Analytics":

    st.title("📊 Analytics Dashboard")

    if not os.path.exists(CSV_FILE):
        st.warning("⚠️ No invoice data found. Please upload invoices first.")
        st.stop()

    df = pd.read_csv(CSV_FILE)

    if df.empty:
        st.warning("⚠️ CSV file is empty.")
        st.stop()

    # -----------------------------
    # Clean Total Amount
    # -----------------------------
    df["Total Amount"] = (
        df["Total Amount"]
        .astype(str)
        .str.replace(",", "", regex=False)
    )

    df["Total Amount"] = pd.to_numeric(
        df["Total Amount"],
        errors="coerce"
    ).fillna(0)


    st.divider()

    # -----------------------------
    # Metrics
    # -----------------------------
    total_invoices = len(df)
    total_revenue = df["Total Amount"].sum()
    average_invoice = df["Total Amount"].mean()
    

    col1, col2, col3  = st.columns(3)

    with col1:
        st.metric(
            "📄 Total Invoices",
            total_invoices
        )

    with col2:
        st.metric(
            "💰 Total Revenue",
            f"{total_revenue:.2f}"
        )

    with col3:
        st.metric(
            "📈 Average Invoice",
            f" {average_invoice:.2f}"
        )
    


    st.divider()

    # -----------------------------
    # Revenue by Company
    # -----------------------------
    st.subheader("🏢 Revenue by Company")

    company_df = (
        df.groupby("Company Name")["Total Amount"]
        .sum()
        .reset_index()
    )

    fig_company = px.bar(
        company_df,
        x="Company Name",
        y="Total Amount",
        color="Company Name",
        text_auto=True,
        title="Revenue by Company"
    )

    st.plotly_chart(
        fig_company,
        use_container_width=True
    )

    # -----------------------------
    # Payment Method Distribution
    # -----------------------------
    st.subheader("💳 Payment Method Distribution")

    payment_df = (
        df["Payment Method"]
        .fillna("Unknown")
        .replace("", "Unknown")
        .value_counts()
        .reset_index()
    )

    payment_df.columns = ["Payment Method", "Count"]

    fig_payment = px.pie(
        payment_df,
        names="Payment Method",
        values="Count",
        hole=0.4,
        title="Payment Methods"
    )

    st.plotly_chart(
        fig_payment,
        use_container_width=True
    )
    # -----------------------------
    # Tax Distribution chart
    # -----------------------------
    st.subheader("🧾 Tax Amount by Invoice")

    fig_tax = px.bar(
    df,
    x="Invoice Number",
    y="Tax",
    color="Company Name",
    text_auto=True,
    title="Tax Amount"
    )

    st.plotly_chart(
    fig_tax,
    use_container_width=True
    )

    # -----------------------------
    # Invoice Data
    # -----------------------------
    st.subheader("📋  Invoice Summary")

    st.dataframe(df[[
    "Company Name",
    "Invoice Number",
    "Invoice Date",
    "Tax",
    "Payment Method",
    "Total Amount"
    ]],
        use_container_width=True
    )
# -----------------------------
# About Page
# -----------------------------
elif page == "ℹ️ About":

    st.title("ℹ️ About")

    st.markdown("""
    ## AI-Powered Invoice Information Extraction System

    This project is designed to automatically extract important information
    from invoice images and PDF documents using **EasyOCR** and
    **Regular Expression (Regex)** based information extraction.

    The extracted invoice details are processed, displayed in a structured
    format, stored in CSV files, and visualized through an interactive
    analytics dashboard.

    ### 🎯 Project Objectives
    - Automate invoice information extraction.
    - Reduce manual data entry.
    - Improve invoice processing efficiency.
    - Store extracted data for future analysis.
    - Provide visual analytics of invoice records.
    """)
    
    st.divider()

    st.subheader("⚠️ Current Limitations")

    st.markdown("""
    - OCR accuracy depends on image quality.
    - Blurred or low-resolution invoices may reduce extraction accuracy.
    - The current system works best with printed invoices.
    - Different invoice layouts may require additional extraction rules.
    - Handwritten invoices are not supported.
    - Multi-page PDF invoices are processed page by page.
    """)

    st.divider()

    st.subheader("🚀 Future Improvements")

    st.markdown("""
    - Integrate Transformer-based document understanding models.
    - Improve extraction for multiple invoice layouts.
    - Support handwritten invoice recognition.
    - Export data to Excel and database systems.
    - Add cloud storage integration.
    - Improve OCR preprocessing techniques.
    - Detect duplicate invoices automatically.
    - Add user authentication and role-based access.
    """)

    st.divider()

    st.success(
        "Developed as an AI-based invoice information extraction system using OCR and intelligent pattern matching."
    )
