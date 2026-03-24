import numpy as np
from . import vectors

def write_vector_matrix_to_csv_using_vector_array(vector_array, filepath):
    # loop through the vector array and convert each vector object to a list of its attributes, then write to csv file
    vector_matrix_text = []
    for vector in vector_array:
        # append the vector attributes to the vector data list in the order of the VECTOR_HEADERS list
        vector_data = vector.get_all_data_and_headers()
        current_vector_text = []
        for column_header in vectors.VECTOR_HEADERS:
            current_vector_text.append(vector_data[column_header])

        # convert the current vector data to a comma separated string and append to the vector matrix text list
        current_vector_text = ",".join(str(x) for x in current_vector_text)
        vector_matrix_text.append(current_vector_text)

    # write the vector matrix text to the csv file
    with open(filepath, "w") as f:
        f.write(",".join(vectors.VECTOR_HEADERS) + "\n")
        for line in vector_matrix_text:
            f.write(line + "\n")

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
vector_array = np.array([])
for i in range(5):
    vector_array = np.append(vector_array, vectors.generate_random_vector_3d())

for vector in vector_array:
    print(vector.get_all_data_and_headers())
write_vector_matrix_to_csv_using_vector_array(vector_array, "data/matrix_gen_output/test.csv")
