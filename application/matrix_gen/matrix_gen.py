import random
import math
import numpy as np

MAG_OF_COORD_RANGE = 10

NUMBER_OF_ROWS_IN_VECTOR_MATRIX = 5
VECTOR_NAME_ROW = 0
VECTOR_MAGNITUDE_ROW = 1
VECTOR_DIRECTION_ROW = 2
VECTOR_X_COORD_ROW = 3
VECTOR_Y_COORD_ROW = 4

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

# The following function generates a matrix of vectors for a magnitude and direction of n
# vectors problem where n, the number of vectors is passed through
def generate_vector_matrtix_with_n_vectors(n):
    vector_data = []
    
    for vector_num in range(n):
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

        vector_data.append([f"vector_{vector_num+1}", round(magnitude, 3), vx, vy, round(direction, 3), x, y])

    # Convert to numpy array and transpose
    vector_matrix = np.array(vector_data).T
    return vector_matrix

output = generate_vector_matrtix_with_n_vectors(3)
print(output)

# Export to csv file
def export_vector_matrix_to_csv(vector_matrix, filename):
    np.savetxt(filename, vector_matrix, delimiter=",", fmt="%s")

output_filepath = "data/matrix_gen_output/vector_matrix.csv"
export_vector_matrix_to_csv(output, output_filepath)