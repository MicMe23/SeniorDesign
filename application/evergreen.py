import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from test_api import *

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

context = {
    "basic": "short/simple context",
    "creative": "long/creative context"
}

if "problem" not in st.session_state:
    st.session_state.problem = ""
if "last_meta" not in st.session_state:
    st.session_state.last_meta = None

with st.sidebar:
    st.header("Problem Settings")

    with st.form("generator_form", border=True):
        unit = st.selectbox("Chapter", options=list(unit_dict.keys()), index=0, format_func=lambda x: unit_dict[x])
        subtopic_options = subtopics_by_unit[unit]
        subtopic = st.selectbox("Topic", options=subtopic_options, index=0, format_func=lambda x: f"{x}{subtopic_dict.get(x, '')}"
)
        injection = st.text_input(label = "custom context. (do not add too much)")
        context = st.selectbox("Context",
                               options = context)
        domain = st.selectbox("Major", options=["Generic", "Aerospace Engineering", "Biomedical Engineering"], index=0)

        velocity_units = st.selectbox("Units (per second)", options=["Kilometers", "Meters", "Centimeters", "Feet"], index=0)
        st.divider()

        generate_clicked = st.form_submit_button("Generate problem", type="primary", use_container_width=True)

# we will replae this when the matrix generator is useable. For now it loads in 1 of 2 random matrices in data/chapter2
matrix_name, matrix_path, MATRIX = load_random_matrix()

if matrix_name is not None:
    try:
        df = pd.read_csv(matrix_path)   
        st.subheader("Edit your data below:")
        edited_df = st.data_editor(df, num_rows="dynamic")
    except Exception as e:
        st.error(f"Error reading file: {e}")
    
    csv_bytes = edited_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download CSV",
        data=csv_bytes,
        file_name=matrix_name,
        mime="text/csv",
        use_container_width=True,
    )

else:
    st.info("Please generate a matrix to start editing.")





# ---------- Generate ----------
if generate_clicked:
    with st.spinner("Generating…"):
        st.session_state.problem = generate_problem(domain, unit, subtopic, injection, context, velocity_units, matrix_name, MATRIX)
        st.session_state.last_meta = {"domain": domain, "unit": unit, "subtopic": subtopic, "custom context": injection, "context": context, "velocity_units": velocity_units, "matrix_name": matrix_name, "MATRIX": MATRIX}

# ---------- Main output ----------
st.divider()

meta = st.session_state.last_meta
if meta:
    st.caption(f"**Selected:** {unit_dict[meta['unit']]} • {meta['subtopic']} — {subtopic_dict.get(meta['subtopic'], '')} • {meta['domain']}")

if st.session_state.problem:
    with st.container(border=True):
        st.subheader("Generated Problem")
        st.code(st.session_state.problem, language="text")

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Regenerate", use_container_width=True):
                with st.spinner("Regenerating…"):
                    st.session_state.problem = generate_problem(domain, unit, subtopic, injection, context, velocity_units, matrix_name, MATRIX)
                    st.session_state.last_meta = {"domain": domain, "unit": unit, "subtopic": subtopic}

else:
    st.info("Choose settings in the sidebar, then click **Generate problem**.")