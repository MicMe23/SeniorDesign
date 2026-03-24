import numpy as np
import math
import random
from . import vectors
from . import vector_matrix
from . import problem_metadata

# returns a vector object for the resultant vector of the vector addition problem
# the method will add all of the vectors in the array to get one resultant vectord
def calculate_sum_of_vectors(vector_array):
    # add the x, y, z components of each vector in the vector array to get the x, y, z components of the resultant vector, then calculate the magnitude and direction of the resultant vector
    resultant_x_component = 0
    resultant_y_component = 0
    resultant_z_component = 0

    # check if the vectors are in 2d or 3d by checking the number of dimensions in each vector, if any vector has 3 dimensions, 
    # then we can assume all vectors are in 3d and we need to add the z components, otherwise we can assume all vectors are in 2d and we can ignore the z components
    resultant_is_in_2d = True
    for vector in vector_array:
        if vector.number_of_dimensions == 3:
            resultant_is_in_2d = False
        resultant_x_component += vector.x_component
        resultant_y_component += vector.y_component
        resultant_z_component += vector.z_component

    # Initialize the resultant vector object with the calculated x, y, z components and 0 for the location since we are only interested in the magnitude and direction of the resultant vector
    if resultant_is_in_2d:
        resultant_z_component = 0
        resultant_vector = vectors.Vector(2, resultant_x_component, resultant_y_component, resultant_z_component, 0, 0, 0)
    else:
        resultant_vector = vectors.Vector(3, resultant_x_component, resultant_y_component, resultant_z_component, 0, 0, 0)

    return resultant_vector

# # TEST TO CALCULATE SUM OF VECTORS 2D VECTOR ARRAY FROM CSV
# # --------------------------------------------------
# vector_array = vector_matrix.get_vector_array_from_vector_matrix_from_csv("data/matrix_gen_output/2d_test.csv")
# resultant_vector = calculate_sum_of_vectors(vector_array)
# for vector in vector_array:
#     print(vector.get_all_data_and_headers())
# print("resultant: \n {0}".format(resultant_vector.get_all_data_and_headers()))

# TEST TO CALCULATE SUM OF VECTORS 3D VECTOR ARRAY FROM CSV
# --------------------------------------------------
# vector_array = vector_matrix.get_vector_array_from_vector_matrix_from_csv("data/matrix_gen_output/3d_test.csv")
# resultant_vector = calculate_sum_of_vectors(vector_array)
# for vector in vector_array:
#     print(vector.get_all_data_and_headers())
# print("resultant: \n {0}".format(resultant_vector.get_all_data_and_headers()))


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
    # Raise an exception if the vectors have different number of dimensions since we cannot calculate the dot product of vectors with different number of dimensions
    if vector_1.number_of_dimensions != vector_2.number_of_dimensions:
        raise Exception("Error: cannot calculate dot product of vectors with different number of dimensions")
    
    # If the vectors are in 3d, we need to include the z components in the calculation, otherwise we can ignore the z components since they will be 0 for 2d vectors
    if vector_1.number_of_dimensions == 3:
        return vector_1.x_component * vector_2.x_component + vector_1.y_component * vector_2.y_component + vector_1.z_component * vector_2.z_component
    else:
        return vector_1.x_component * vector_2.x_component + vector_1.y_component * vector_2.y_component

# # TEST TO CALCULATE DOT PRODUCT OF VECTORS WITH RANDOMLY GENERATED VECTOR ARRAY
# # --------------------------------------------------
# problem = problem_metadata.ProblemMetadata("dot_product", 3, "units")
# problem.set_vector_array_randomly()
# dot_product = calculate_dot_product_of_vectors(problem.vector_array[0], problem.vector_array[1])
# for vector in problem.vector_array:
#     print(f"Vector with magnitude {vector.get_magnitude():.3f}, direction {vector.get_direction():.3f}, x component {vector.x_component}, y component {vector.y_component}, x location {vector.x_location}, and y location {vector.y_location}")
# print(f"Dot product of vector 1 and vector 2: {dot_product:.3f}")

# # TEST TO CALCULATE DOT PRODUCT OF VECTORS WITH VECTOR ARRAY FROM CSV 2D
# # --------------------------------------------------
# vector_array = vector_matrix.get_vector_array_from_vector_matrix_from_csv("data/matrix_gen_output/2d_test.csv")
# dot_product = calculate_dot_product_of_vectors(vector_array[0], vector_array[1])
# print(vector_array[0].get_all_data_and_headers())
# print(vector_array[1].get_all_data_and_headers())
# print(f"Dot product of vector 1 and vector 2: {dot_product:.3f}")

# # TEST TO CALCULATE DOT PRODUCT OF VECTORS WITH VECTOR ARRAY FROM CSV 3D
# # --------------------------------------------------
# vector_array = vector_matrix.get_vector_array_from_vector_matrix_from_csv("data/matrix_gen_output/3d_test.csv")
# dot_product = calculate_dot_product_of_vectors(vector_array[0], vector_array[1])
# print(vector_array[0].get_all_data_and_headers())
# print(vector_array[1].get_all_data_and_headers())
# print(f"Dot product of vector 1 and vector 2: {dot_product:.3f}")
