import os
import random
from openai import OpenAI

client = OpenAI() 

MATRIX_DIR = "data/chapter2"

def load_random_matrix():
    files = [f for f in os.listdir(MATRIX_DIR) if f.endswith(".csv")]
    if not files:
        raise RuntimeError("No matrix CSV files found.")
    chosen = random.choice(files)
    with open(os.path.join(MATRIX_DIR, chosen), "r") as f:
        return chosen, f.read()

domain = "Dungeons and Dragons"

def generate_problem(domain, unit, subtopic):

    SYSTEM = f"""You generate an {domain}-themed {unit} homework problem.
    The problem should be related to {subtopic}
    Columns are vectors; rows, in top to bottom order, are magnitude, angle counter clockwise from positvie x, x_direction, y_direction.
    Pick exactly ONE unknown per vector by replacing its number with a variable, remember the number to use in solution.
    At the very end of the response, say what the unknown variables equal.
    Return ONLY the final problem text and the solution at the end (no JSON).
    The solution should only be (variable) = (number) for each hidden value.
    Do not caclculate the answer, use the number stored from earlier for consistency.
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
