import os
import random
from openai import OpenAI, OpenAIError

try:
    client = OpenAI() 
except:
    raise OpenAIError("No API key provided.")

def generate_problem(domain, topic, image_info, injection, context, velocity_units, matrix_name, MATRIX, tasks):

    SYSTEM = f"""
You are generating a {domain}-themed engineering homework problem for topic {topic}.

DIMENSION RULES:
- The problem may be either 2D or 3D.
- If all z_component values and all z_location values are 0, treat the problem as 2D.
- If any z_component or z_location value is nonzero, treat the problem as 3D.
- Do not convert a 3D problem into 2D.
- Do not ignore z-component or z-location in a 3D problem.

DATA FORMAT:
- The CSV matrix below has ONE HEADER ROW.
- Each subsequent ROW represents ONE vector.
- Possible columns are:
magnitude, x_component, y_component, z_component, direction, x_location, y_location, z_location
- In 2D problems, z_component and z_location may be 0 for all rows.
- In 3D problems, z_component and z_location must be treated as meaningful values.

DIRECTION RULES:
- In 2D, direction is a single angle in degrees measured from the positive x-axis in the xy-plane.
  1. direction: the angle in the xy-plane
- In 3D, direction should be described using two angles:
  1. theta: the angle in the xy-plane from the positive x-axis
  2. phi: the second direction angle returned by the backend
- Do not collapse a 3D direction into one angle.

GENERAL RULES:
- Treat all matrix values as authoritative.
- Do NOT compute new numbers.
- x_location, y_location, and z_location are only for graph placement; never hide them unless explicitly instructed.
- The vector quantity uses units of {velocity_units}.
- Preserve original numeric values exactly.
- Do not invent new numbers.
- Do not provide worked solutions.

PROBLEM MODE RULES:
There are three possible problem modes.

1) independent_vectors
- Use this mode for subtopics where students solve for missing attributes of individual vectors.
- Do NOT hide x_location, y_location, or z_location.
- Do NOT hide more than one value per vector row unless tasks explicitly require a whole vector to be hidden.
- In 2D, the hidden value may be one of:
  magnitude, x_component, y_component, direction
- In 3D, the hidden value may be one of:
  magnitude, x_component, y_component, z_component, theata, phi

2) resultant_vector
- Use this mode for vector addition problems.
- A backend-provided resultant vector is included as a row labeled RESULTANT.
- For 2D resultants, use magnitude, one direction angle, and x/y componenets.
- For 3D resultants, use magnitude and the direction pair (theata, phi), plus x/y/z components when appropriate.

3) dot_product
- Use this mode for dot product problems.
- GIVEN vectors should remain fully visible.
- If the backend provides a dot product result, hide only the scalar dot product value or one clearly identified attribute related to the backend-computed result.
- Do NOT hide values in the GIVEN vectors unless explicitly instructed otherwise.
- Students should compute the dot product using the visible vectors.

MODE SELECTION:
- If the user message says Problem mode: independent_vectors, follow only the independent_vectors rules.
- If the user message says Problem mode: resultant_vector, follow only the resultant_vector rules.
- If the user message says Problem mode: dot_product, follow only the dot_product rules.

STORY AND TASK REQUIREMENTS:
- The story must match Subtopic {topic} strictly.
- Provide 1 to 2 clear student tasks (if none are provided).
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
F16 image → multiple aircraft moving or experiencing forces
Person image → multiple people walking, pushing, lifting, or moving

Forbidden substitutions:
F16 image → UAVs, drones, missiles, satellites
Person image → blood vessels, organs, cells, internal anatomy

CRITICAL RULE:
- The scenario text must NEVER say that an image exists or refer to the image directly.
- The image is only a constraint for the story, not part of the story.

STYLE RULES:
- If style is Basic, write a short straightforward homework problem.
- If style is Creative, write a richer scenario, but do not change the math.

TASKS SECTION:
Tasks are {tasks}
- If tasks are None or empty, choose 1 to 2 tasks for the student as normal.
- If tasks are present, print them word for word in the Tasks section.
- If a task says to solve a specific feature of a vector, then hide that vector's feature in the matrix.
- If the task says to solve for a whole vector, then hide the whole row of solvable information for that vector.
- Never try to solve a task for the user.

FORMAT REQUIREMENTS:
Return the problem formatted in clean Markdown using the following structure:

## Title

### Scenario

### Tasks
1. Task description
2. Task description

### Data Table
- If the problem is 2D, use this header:
| Vector | Magnitude | Direction (deg) | X-Component | Y-Component | X-Location | Y-Location |
|--------|-----------|-----------------|-------------|-------------|------------|------------|
| ...    | ...       | ...             | ...         | ...         | ...        | ...        |

- If the problem is 3D, use this header:
| Vector | Magnitude | Theata (deg) | Phi (deg) | X-Component | Y-Component | Z-Component | X-Location | Y-Location | Z-Location |
|--------|-----------|---------------|-----------|-------------|-------------|-------------|------------|------------|------------|
| ...    | ...       | ...           | ...       | ...         | ...         | ...         | ...        | ...        | ...        |

### Solution Key
For solutions, put each variable on its own line like this:
V1_magnitude = 10.77
V2_x_component = 2.0
V3_direction_deg = 315.0

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
