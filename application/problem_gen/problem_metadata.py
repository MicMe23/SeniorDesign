import numpy as np
import math
import random
import pandas as pd
from . import vectors
from . import vector_matrix

class ProblemMetadata:
    def __init__(self, problem_type, number_of_vectors, units, scenario):
        self.problem_type = problem_type
        self.number_of_vectors = number_of_vectors
        self.vector_array = np.empty([]) # empty array to hold vector data, will be populated by generate_vector_matrix_with_n_vectors function
        self.units = units
        self.solution = None # should be a list of the correct answers to the problemg
        self.scenario = scenario # select a unique scenario for matrix gen (Ex soccer game)

    def set_vector_array_from_csv(self, csv_filepath):
        self.vector_array = vector_matrix.get_vector_array_from_vector_matrix_from_csv(csv_filepath)

    def set_vector_array_randomly(self):
        if self.scenario == "Soccer Match 2D":
            num_positive = math.ceil(self.number_of_vectors / 2)
            num_negative = self.number_of_vectors - num_positive

            directions = [1] * num_positive + [-1] * num_negative
            random.shuffle(directions)

            for i in range(self.number_of_vectors):
                random_vector = vectors.generate_random_vector_2d()

                # make directions realistic
                while True:
                    if directions[i] == 1:
                        if random_vector.x_component > 0 and abs(random_vector.x_component) > abs(random_vector.y_component):
                            break
                    else:
                        if random_vector.x_component < 0 and abs(random_vector.x_component) > abs(random_vector.y_component):
                            break

                    # regenerate until valid
                    random_vector = vectors.generate_random_vector_2d()
                
                # positions realistic to a real game
                if directions[i] == 1:
                    random_vector.x_location = random.randint(-11, -2)
                else:
                    random_vector.x_location = random.randint(2, 11)

                random_vector.y_location = random.randint(-10, 10)

                if i == 0:
                    self.vector_array = np.array([random_vector])
                else:
                    self.vector_array = np.append(self.vector_array, random_vector)

        elif self.scenario == "Aircraft Formation 2D":
            for i in range(self.number_of_vectors):
                random_vector = vectors.generate_random_vector_2d()

                while True:
                    # all aircraft move forward toward pos x
                    if random_vector.x_component > 0 and abs(random_vector.x_component) > abs(random_vector.y_component):
                        break

                    random_vector = vectors.generate_random_vector_2d()

                # closeish together
                random_vector.x_location = random.randint(-10, 10)
                random_vector.y_location = random.randint(-5, 5)

                if i == 0:
                    self.vector_array = np.array([random_vector])
                else:
                    self.vector_array = np.append(self.vector_array, random_vector)

        elif self.scenario == "Soccer Match 3D":
            num_positive = math.ceil(self.number_of_vectors / 2)
            num_negative = self.number_of_vectors - num_positive

            directions = [1] * num_positive + [-1] * num_negative
            random.shuffle(directions)

            for i in range(self.number_of_vectors):
                random_vector = vectors.generate_random_vector_3d()

                # make directions realistic
                while True:
                    if directions[i] == 1:
                        if random_vector.x_component > 0 and abs(random_vector.x_component) > abs(random_vector.y_component):
                            break
                    else:
                        if random_vector.x_component < 0 and abs(random_vector.x_component) > abs(random_vector.y_component):
                            break

                    # regenerate until valid
                    random_vector = vectors.generate_random_vector_3d()
                
                # positions realistic to a real game
                if directions[i] == 1:
                    random_vector.x_location = random.randint(-20, -5)
                    random_vector.z_location = random.randint(-20, -5)
                else:
                    random_vector.x_location = random.randint(5, 20)
                    random_vector.z_location = random.randint(5, 20)

                random_vector.y_location = random.randint(-10, 10)


                if i == 0:
                    self.vector_array = np.array([random_vector])
                else:
                    self.vector_array = np.append(self.vector_array, random_vector)

        elif self.scenario == "Aircraft Formation 3D":
            for i in range(self.number_of_vectors):
                random_vector = vectors.generate_random_vector_3d()

                while True:
                    # all aircraft move forward toward pos x
                    if random_vector.x_component > 0 and abs(random_vector.x_component) > abs(random_vector.y_component):
                        break

                    random_vector = vectors.generate_random_vector()

                # closeish together
                random_vector.x_location = random.randint(-10, 10)
                random_vector.y_location = random.randint(-5, 5)
                random_vector.z_location = random.randint(-5, 5)

                if i == 0:
                    self.vector_array = np.array([random_vector])
                else:
                    self.vector_array = np.append(self.vector_array, random_vector)            

        elif self.scenario == 'No Scenario 2D':
            for i in range(self.number_of_vectors):
                random_vector = vectors.generate_random_vector_2d()
                if i == 0:
                    self.vector_array = np.array([random_vector])
                else:
                    self.vector_array = np.append(self.vector_array, random_vector)

        elif self.scenario == 'No Scenario 3D':
            for i in range(self.number_of_vectors):
                random_vector = vectors.generate_random_vector_3d()
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