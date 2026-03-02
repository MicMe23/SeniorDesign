import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from test_api import *
import streamlit.components.v1 as component

# example PDF generator -- DEPRECATED
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


############################## UI prep ##############################

st.set_page_config(page_title="Evergreen Classrooms", page_icon="🌲", layout="centered")

st.title("Evergreen Classrooms")

# --- Subtopic selector ---
# Connect subsection numbers to their corresponding titles
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

# Connect a chapter with all of its subchapters
subtopics_by_unit = {
    2: ["2.1", "2.2", "2.3", "2.4", "2.5", "2.6", "2.7", "2.8"],
    4: ["4.1", "4.2", "4.3", "4.4", "4.5", "4.6", "4.7"]
}

# --- Section selector ---
# Connect a chapter number with its title
unit_dict = {
    2: "Chapter 2 - Forces and Other Vectors",
    4: "Chapter 4 - Moments and Static Equivalence"
}

# --- Context selector ---
# Connect a selectbox choice to its description
context = {
    "Basic": "short/simple context",
    "Creative": "long/creative context"
}

asset_choices = {
    "Generic": [],
    "Aerospace Engineering": ["Plane (seen from the side)"],
    "Biomedical Engineering": ["Person (seen from above)"]
}

# --- Unit selector ---
# Connect a vector type to all possible measurements
unit_types = {
    "Velocity": ["Meters per second", "Kilometers per hour", "Feet per second", "Miles per hour", "Knots"],
    "Acceleration": ["Meters per second squared", "Feet per second squared", "Gs"],
    "Force": ["Newtons", "Kilonewtons", "Pounds-force", "Kips"],
    "Torque": ["Newton-meters", "Kilonewton-meters", "Pound-feet", "Kip-feet"]
}

# Connect a selection tuple to what units are reasonable to be selected
# --- Chapter 4 is set to all temporarily
unit_selector = {
    (2): ["Velocity", "Acceleration", "Force"],
    (4): ["Velocity", "Acceleration", "Force", "Torque"]
}

############################## Sidebar ##############################

if "problem" not in st.session_state:
    st.session_state.problem = ""
if "last_meta" not in st.session_state:
    st.session_state.last_meta = None
if "pic_seeded" not in st.session_state:
    st.session_state.pic_seeded = True
if "unit_seeded" not in st.session_state:
    st.session_state.unit_seeded = True

with st.sidebar:
    st.header("Problem Settings")

    ### Everything inside the sidebar's small box ###
    with st.form("generator_form", border=True):
        # Displays the Chapter selectbox
        unit = st.selectbox("Chapter", options=list(unit_dict.keys()), index=0, format_func=lambda x: unit_dict[x])
        subtopic_options = subtopics_by_unit[unit]

        # Displays the Topic selectbox
        subtopic = st.selectbox("Topic", options=subtopic_options, index=0, format_func=lambda x: f"{x}{subtopic_dict.get(x, '')}")

        # Displays the Context prompt
        injection = st.text_input(label = "Custom context (do not add too much)")
        context = st.selectbox("Level of Detail",
                               options = context)
        
        # Displays the Major selectbox
        domain = st.selectbox("Major", options=["Generic", "Aerospace Engineering", "Biomedical Engineering"], index=0)

        if st.session_state.pic_seeded:
            assets = asset_choices.get(domain)
            if assets:
                # Select asset to be used
                asset = st.selectbox("Asset", options=assets, index = 0)
        
        if st.session_state.unit_seeded:
            # vector_unit will be a tuple which can consider any selection needed to determine what units should be used
            # --- We might need more than one selectable unit in the future, and assets should affect this someday
            vector_unit = (unit)

            # Picks what choices for units are shown to the user based on other variables
            unit_choices = [u for types in unit_selector.get(vector_unit) for u in unit_types.get(types)]

            # Displays the Units selectbox
            unit_selection = st.selectbox("Units", options=unit_choices, index=0)

        st.divider()

        # Displays the Generate Problem button
        generate_prompt_clicked = st.form_submit_button("Generate problem", type="primary", use_container_width=True)

    # Displays the Generate Matrix button
    # --- Currently does nothing, will be added to later
    generate_matrix_clicked = st.button("Generate matrix", type="primary", use_container_width=True)

    pic_seeded = st.checkbox("Picture seeding", key = "pic_seeded")
    unit_seeded = st.checkbox("Unit seeding", key = "unit_seeded")

############################## Main Screen ##############################

# We will replace this when the matrix generator is useable. For now it loads in 1 of 2 random matrices in data/chapter2
matrix_name, matrix_path, MATRIX = load_random_matrix()

if matrix_name is not None:
    try:
        df = pd.read_csv(matrix_path)   
        st.subheader("Edit your data below:")
        edited_df = st.data_editor(df, num_rows="dynamic")
    except Exception as e:
        st.error(f"Error reading file: {e}")
    
    # --- The data_editor already has an option to download as csv, I'm not sure this is necessary
    #csv_bytes = edited_df.to_csv(index=False).encode("utf-8")

    # st.download_button(
    #     label="Download CSV",
    #     data=csv_bytes,
    #     file_name=matrix_name,
    #     mime="text/csv",
    #     use_container_width=True,
    # )

else:
    st.info("Please generate a matrix to start editing.")





# ---------- Generate Button Logic ----------
if generate_prompt_clicked:
    with st.spinner("Generating…"):
        st.session_state.problem = generate_problem(domain, unit, subtopic, injection, context, unit_selection, matrix_name, MATRIX)
        st.session_state.last_meta = {"domain": domain, "unit": unit, "subtopic": subtopic, "custom context": injection, "context": context, "velocity_units": unit_selection, "matrix_name": matrix_name, "MATRIX": MATRIX}

# ---------- Main output ----------
st.divider()

meta = st.session_state.last_meta
if meta:
    st.caption(f"**Selected:** {unit_dict[meta['unit']]} • {meta['subtopic']} — {subtopic_dict.get(meta['subtopic'], '')} • {meta['domain']}")

if st.session_state.problem:
    with st.container(border=True, width = 750):
        st.subheader("Generated Problem")
        st.markdown(st.session_state.problem)

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Regenerate", use_container_width=True):
                with st.spinner("Regenerating…"):
                    st.session_state.problem = generate_problem(domain, unit, subtopic, injection, context, unit_selection, matrix_name, MATRIX)
                    st.session_state.last_meta = {"domain": domain, "unit": unit, "subtopic": subtopic}
    # with st.container(border=False):
    #     with open("diagram_gen\index.html", "r", encoding="utf-8") as f:
    #         html_code = f.read()

    #     component.html(html_code)

else:
    st.info("Choose settings in the sidebar, then click **Generate problem**.")