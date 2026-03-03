import numpy as np
import math
import random
import pandas as pd
import vectors
import vector_matrix

class ProblemMetadata:
    def __init__(self, problem_type, number_of_vectors, units):
        self.problem_type = problem_type
        self.number_of_vectors = number_of_vectors
        self.vector_array = np.empty([]) # empty array to hold vector data, will be populated by generate_vector_matrix_with_n_vectors function
        self.units = units
        self.solution = None # should be a list of the correct answers to the problem

    def set_vector_array_from_csv(self, csv_filepath):
        self.vector_array = vector_matrix.get_vector_array_from_vector_matrix_from_csv(csv_filepath)

    def set_vector_array_randomly(self):
        for i in range(self.number_of_vectors):
            random_vector = vectors.generate_random_vector()
            if i == 0:
                self.vector_array = np.array([random_vector])
            else:
                self.vector_array = np.append(self.vector_array, random_vector)

# TEST TO SET VECTOR ARRAY FROM CSV FILE
# --------------------------------------------------
# csv_filepath = "data/matrix_gen_output/vector_matrix.csv"
# problem = ProblemMetadata("magnitude_and_direction", 3)
# problem.set_vectors_from_csv(csv_filepath)

# for vector in problem.vector_array:
#     print(f"Vector with magnitude {vector.get_magnitude():.3f}, direction {vector.get_direction():.3f}, x component {vector.x_component}, y component {vector.y_component}, x location {vector.x_location}, and y location {vector.y_location}")


# # TEST TO SET VECTOR ARRAY RANDOMLY
# # --------------------------------------------------
# problem = ProblemMetadata("magnitude_and_direction", 3, "units")
# problem.set_vector_array_randomly()
# print(problem.vector_array)
# for vector in problem.vector_array:
#     print(f"Vector with magnitude {vector.get_magnitude():.3f}, direction {vector.get_direction():.3f}, x component {vector.x_component}, y component {vector.y_component}, x location {vector.x_location}, and y location {vector.y_location}")