import streamlit as st
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


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
subtopics_by_unit = {
    1: ["1.1", "1.2", "1.3"],
    2: ["2.1", "2.2", "2.3"],
    3: ["3.1", "3.2", "3.3"],
    4: ["4.1", "4.2", "4.3"],
    5: ["5.1", "5.2", "5.3"],
}

# sections
unit = st.selectbox("Select Unit", options=[1, 2, 3, 4, 5], index=0)

subtopic_options = subtopics_by_unit.get(unit, [f"{unit}.1"])
subtopic = st.selectbox("Select Subtopic", options=subtopic_options, index=0)

st.divider()

# Confirm button makes pdf
if st.button("Confirm", type="primary"):
    pdf_bytes = make_pdf_bytes("nothing important right now")

    filename = f"EvergreenClassrooms_Unit{unit}_Topic{subtopic}.pdf"
    st.success(f"Created Unit {unit}, Subtopic {subtopic}")

    st.download_button(
        label="Download PDF",
        data=pdf_bytes,
        file_name=filename,
        mime="application/pdf",
    )
