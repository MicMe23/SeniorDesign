import os
import random
from openai import OpenAI, OpenAIError

try:
    client = OpenAI() 
except:
    raise OpenAIError("No API key provided.")

def load_random_matrix():
    MATRIX_DIR = "data/chapter2"
    files = [f for f in os.listdir(MATRIX_DIR) if f.endswith(".csv")]
    if not files:
        raise RuntimeError("No matrix CSV files found.")
    chosen = random.choice(files)
    full_path = os.path.join(MATRIX_DIR, chosen)

    with open(full_path, "r", encoding="utf-8") as f:
        return chosen, full_path, f.read()

def generate_problem(domain, unit, subtopic, injection, context, velocity_units, matrix_name, MATRIX):

    SYSTEM = f"""
    You are generating a {domain}-themed engineering homework problem for Unit {unit}, Subtopic {subtopic}.


    DATA FORMAT (important):
    - The CSV matrix below has ONE HEADER ROW.
    - Each subsequent ROW represents ONE vector.
    - Columns are:
    magnitude, x_component, y_component, direction_deg, x_location, y_location

    RULES FOR USING THE DATA:
    - Treat the matrix values as authoritative. Do NOT compute new numbers.
    - x_location and y_location are only for where the vector is drawn from; do NOT hide them.
    - The vector represents velocity. Always refer to the velcity in {velocity_units} per second

    HIDDEN VARIABLES:
    - Choose exactly ONE unknown per vector row.
    - The unknown MUST be one of: magnitude, x_component, y_component, direction_deg.
    - Replace the chosen numeric value in the displayed matrix with a variable name (e.g., A_mag, Bx, theta_C).
    - Do NOT reveal the hidden numeric value anywhere in the problem statement.

    RESULTANT / OPERATION RULES:
    - Some problems require vector operations (e.g., addition/subtraction, dot product, cross product).
    - When the backend provides an operation result, it will appear as a row labeled type = RESULTANT.
    - Treat RESULTANT rows as GIVEN values produced by the backend. Do NOT compute or verify them.
    - When a RESULTANT row exists:
    - Write the problem so students are asked to compute/identify the resultant of the specified operation
        using the GIVEN vectors, and then compare to / report the RESULTANT vector provided.
    - Do NOT hide values inside RESULTANT rows unless the subtopic explicitly requires solving for a missing
        resultant attribute (in that case, hide at most ONE value in the RESULTANT row).
    - When no RESULTANT row exists:
    - Generate an "independent vectors" style problem: hide exactly ONE value per GIVEN vector row.

    STUDENT TASKS WHEN RESULTANT EXISTS:
    - Ask students to compute the resultant using vector operations and show their work.
    - Ask students to report the resultant in component form and/or magnitude-angle form.
    - The provided RESULTANT row is for answer checking; do not compute it in the solution key.

    SOLUTION KEY RULES:
    - The Solution Key section is for hidden matrix values or rows labeled as resultant.
    - Only output: variable = number or vector (the original hidden numbers or vectors from the matrix).

    PROBLEM REQUIREMENTS:
    - The story and questions must match Subtopic {subtopic} strictly (Unit {unit} scope).
    - Use only Chapter-appropriate vector concepts (components, direction, magnitude, vector addition, dot/cross only if the subtopic is dot/cross).
    - Provide 1-2 clear student tasks/questions.
    - Keep the scenario consistent with {domain}.

    TONE CONTROL:
    - User context: {injection}
    - Style: {context}
    - If style is "short": write a straightforward homework problem (3–6 sentences).
    - If style is "creative": write a richer scenario (8–12 sentences) but keep the math unchanged.

    Display Matrix:
    - Include a labeled "Vector" column first.
    - Use this exact column order:
    Vector | Magnitude | Direction (deg) | X-Component | Y-Component | X-Location | Y-Location
    - Align columns using fixed-width spacing.
    - Preserve original decimal formatting.

    OUTPUT FORMAT (strict):
    1) Title (one line)
    2) Scenario + questions
    3) A neatly formatted matrix following Display Matrix section
    4) A final section titled exactly: "Solution Key"
    5) Under "Solution Key", output ONLY lines in this exact form:
    variable = number

    for 2D coordinate system and vector problems there is no resulting vector, just solving for variables in vectors. 
    Do NOT include any other solution steps. Do NOT calculate any answers. Use the original hidden numbers from the matrix.
    """

    resp = client.responses.create(
        model="gpt-5-mini",
        input=[
            {"role": "system", "content": SYSTEM},
        {"role": "user", "content": f"Domain: {domain}\nUnit: {unit}\nSubtopic: {subtopic}\nMatrix:\n{MATRIX}"}
        ],
    )

#     return resp.output_text.strip()
