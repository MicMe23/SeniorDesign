import numpy as np
from . import vectors

def write_vector_matrix_to_csv_using_vector_array(vector_array, filepath):
    # loop through the vector array and convert each vector object to a list of its attributes, then write to csv file
    vector_matrix_text = []
    csv_headers = vector_array[0].get_all_data_and_headers().keys()
    current_vector_text = []
    for vector in vector_array:
        # append the vector attributes to the vector data list
        vector_data = vector.get_all_data_and_headers()
        for column_header in csv_headers:
            current_vector_text.append(vector_data[column_header])

        # convert the current vector data to a comma separated string and append to the vector matrix text list
        current_line = ",".join(str(x) for x in current_vector_text)
        vector_matrix_text.append(current_line)
        current_vector_text = []

    # write the vector matrix text to the csv file
    with open(filepath, "w") as f:
        f.write(",".join(csv_headers) + "\n")
        for line in vector_matrix_text:
            f.write(line + "\n")

def get_vector_array_from_vector_matrix_from_csv(filepath):
    # read the csv file and convert each row to a vector object, then return an array of vector objects
    with open(filepath, "r") as f:
        lines = f.readlines()
        csv_headers = lines[0].strip().split(",")
        vector_array = np.array([])

        # Check if 2d or 3d by checking if z_component or z_location are headers or if the z_component and z_location columns are all 0
        # if either are true, then we can assume the vectors are 2d and set the z_component and z_location to 0 when creating the vector objects
        is_2d = False
        if "z_component" not in csv_headers or "z_location" not in csv_headers:
            is_2d = True
        else:
            z_component_index = csv_headers.index("z_component")
            z_location_index = csv_headers.index("z_location")
            is_2d = all(line.strip().split(",")[z_component_index] == "0" and line.strip().split(",")[z_location_index] == "0" for line in lines[1:])

        if is_2d:
            for line in lines[1:]:
                vector_data = line.strip().split(",")
                vector_dict = dict(zip(csv_headers, vector_data))
                vector_array = np.append(vector_array, vectors.Vector(2, float(vector_dict["x_component"]), float(vector_dict["y_component"]), 0, float(vector_dict["x_location"]), float(vector_dict["y_location"]), 0))
        else:
            for line in lines[1:]:
                vector_data = line.strip().split(",")
                # direction should be a list of 2 values for 3d vectors, so we need to convert it back to a list if it is a string
                # by combining the indices with a ( and then with the ) together (should be next to each other)
                if "direction" in csv_headers:
                    direction_index = csv_headers.index("direction")
                    direction_value = [float(vector_data[direction_index].strip("(")), float(vector_data[direction_index + 1].strip(")"))]
                    # print(f"Direction value: {direction_value}")
                    # replace the direction value in the vector data with the list of 2 values
                    vector_data[direction_index] = direction_value
                    # remove the next value in the vector data since it is part of the direction value
                    vector_data.pop(direction_index + 1)
                else:
                    raise Exception(f"Error in direction format for 3d vector: {vector_data[direction_index]}")
                vector_dict = dict(zip(csv_headers, vector_data))
                # direction should be a list of 2 values for 3d vectors, so we need to convert it back to a list if it is a string
                vector_array = np.append(vector_array, vectors.Vector(3, float(vector_dict["x_component"]), float(vector_dict["y_component"]), float(vector_dict["z_component"]), float(vector_dict["x_location"]), float(vector_dict["y_location"]), float(vector_dict["z_location"])))

    return vector_array

# vector_array = get_vector_array_from_vector_matrix_from_csv("data/matrix_gen_output/2d_test.csv")
# for vector in vector_array:
#     print(vector.get_all_data_and_headers())

# TEST TO WRITE 2D VECTOR MATRIX TO CSV
# vector_array = np.array([])
# for i in range(5):
#     vector_array = np.append(vector_array, vectors.generate_random_vector_2d())

# for vector in vector_array:
#     print(vector.get_all_data_and_headers())
# write_vector_matrix_to_csv_using_vector_array(vector_array, "data/matrix_gen_output/2d_test.csv")

# TEST TO WRITE 3D VECTOR MATRIX TO CSV
# vector_array = np.array([])
# for i in range(5):
#     vector_array = np.append(vector_array, vectors.generate_random_vector_3d())

# for vector in vector_array:
#     print(vector.get_all_data_and_headers())
# write_vector_matrix_to_csv_using_vector_array(vector_array, "data/matrix_gen_output/3d_test.csv")

