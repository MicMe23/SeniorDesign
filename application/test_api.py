import os
import random
from openai import OpenAI, OpenAIError

try:
    client = OpenAI() 
except:
    raise OpenAIError("No API key provided.")

MATRIX_DIR = "data/chapter2"

def load_random_matrix():
    files = [f for f in os.listdir(MATRIX_DIR) if f.endswith(".csv")]
    if not files:
        raise RuntimeError("No matrix CSV files found.")
    chosen = random.choice(files)
    with open(os.path.join(MATRIX_DIR, chosen), "r") as f:
        return chosen, f.read()

def generate_problem(domain, unit, subtopic, injection, context):

    SYSTEM = f"""You generate an {domain}-themed {unit} homework problem.
    The problem should be related to {subtopic}
    Rows are individual planes; columns are magnitude, angle counter clockwise from positvie x, x_coordinate (for graph), y_coordinate (for graph), force_x_direction, force_y_direction.
    Pick 1-2 numbers in each vector by replacing it's number with a variable, remember the number to use in solution.
    Do not pick x_coordinate or y_coordinate as an unkown variable. Only choose from magnitude, force_x_direction, force_y_direction.
    Make sure to ensure that the hidden variables are solvable.
    Format the matrix nice for the output. Label rows.
    At the very end of the response, say what the unknown variables equal.
    Return ONLY the final problem text and the solution at the end (no JSON).
    The solution should only be (variable) = (number) for each hidden value.
    Do not caclculate the answer, use the number stored from earlier for consistency.
    context added by user ({injection}).
    Make the question more {context}. If short, make it a basic straight-foreward homework problem. If creative, then make the question about a paragraph and give the numbers a colorful story.
    """

    matrix_name, MATRIX = load_random_matrix()

    resp = client.responses.create(
        model="gpt-5-mini",
        input=[
            {"role": "system", "content": SYSTEM},
        {   "role": "user", "content": f"Domain: {matrix_name}\nMatrix:\n{MATRIX}"}
        ],
    )

    return resp.output_text.strip()
