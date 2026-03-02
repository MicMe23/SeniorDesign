import numpy as np
import vectors

def write_vector_matrix_to_csv_using_vector_array(vector_array, filepath):
    headers = ["magnitude","x_component","y_component","direction","x_location","y_location"]

    # loop through the vector array and convert each vector object to a list of its attributes, then write to csv file
    vector_data = []
    for vector in vector_array:
        # append the vector attributes to the vector data list in the order of the headers. format to 3 decimal places for magnitude and direction
        vector_data.append([f"{vector.get_magnitude():.3f}", vector.x_component, vector.y_component, f"{vector.get_direction():.3f}", vector.x_location, vector.y_location])
    np.savetxt(filepath, vector_data, delimiter=",", fmt="%s", header=",".join(headers), comments='')

def get_vector_array_from_vector_matrix_from_csv(filepath):
    # read the csv file and convert each row to a vector object, then return an array of vector objects
    first_line = True
    with open(filepath, "r") as f:
        next(f) # skip header row
        for line in f:
            magnitude, x_component, y_component, direction, x_location, y_location = line.strip().split(",")
            if first_line:
                vector_array = np.array([vectors.Vector(float(x_component), float(y_component), float(x_location), float(y_location))])
                first_line = False
            else:
                vector_array = np.append(vector_array, vectors.Vector(float(x_component), float(y_component), float(x_location), float(y_location)))
    return vector_array

# vector_array = get_vector_array_from_vector_matrix_from_csv("data/matrix_gen_output/vector_matrix.csv")
# print(vector_array)
# for vector in vector_array:
#     print(f"Vector with magnitude {vector.get_magnitude():.3f}, direction {vector.get_direction():.3f}, x component {vector.x_component}, y component {vector.y_component}, x location {vector.x_location}, and y location {vector.y_location}")
# write_vector_matrix_to_csv_using_vector_array(vector_array, "data/matrix_gen_output/test.csv")
