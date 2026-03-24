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
    # convert dataframe rows into Vector objects for now
    vector_array = []

    for _, row in df.iterrows():
        vec = vectors.Vector(
            row["x_component"],
            row["y_component"],
            row["x_location"],
            row["y_location"]
        )
        vector_array.append(vec)

    payload = {
        "vectors": df.to_dict(orient="records"),
        "computed": {}
    }

    # vector addition section
    if subtopic == "Vector Addition":
        print("made it here made it here")
        resultant = calculate_problem_solution.calculate_sum_of_vectors(vector_array)
        payload["computed"]["resultant"] = {
            "magnitude": round(resultant.get_magnitude(), 3),
            "direction": round(resultant.get_direction(), 3),
            "x_component": round(resultant.x_component, 3),
            "y_component": round(resultant.y_component, 3),
            "x_location": round(resultant.x_location, 3),
            "y_location": round(resultant.y_location, 3),
        }

    # Dot product
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