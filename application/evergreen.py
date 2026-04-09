# streamlit
import streamlit as st
import streamlit.components.v1 as component

import base64

# data formatting
import pandas as pd
import numpy as np

# utilities
import random
import math
import json
from pathlib import Path
from io import BytesIO

# PDF stuff
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# project modules
from problem_gen import vectors
import evergreen_utils

from problem_gen import vector_matrix
from problem_gen import problem_metadata
from problem_gen import calculate_problem_solution

from evergreen_utils import *

# api and model code
from test_api import *
from model import *

############################## UI prep ##############################

st.set_page_config(page_title="Evergreen Classroom", page_icon="🌲", layout="wide")

# Keep the main content slightly narrower than full screen width.
page_col1, page_col2, page_col3 = st.columns([1, 10, 1])

def make_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# make a file named problem_metadata in the application directory which stores entry (dictionary)
def save_problem_log(entry, filename="problem_metadata.json"):
    log_path = Path(__file__).parent/filename
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(entry, f, indent=4)

with page_col2:
    # Load and display centered logo
    with open("application/assets/streamlit-app/Evergreen Classroom Logo-01.png", "rb") as f:
        logo_data = base64.b64encode(f.read()).decode()
    st.markdown(f"<div style='text-align: center;'><img src='data:image/png;base64,{logo_data}' width='300'></div>", unsafe_allow_html=True)
    
    # st.title("Evergreen Classroom")

# --- Subtopic selector ---
# Connect subsection numbers to their corresponding titles
subtopic_list = [
    "Coordinate System & Vectors",
    "Unit Vectors",
    "Vector Addition",
    "Dot Product",
    "Cross Products",

    "4. Moment of Force",
    "4. Scalar Addition of Moments",
    "4. Varignon's Theorem",
    "4. 3D Moments",
    "4. Couples",
    "4. Equivalent Transformations",
    "4. Statically Equivalent Systems"
]

scenario_dimension = {
    "2D": ["No Scenario", "Soccer Match", "Aircraft Formation"],
    "3D": ["No Scenario", "Soccer Match", "Aircraft Formation"]
}

# --- Context selector ---
# Connect a selectbox choice to its description
context = {
    "Basic": "short/simple context",
    "Creative": "long/creative context"
}

