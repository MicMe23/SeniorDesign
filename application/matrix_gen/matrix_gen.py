import random
import math

MAG_OF_COORD_RANGE = 10
NUMBER_OF_ROWS_IN_FORCE_MATRIX = 5

# helper function to calculate scalar magnitude using x and y component of the vector
def calculate_vector_magnitude(vx, vy):
    return math.sqrt((vx**2) + (vy**2))

# Helper function to calculate direction of vector using x and y component of the vector,
# the x and y coordinate of the vector, and using the positive x axis as 0 degrees
def calculate_vector_direction(x,y):
    if x >= 0 and y >= 0:
        # Quadrant 1
        theta = 0
    elif x <= 0 and y >= 0:
        # Quadrant 2
        theta = 90
    elif x <= 0 and y <= 0:
        # Quadrant 3
        theta = 90
    elif x >= 0 and y <= 0:
        # Quadrant 4
    else:
        raise Exception(f"Error in vector direction calculation: x = {x}, y = {y}")

# The following function generates a matrix of forces for a maginitude and direction of n
# vectors problem where n, the number of vectors is passed through
def generate_force_matrtix_with_n_vectors(n):
    # Create an empty force matrix with enough columns for the forces
    force_matrix = [[0] * n] * NUMBER_OF_ROWS_IN_FORCE_MATRIX
    print(force_matrix)
    for force_num in range(n):
        # Generate a random x and y coordinate which cannot be the same number
        x = random.randint(-MAG_OF_COORD_RANGE, MAG_OF_COORD_RANGE)
        y = random.randint(-MAG_OF_COORD_RANGE, MAG_OF_COORD_RANGE)
        while y == x:
            y = random.randint(-MAG_OF_COORD_RANGE, MAG_OF_COORD_RANGE)
    
        #
        

generate_force_matrtix_with_n_vectors(20)