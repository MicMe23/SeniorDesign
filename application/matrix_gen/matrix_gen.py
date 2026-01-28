import random
import math
import numpy as np

MAG_OF_COORD_RANGE = 10

NUMBER_OF_ROWS_IN_FORCE_MATRIX = 5
FORCE_NAME_ROW = 0
FORCE_MAGNITUDE_ROW = 1
FORCE_DIRECTION_ROW = 2
FORCE_X_COORD_ROW = 3
FORCE_Y_COORD_ROW = 4

# helper function to calculate scalar magnitude using x and y component of the vector
def calculate_vector_magnitude(vx, vy):
    return math.sqrt((vx**2) + (vy**2))

# Helper function to calculate direction of vector using x and y component of the vector,
# the x and y coordinate of the vector, and using the positive x axis as 0 degrees
def calculate_vector_direction(vx, vy):
    if vx >= 0 and vy >= 0:
        theta = math.degrees(math.atan(vy/vx))
    elif vx <= 0 and vy >= 0:
        theta = 90 + math.degrees(math.atan(-vx/vy))
    elif vx <= 0 and vy <= 0:
        theta = 180 + math.degrees(math.atan(vy/vx))
    elif vx >= 0 and vy <= 0:
        theta = 270 + math.degrees(math.atan(-vy/vx))
    else:
        raise Exception(f"Error in vector direction calculation: x = {vx}, y = {vy}")
    return theta

# The following function generates a matrix of forces for a magnitude and direction of n
# vectors problem where n, the number of vectors is passed through
def generate_force_matrtix_with_n_vectors(n):
    force_data = []
    
    for force_num in range(n):
        x = random.randint(-MAG_OF_COORD_RANGE, MAG_OF_COORD_RANGE)
        y = random.randint(-MAG_OF_COORD_RANGE, MAG_OF_COORD_RANGE)
        
        vx = 0
        vy = 0
        while vx == 0:
            vx = random.randint(-MAG_OF_COORD_RANGE - x, MAG_OF_COORD_RANGE - x)
        while vy == 0:
            vy = random.randint(-MAG_OF_COORD_RANGE - y, MAG_OF_COORD_RANGE - y)

        magnitude = calculate_vector_magnitude(vx, vy)
        direction = calculate_vector_direction(vx, vy)

        force_data.append([f"force_{force_num+1}", magnitude, direction, x, y])

    # Convert to numpy array and transpose
    force_matrix = np.array(force_data).T
    return force_matrix

# format to three decimal places for readability
# force_matrix = 
print(generate_force_matrtix_with_n_vectors(3))