asset_choices = {
    "Generic": ["No Image", "Just the arrow", "Plane (seen from the side)", "Person (seen from above)", "Car (seen from above)", "Placeholder"],
    "Aerospace Engineering": ["No Image","Just the arrow", "Plane (seen from the side)"],
    "Biomedical Engineering": ["No Image","Just the arrow", "Person (seen from above)"]
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

# Asset to img
img_selector = {
    "Plane (seen from the side)": "application/assets/aerospace/f16_clipart_cropped.png",
    "Person (seen from above)": "application/assets/bme/man_running.png",
    "Car (seen from above)": "application/assets/mechanical/red_f1_car.png",
    "Placeholder": "application/assets/Placeholder.png",
    "Just the arrow": "application/assets/Empty.png"
}

# init session states
if "problem" not in st.session_state:
    st.session_state.problem = ""
if "last_meta" not in st.session_state:
    st.session_state.last_meta = None
if "matrix_df" not in st.session_state:
    st.session_state.matrix_df = None
if "matrix_name" not in st.session_state:
    st.session_state.matrix_name = None
if "dimension_mode" not in st.session_state:
    st.session_state.dimension_mode = "2D"
if "matrix_payload" not in st.session_state:
    st.session_state.matrix_payload = None
if "uploaded_csv_name" not in st.session_state:
    st.session_state.uploaded_csv_name = None


with page_col2:
    st.divider()
    ################ Section 1: Problem settings #################
    st.header("Problem Settings")

    settings_col1, settings_col2 = st.columns(2)

    with settings_col1:
        subtopic = st.selectbox("Topic", options=subtopic_list, index=0)

    with settings_col2:
        context = st.selectbox("Level of Detail", options=context)

    with settings_col1:
        domain = st.selectbox("Major", options=["Generic", "Aerospace Engineering", "Biomedical Engineering"], index=0)

    with settings_col2:
        image_info = st.selectbox("Image", options=asset_choices[domain], index=0)

    settings_col5, settings_col6 = st.columns(2)

    with settings_col5:
        unit_type = st.selectbox("Unit Type", options=list(unit_types.keys()), index=0)

    with settings_col6:
        velocity_unit = st.selectbox("Exact Unit", options=unit_types[unit_type], index=0)

    injection = st.text_input("Custom context (1 - 2 sentences)")
    tasks = st.text_area("Task list (number tasks if you have specific tasks in mind)", value=None, height=240)
    st.divider()

    st.header("Matrix Gen")
    # Displays the Generate Matrix controls
    # number of vectors for generated matrix
    num_vectors = st.number_input("Number of vectors", min_value=1, max_value=10, value=3, step=1)

    dimension_mode = st.selectbox("Dimension", options=["2D", "3D"], index=0)
    st.session_state.dimension_mode = dimension_mode

    selected_scenario = st.selectbox("Scenario", options=scenario_dimension[dimension_mode], index=0)
    
    uploaded_csv = st.file_uploader(
        "Upload a CSV matrix",
        type=["csv"],
        help="Upload a CSV to load directly into the matrix editor."
    )
    generate_matrix_clicked = st.button("Generate Matrix", type="primary", use_container_width=True)

    if generate_matrix_clicked:
        pm = problem_metadata.ProblemMetadata(
            problem_type=subtopic,
            number_of_vectors=int(num_vectors),
            units=velocity_unit,
            scenario=selected_scenario,
            dimension_mode=dimension_mode,
        )
        pm.set_vector_array_randomly()
        st.session_state.matrix_df = vectors.vectors_to_df(pm.vector_array, dimension_mode=dimension_mode)
        st.session_state.matrix_name = f"generated_{int(num_vectors)}_vectors"
        st.rerun()

    EXPECTED_COLUMNS = [
        "magnitude",
        "x_component",
        "y_component",
        "z_component",
        "direction",
        "x_location",
        "y_location",
        "z_location"
    ]

    if uploaded_csv is not None and st.session_state.uploaded_csv_name != uploaded_csv.name:
        try:
            uploaded_df = pd.read_csv(uploaded_csv)

            # remove accidental spaces in headers
            uploaded_df.columns = uploaded_df.columns.str.strip()

            # keep only the columns you care about, in the right order
            uploaded_df = uploaded_df[EXPECTED_COLUMNS]

            st.session_state.matrix_df = uploaded_df
            st.session_state.matrix_name = uploaded_csv.name
            st.session_state.uploaded_csv_name = uploaded_csv.name

            st.success(f"Loaded CSV: {uploaded_csv.name}")

        except Exception as e:
            st.error(f"Could not read uploaded CSV: {e}. Make sure your csv uses the correct fileds for the matrix.")

    # ---------------- csv editor ----------------
    if st.session_state.matrix_df is not None:
        with st.container(border=True):
            st.subheader("Edit your data below:")
            edited_df = st.data_editor(
                st.session_state.matrix_df,
                num_rows="dynamic",
                key="matrix_editor",
            )
            col1, col2 = st.columns(2)

            with col1:
                if st.button("Apply Edits", use_container_width=True):
                    st.session_state.matrix_df = edited_df
                    st.rerun()

            with col2:
                if st.button("Recalculate Magnitude / Direction", use_container_width=True):
                    st.session_state.matrix_df = recalculate_matrix_df(edited_df)
                    st.rerun()
    else:
        st.info("Please generate a matrix to start editing.")
    st.divider()

    # Displays the Generate Problem button
    generate_prompt_clicked = st.button("Generate Problem", type="primary", use_container_width=True)

    st.divider()

    # ---------- Generate Button Logic ----------
    if generate_prompt_clicked:
        if generate_prompt_clicked:
            if st.session_state.matrix_df is None:
                st.warning("Please generate a matrix first.")
            else:

                st.session_state.matrix_df.to_csv('data/matrix_gen_output/vector_matrix.csv', index=False)
                #building the payload to be injested by the LLM
                st.session_state.matrix_payload = evergreen_utils.build_llm_payload(st.session_state.matrix_df, subtopic, st.session_state.dimension_mode)

                log_entry = {
                "domain": domain,
                "subtopic": subtopic,
                "custom_context": injection,
                "level_of_detail": context,
                "unit_type": unit_type,
                "velocity_unit": velocity_unit,
                "matrix_name": st.session_state.matrix_name,
                "matrix_payload": st.session_state.matrix_payload,
                "tasks": tasks,
                "dimension_mode": dimension_mode
                }

                save_problem_log(log_entry)

                with st.spinner("Generating…"):
                    st.session_state.problem = generate_problem(
                        domain,
                        subtopic,
                        image_info,
                        injection,
                        context,
                        velocity_unit,
                        st.session_state.matrix_name,
                        st.session_state.matrix_payload,
                        tasks,
                        dimension_mode
                    )

                    st.session_state.last_meta = log_entry

    meta = st.session_state.last_meta
    if meta:
        st.caption(f"**Selected:** {meta['subtopic']} • {meta['domain']}")

    if st.session_state.problem:
        with st.container(border=False, width = 1000):
            st.subheader("Generated Problem")
            st.markdown(st.session_state.problem)

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Regenerate", use_container_width=True):
                with st.spinner("Regenerating…"):
                    st.session_state.problem = generate_problem(domain, subtopic, image_info, injection, context, velocity_unit, st.session_state.matrix_name, st.session_state.matrix_payload, tasks, dimension_mode)
                    st.session_state.last_meta = {
            "domain": domain,
            "subtopic": subtopic,
            "custom_context": injection,
            "level_of_detail": context,
            "unit_type": unit_type,
            "velocity_unit": velocity_unit,
            "matrix_name": st.session_state.matrix_name,
            "matrix_payload": st.session_state.matrix_payload,
            "tasks": tasks,
            "dimension_mode": dimension_mode
            }       

        if image_info != "No Image":
            # Generate the base64 version of the selected image to then turn it into a form
            # javascript can read inline.
            b64_img = make_base64(img_selector.get(image_info, "null"))
            js_img = f'"data:image/png;base64,{b64_img}"'

            # Read in unedited html and js files to run inline
            with open("application\diagram_gen\index.html", "r") as html:
                html_code = html.read()
                html.close()
            with open("application\diagram_gen\js\main.js", "r") as main:
                html_main = main.read()
                main.close()
            with open("application\diagram_gen\js\cartesianGraph.js", "r") as graph:
                html_graph = graph.read()
                graph.close()

            # Read in the csv to inject it into the html when it runs
            df = pd.read_csv("data/matrix_gen_output/vector_matrix.csv")
            csvInj = df.to_csv(index=False)
                
            # Make all scripts inline and inject all changes that come from outside the html file: csv, image, other html files
            html_code = html_code.replace('<script src="js/cartesianGraph.js"></script>', f'<script>{html_graph}</script>')
            html_code = html_code.replace('<script src="js/main.js"></script>', f'<script> let injection = `{csvInj}`; let img = {js_img};</script><script>{html_main}</script>')

            # Debug. Shows what the component.html is receiving
            #st.code(html_code[:-2000])
            
        # Make all scripts inline and inject all changes that come from outside the html file: csv, image, other html files
        html_code = html_code.replace('<script src="js/cartesianGraph.js"></script>', f'<script>{html_graph}</script>')
        html_code = html_code.replace('<script src="js/main.js"></script>', f'<script> let injection = `{csvInj}`; let img = {js_img};</script><script>{html_main}</script>')
        html_code = html_code.replace("<body>", '<body style="margin:0; overflow:hidden;">')

        # Debug. Shows what the component.html is receiving
        #st.code(html_code[:-2000])

        # Match component frame height to the rendered 1000x1000 SVG so no internal scroll is needed.
        component.html(html_code, height=1008, scrolling=False)

    else:
        st.info("Choose settings then click **Generate problem**.")