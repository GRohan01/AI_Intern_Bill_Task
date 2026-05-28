import streamlit as st
import pytesseract
from pdf2image import convert_from_bytes
import re
import numpy as np
import cv2
import os
import pandas as pd

# ==============================
# Tesseract Configuration
# ==============================

# Tessdata folder for deployment
tessdata_dir = os.path.join(os.getcwd(), "tessdata")
os.environ["TESSDATA_PREFIX"] = tessdata_dir

# ==============================
# Keywords (English + Marathi)
# ==============================

consumer_keywords = [
    "Consumer No",
    "Consumer Number",
    "Account No",
    "ग्राहक क्रमांक",
    "खाते क्रमांक"
]

name_keywords = [
    "Consumer Name",
    "Name",
    "ग्राहक नाव",
    "नाव"
]

mobile_keywords = [
    "Mobile No",
    "Mobile Number",
    "Mob No",
    "मोबाईल/इंमेल",
    "मोबाइल नंबर"
]

units_keywords = [
    "Units",
    "Units Consumed",
    "Consumption",
    "युनिट",
    "एकूण युनिट",
    " B ) "
]

amount_keywords = [
    "Amount",
    "Bill Amount",
    "या तारखे पर्यंत रू.",
    "पूर्णांक देयक (स)",
    "देयक रक्कम रु :"
]

# ==============================
# Extraction Functions
# ==============================

def extract_field(text, keywords):
    for keyword in keywords:
        pattern = rf"{keyword}[:\-]?\s*(.+)"
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return None


def extract_number(text, keywords):
    for keyword in keywords:
        pattern = rf"{keyword}.*?(\d+)"
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1)

    return None


def extract_name_from_mobile(text):
    lines = text.split('\n')

    for i, line in enumerate(lines):

        for keyword in mobile_keywords:

            if keyword.lower() in line.lower():

                if i + 1 < len(lines):

                    next_line = lines[i + 1].strip()

                    next_line = re.sub(
                        r'[^a-zA-Z\u0900-\u097F\s]',
                        '',
                        next_line
                    )

                    if next_line and not re.search(r'\d', next_line):

                        if not any(
                            word in next_line.lower()
                            for word in ["bill", "date", "amount"]
                        ):

                            return next_line

    return None

# ==============================
# PDF Processing
# ==============================

def process_pdf(file):

    images = convert_from_bytes(file.read())

    full_text = ""

    for img in images:

        img_np = np.array(img)

        gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)

        text = pytesseract.image_to_string(
            gray,
            lang='mar+eng',
            config='--psm 6'
        )

        full_text += text + "\n"

    return full_text

# ==============================
# Save to Excel
# ==============================

def save_to_excel(data):

    file_path = "Extract_Data.xlsx"

    new_data = pd.DataFrame([data])

    if os.path.exists(file_path):

        existing_data = pd.read_excel(file_path)

        updated_data = pd.concat(
            [existing_data, new_data],
            ignore_index=True
        )

    else:

        updated_data = new_data

    updated_data.to_excel(file_path, index=False)

# ==============================
# Streamlit UI
# ==============================

st.title("Smart Light Bill Data Extractor (Marathi + English)")

uploaded_file = st.file_uploader(
    "Upload Light Bill PDF",
    type=["pdf"]
)

if uploaded_file:

    with st.spinner("Processing PDF..."):

        text = process_pdf(uploaded_file)

    st.subheader("Extracted Text")

    st.text_area(
        "",
        text,
        height=250
    )

    # ==============================
    # Extract Data
    # ==============================

    name = extract_field(text, name_keywords)

    if not name:
        name = extract_name_from_mobile(text)

    consumer_no = extract_number(text, consumer_keywords)

    units = extract_number(text, units_keywords)

    amount = extract_number(text, amount_keywords)

    result = {
        "Consumer Name": name,
        "Consumer Number": consumer_no,
        "Units": units,
        "Amount": amount
    }

    st.subheader("Extracted Data")

    st.json(result)

    # ==============================
    # Save Data to Excel
    # ==============================

    save_to_excel(result)

    st.success("Data saved to Extract_Data.xlsx")
