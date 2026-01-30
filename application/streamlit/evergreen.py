import streamlit as st
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from application.test_api import *

# example PDF generator
def make_pdf_bytes(title_text: str) -> bytes:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 18)
    c.drawString(72, height - 72, title_text)

    #c.showPage()
    c.save()

    buffer.seek(0)
    return buffer.read()


# UI section
st.set_page_config(page_title="Evergreen Classrooms", page_icon="🌲", layout="centered")

st.title("Evergreen Classrooms")

# subsections
subtopic_dict = {
    "2.1": " - Vectors",
    "2.2": " - One-Dimensional Vectors",
    "2.3": " - 2D Coordinate System & Vectors",
    "2.4": " - 3D Coordinate System & Vectors",
    "2.5": " - Unit Vectors",
    "2.6": " - Vector Addition",
    "2.7": " - Dot Products",
    "2.8": " - Cross Products",

    "4.1": " - Moment of Force",
    "4.2": " - Scalar Addition of Moments",
    "4.3": " - Varignon's Theorem",
    "4.4": " - 3D Moments",
    "4.5": " - Couples",
    "4.6": " - Equivalent Transformations",
    "4.7": " - Statically Equivalent Systems"
}

subtopics_by_unit = {
    2: ["2.1", "2.2", "2.3", "2.4", "2.5", "2.6", "2.7", "2.8"],
    4: ["4.1", "4.2", "4.3", "4.4", "4.5", "4.6", "4.7"]
}

# sections
unit_dict = {
    2: "Chapter 2 - Forces and Other Vectors",
    4: "Chapter 4 - Moments and Static Equivalence"
}

unit = st.selectbox("Select Unit", options=[2, 4], index=0, format_func = lambda x: unit_dict.get(x))

subtopic_options = subtopics_by_unit.get(unit, [f"{unit}.1"])
subtopic = st.selectbox("Select Subtopic", options=subtopic_options, index=0, format_func = lambda x: x + str(subtopic_dict.get(x)))

domain = st.selectbox("Select Major", options=["Generic", "Aerospace Engineering", "Biomedical Engineering"], index=0)

st.divider()

# Confirm button makes pdf
if st.button("Generate a problem", type="primary"):
    word_problem = generate_problem(domain, unit, subtopic)
    st.text(word_problem)