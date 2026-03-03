import numpy as np
import math
import random
import vectors
import vector_matrix
import problem_metadata

# returns a vector object for the resultant vector of the vector addition problem
# the method will add all of the vectors in the array to get one resultant vector
def calculate_sum_of_vectors(vector_array):
    # add the x and y components of each vector in the vector array to get the x and y components of the resultant vector, then calculate the magnitude and direction of the resultant vector
    resultant_x_component = 0
    resultant_y_component = 0
    for vector in vector_array:
        resultant_x_component += vector.x_component
        resultant_y_component += vector.y_component
    resultant_vector = vectors.Vector(resultant_x_component, resultant_y_component, 0, 0)
    return resultant_vector

# # TEST TO CALCULATE SUM OF VECTORS
# # --------------------------------------------------
# vector_array = vector_matrix.get_vector_array_from_vector_matrix_from_csv("data/matrix_gen_output/vector_matrix.csv")
# resultant_vector = calculate_sum_of_vectors(vector_array)
# print(f"Resultant vector with magnitude {resultant_vector.get_magnitude():.3f}, direction {resultant_vector.get_direction():.3f}, x component {resultant_vector.x_component}, and y component {resultant_vector.y_component}")


# TEST TO CALCULATE SUM OF VECTORS WITH RANDOMLY GENERATED VECTOR ARRAY
# --------------------------------------------------
# problem = problem_metadata.ProblemMetadata("magnitude_and_direction", 3, "units")
# problem.set_vector_array_randomly()
# resultant_vector = calculate_sum_of_vectors(problem.vector_array)
# for vector in problem.vector_array:
#     print(f"Vector with magnitude {vector.get_magnitude():.3f}, direction {vector.get_direction():.3f}, x component {vector.x_component}, y component {vector.y_component}, x location {vector.x_location}, and y location {vector.y_location}")
# print(f"Resultant vector with magnitude {resultant_vector.get_magnitude():.3f}, direction {resultant_vector.get_direction():.3f}, x component {resultant_vector.x_component}, and y component {resultant_vector.y_component}")

# Calculates the dot product of two vectors using their x and y components, returns a scalar value
def calculate_dot_product_of_vectors(vector_1, vector_2):
    return vector_1.x_component * vector_2.x_component + vector_1.y_component * vector_2.y_component

# # TEST TO CALCULATE DOT PRODUCT OF VECTORS WITH RANDOMLY GENERATED VECTOR ARRAY
# # --------------------------------------------------
# problem = problem_metadata.ProblemMetadata("dot_product", 3, "units")
# problem.set_vector_array_randomly()
# dot_product = calculate_dot_product_of_vectors(problem.vector_array[0], problem.vector_array[1])
# for vector in problem.vector_array:
#     print(f"Vector with magnitude {vector.get_magnitude():.3f}, direction {vector.get_direction():.3f}, x component {vector.x_component}, y component {vector.y_component}, x location {vector.x_location}, and y location {vector.y_location}")
# print(f"Dot product of vector 1 and vector 2: {dot_product:.3f}")