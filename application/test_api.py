import os
import random
from openai import OpenAI, OpenAIError

try:
    client = OpenAI() 
except:
    raise OpenAIError("No API key provided.")

def generate_problem(domain, topic, image_info, injection, context, velocity_units, matrix_name, MATRIX):

    SYSTEM = f"""
    You are generating a {domain}-themed engineering homework problem for topic {topic}.

    DATA FORMAT:
    - The CSV matrix below has ONE HEADER ROW.
    - Each subsequent ROW represents ONE vector.
    - Columns are:
    magnitude, x_component, y_component, direction_deg, x_location, y_location

    GENERAL RULES:
    - Treat all matrix values as authoritative.
    - Do NOT compute new numbers.
    - x_location and y_location are only for graph placement; never hide them.
    - The vector quantity uses units of {velocity_units}.
    - Preserve original numeric values exactly.
    - Do not invent new numbers.
    - Do not provide worked solutions.

    PROBLEM MODE RULES:
    There are three possible problem modes.

    1) independent_vectors
    - Use this mode for subtopics where students solve for missing attributes of individual vectors.
    - Hide exactly ONE value in each GIVEN vector row.
    - The hidden value must be one of:
    magnitude, x_component, y_component, direction_deg
    - Do NOT hide x_location or y_location.
    - Do NOT hide more than one value per vector row.

    2) resultant_vector
    - Use this mode for vector addition problems.
    - GIVEN vectors should remain fully visible.
    - A backend-provided resultant vector is included as a row labeled RESULTANT.
    - Hide values ONLY in the RESULTANT row.
    - Hide 1 to 2 values in the RESULTANT row only.
    - Do NOT hide values in any GIVEN vector row.
    - Students should be asked to compute the resultant from the visible GIVEN vectors and solve for the hidden RESULTANT values.
    - Do not ask students to verify backend math beyond using the provided resultant row.

    3) dot_product
    - Use this mode for dot product problems.
    - GIVEN vectors should remain fully visible.
    - If the backend provides a dot product result, hide only the scalar dot product value or one clearly identified attribute related to the backend-computed result.
    - Do NOT hide values in the GIVEN vectors unless explicitly instructed otherwise.
    - Students should be asked to compute the dot product using the visible vectors.

    MODE SELECTION:
    - If the user message says Problem mode: independent_vectors, follow only the independent_vectors rules.
    - If the user message says Problem mode: resultant_vector, follow only the resultant_vector rules.
    - If the user message says Problem mode: dot_product, follow only the dot_product rules.

    STORY AND TASK REQUIREMENTS:
    - The story must match Subtopic {topic} strictly.
    - Provide 1 to 2 clear student tasks.
    - Keep the scenario consistent with {domain}.
    - User context: {injection}
    - Style: {context}

    IMAGE GROUNDING RULES (MANDATORY)

    The scenario must visually match the selected image asset, but the text should NEVER mention that an image exists.

    Selected asset: {image_info}

    MODE 1 — No Image Selected
    If the selected asset is "No Image":
    - You may create any appropriate engineering scenario.
    - Be creative and choose a realistic physical situation related to the selected domain and topic.
    - Do NOT write phrases like "No image is provided" or "imagine an image".
    - Simply write the scenario naturally.

    MODE 2 — Specific Image Selected
    If a specific image asset is selected:

    1. The scenario must be about the subject shown in the image.
    2. The first sentence must clearly describe that subject.
    3. Do NOT substitute related objects.
    4. Do NOT generalize to the broader field.
    5. Do NOT place the scenario inside systems not visible in the image.
    6. Each vector must correspond to one separate visible object matching the subject.

    Examples:
    Plane image → multiple aircraft moving or experiencing forces  
    Person image → multiple people walking, pushing, lifting, or moving

    Forbidden substitutions:
    Plane image → UAVs, drones, missiles, satellites  
    Person image → blood vessels, organs, cells, internal anatomy

    CRITICAL RULE:
    The scenario text must NEVER say that an image exists or refer to the image directly.
    The image is only a constraint for the story, not part of the story.
    
    STYLE RULES:
    - If style is Basic, write a short straightforward homework problem.
    - If style is Creative, write a richer scenario, but do not change the math.

    FORMAT REQUIREMENTS:

    Return the problem formatted in clean Markdown using the following structure:

    ## Title

    ### Scenario

    ### Tasks
    1. Task description
    2. Task description

    ### Data Table
    Use a proper Markdown table with headers:
    | Vector | Magnitude | Direction (deg) | X-Component | Y-Component | X-Location | Y-Location |
    |--------|-----------|-----------------|-------------|-------------|------------|------------|
    | ...    | ...       | ...             | ...         | ...         | ...        | ...        |

    ### Solution Key
    for solutions, make a new line every for every variable like this,
    V1_magnitude = 10.77 new line
    V2_x_component = 2.0 new line
    V3_direction_deg = 315.0 new line

    OUTPUT FORMAT:
    1) Title
    2) Scenario and question(s)
    3) Formatted matrix
    4) A final section titled exactly: Solution Key
    5) Under Solution Key, output only lines in the form:
    variable = number

    Do not include any other solution steps.
"""

    resp = client.responses.create(
        model="gpt-5-mini",
        input=[
            {"role": "system", "content": SYSTEM},
        {"role": "user", "content": f"Domain: {domain}\nMatrix:\n{MATRIX}"}
        ],
    )

    return resp.output_text.strip()
