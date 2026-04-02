# streamlit
import streamlit as st
import streamlit.components.v1 as component

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
from application.problem_gen import vectors
from application import evergreen_utils

from application.problem_gen import vector_matrix
from application.problem_gen import problem_metadata
from application.problem_gen import calculate_problem_solution

from application.evergreen_utils import *

# api and model code
from application.test_api import *
from application.model import *

############################## UI prep ##############################

Page_col1, page_col2, page_col3 = st.columns([1,2,1])

# make a file named problem_metadata in the application directory which stores entry (dictionary)
def save_problem_log(entry, filename="problem_metadata.json"):
    log_path = Path(__file__).parent/filename
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(entry, f, indent=4)

with page_col2:
    st.set_page_config(page_title="Evergreen Classroom", page_icon="🌲", layout="wide")
    st.title("Evergreen Classroom")

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

scenario = [
    "No Scenario 2D",
    "No Scenario 3D",
    "Soccer Match 2D",
    "Soccer Match 3D",
    "Aircraft Formation 2D",
    "Aircraft Formation 3D"
]

# --- Context selector ---
# Connect a selectbox choice to its description
context = {
    "Basic": "short/simple context",
    "Creative": "long/creative context"
}

asset_choices = {
    "Generic": ["No Image", "Just the arrow", "F16 (seen from the side)", "Person (seen from above)", "F1 Car (seen from above)"],
    "Aerospace Engineering": ["No Image","Just the arrow", "F16 (seen from the side)"],
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

# init session states
if "problem" not in st.session_state:
    st.session_state.problem = ""
if "last_meta" not in st.session_state:
    st.session_state.last_meta = None
if "matrix_df" not in st.session_state:
    st.session_state.matrix_df = None
if "matrix_name" not in st.session_state:
    st.session_state.matrix_name = None
with page_col2:
    st.divider()
    ################ Section 1: Problem settings #################
    st.header("Problem Settings")

    col1, col2 = st.columns([1,1])

    with col1:
        subtopic = st.selectbox("Topic", options=subtopic_list, index=0)

    with col2:
        context = st.selectbox("Level of Detail", options=context)

    with col1:
        domain = st.selectbox("Major", options=["Generic", "Aerospace Engineering", "Biomedical Engineering"], index=0)

    with col2:
        image_info = st.selectbox("Image", options=asset_choices[domain], index=0)

    with col1:
        unit_type = st.selectbox("Unit Type", options=list(unit_types.keys()), index=0)

    with col2:
        velocity_unit = st.selectbox("Exact Unit", options=unit_types[unit_type], index=0)

    injection = st.text_input("Custom context (1 - 2 scentences)")
    tasks = st.text_area("Task list: number tasks if you have specific tasks in mind", value=None, height=300 )
    st.divider()

    st.header("Matrix Gen")
    # Displays the Generate Matrix button
    # number of vectors for generated matrix
    num_vectors = st.number_input("Number of vectors", min_value=1, max_value=10, value=3, step=1)
    selected_scenario = st.selectbox("Scenario", options=scenario)
    uploaded_csv = st.file_uploader(
        "Upload a CSV matrix",
        type=["csv"],
        help="Upload a CSV to load directly into the matrix editor."
    )
    generate_matrix_clicked = st.button("Generate Matrix", type="primary", use_container_width=True)

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

    if uploaded_csv is not None:
        try:
            uploaded_df = pd.read_csv(uploaded_csv)

            # remove accidental spaces in headers
            uploaded_df.columns = uploaded_df.columns.str.strip()

            missing_cols = [col for col in EXPECTED_COLUMNS if col not in uploaded_df.columns]
            if missing_cols:
                st.error(f"Uploaded CSV is missing required columns: {missing_cols}")
            else:
                # keep only the columns you care about, in the right order
                uploaded_df = uploaded_df[EXPECTED_COLUMNS]

                st.session_state.matrix_df = uploaded_df
                st.session_state.matrix_name = uploaded_csv.name

                st.success(f"Loaded CSV: {uploaded_csv.name}")

        except Exception as e:
            st.error(f"Could not read uploaded CSV: {e}")

    # ---------------- csv editor ----------------
    if st.session_state.matrix_df is not None:
        with st.container(border=True, width = 750):
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

            with col2:
                if st.button("Recalculate Magnitude / Direction", use_container_width=True):
                    st.session_state.matrix_df = recalculate_matrix_df(edited_df)
    else:
        st.info("Please generate a matrix to start editing.")
    st.divider()

    # Displays the Generate Problem button
    generate_prompt_clicked = st.button("Generate Problem", type="primary", use_container_width=True)

    st.divider()

    # ---------------- Matrix generation ----------------
    if generate_matrix_clicked:
        # Create a new matrix
        pm = problem_metadata.ProblemMetadata(
            problem_type = subtopic,
            number_of_vectors=int(num_vectors),
            units = velocity_unit,
            scenario = selected_scenario
        )
        pm.set_vector_array_randomly()

        # Convert to DataFrame for the editor and LLM
        st.session_state.matrix_df = vectors.vectors_to_df(pm.vector_array)

        # debug line
        st.session_state.matrix_name = f"generated_{int(num_vectors)}_vectors"


    # ---------- Generate Button Logic ----------
    if generate_prompt_clicked:
        if generate_prompt_clicked:
            if st.session_state.matrix_df is None:
                st.warning("Please generate a matrix first.")
            else:

                st.session_state.matrix_df.to_csv('data/matrix_gen_output/vector_matrix.csv', index=False)
                #building the payload to be injested by the LLM
                matrix_payload = evergreen_utils.build_llm_payload(st.session_state.matrix_df, subtopic, )

                log_entry = {
                "domain": domain,
                "subtopic": subtopic,
                "custom_context": injection,
                "level_of_detail": context,
                "unit_type": unit_type,
                "velocity_unit": velocity_unit,
                "matrix_name": st.session_state.matrix_name,
                "matrix_payload": matrix_payload,
                "tasks": tasks
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
                        matrix_payload,
                        tasks
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
                        st.session_state.problem = generate_problem(domain, subtopic, image_info, injection, context, velocity_unit, st.session_state.matrix_name, matrix_payload, tasks)
                        st.session_state.last_meta = {
                "domain": domain,
                "subtopic": subtopic,
                "custom_context": injection,
                "level_of_detail": context,
                "unit_type": unit_type,
                "velocity_unit": velocity_unit,
                "matrix_name": st.session_state.matrix_name,
                "matrix_payload": matrix_payload,
                "tasks": tasks
                }
        # with st.container(border=False):
        #     with open("diagram_gen\index.html", "r", encoding="utf-8") as f:
        #         html_code = f.read()

        #     component.html(html_code)

    else:
        st.info("Choose settings then click **Generate problem**.")