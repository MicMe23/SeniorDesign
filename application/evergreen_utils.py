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
from application.problem_gen import calculate_problem_solution
from application.problem_gen import problem_metadata

def build_llm_payload(df, subtopic):
    vector_array = []

    # normalize headers just in case
    df = df.copy()
    df.columns = df.columns.str.strip()

    # fill missing z columns with 0 so uploaded 2D CSVs still work
    if "z_component" not in df.columns:
        df["z_component"] = 0
    if "z_location" not in df.columns:
        df["z_location"] = 0

    # if all z values are 0, assume 2D
    is_2d = (
        (df["z_component"].astype(float) == 0).all() and
        (df["z_location"].astype(float) == 0).all()
    )

    for _, row in df.iterrows():
        if is_2d:
            vec = vectors.Vector(
                2,
                float(row["x_component"]),
                float(row["y_component"]),
                0,
                float(row["x_location"]),
                float(row["y_location"]),
                0
            )
        else:
            vec = vectors.Vector(
                3,
                float(row["x_component"]),
                float(row["y_component"]),
                float(row["z_component"]),
                float(row["x_location"]),
                float(row["y_location"]),
                float(row["z_location"])
            )

        vector_array.append(vec)

    payload = {
        "vectors": df.to_dict(orient="records"),
        "computed": {}
    }

    if subtopic == "Vector Addition":
        resultant = calculate_problem_solution.calculate_sum_of_vectors(vector_array)
        payload["computed"]["resultant"] = {
            "magnitude": round(resultant.get_magnitude(), 3),
            "direction": resultant.get_direction(),
            "x_component": round(resultant.x_component, 3),
            "y_component": round(resultant.y_component, 3),
            "z_component": round(resultant.z_component, 3),
            "x_location": round(resultant.x_location, 3),
            "y_location": round(resultant.y_location, 3),
            "z_location": round(resultant.z_location, 3),
        }

    elif subtopic == "Dot Product":
        if len(vector_array) < 2:
            raise ValueError("Dot product problems require at least 2 vectors.")

        dot_val = calculate_problem_solution.calculate_dot_product_of_vectors(
            vector_array[0], vector_array[1]
        )

        payload["computed"]["dot_product"] = {
            "vector_1_index": 0,
            "vector_2_index": 1,
            "value": round(dot_val, 3)
        }

    return payload