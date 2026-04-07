import random
import math
import numpy as np
import pandas as pd

MAGNITUDE_OF_COORD_RANGE = 10
VECTOR_HEADERS_2D = ["magnitude", "x_component", "y_component", "direction", "x_location", "y_location"]
VECTOR_HEADERS_3D = ["magnitude", "x_component", "y_component", "z_component", "direction", "x_location", "y_location", "z_location"]
DEFAULT_Z_VALUES_IN_2D = 0

#convert a vector to a dataframe for the csv display and to be in payload for llm
def vectors_to_df(vector_array, dimension_mode) -> pd.DataFrame:
    rows = []
    for v in vector_array:
        direction = v.get_direction()

        if dimension_mode == "2D":
            rows.append({
                "magnitude": round(v.get_magnitude(), 3),
                "x_component": float(v.x_component),
                "y_component": float(v.y_component),
                "direction": round(direction, 3),
                "x_location": float(v.x_location),
                "y_location": float(v.y_location),
            })
        else:
            theta = round(direction[0], 3)
            phi = round(direction[1], 3)
            outstring = f"({theta}, {phi})"

            rows.append({
                "magnitude": round(v.get_magnitude(), 3),
                "x_component": float(v.x_component),
                "y_component": float(v.y_component),
                "z_component": float(v.z_component),
                "direction": outstring,
                "x_location": float(v.x_location),
                "y_location": float(v.y_location),
                "z_location": float(v.z_location)
            })
    if dimension_mode == "2D":
        return pd.DataFrame(rows, columns=VECTOR_HEADERS_2D)
    else:
        return pd.DataFrame(rows, columns=VECTOR_HEADERS_3D)

# finally convert to a list of dicts for the LLM
def df_to_matrix_payload(df: pd.DataFrame):
    return df[VECTOR_HEADERS].to_dict(orient="records")

def calculate_magnitude(x_component, y_component, z_component):
    return math.sqrt(x_component**2 + y_component**2 + z_component**2)

def calculate_direction_2d(x_component, y_component):
    # cases where components are 0 to avoid division by 0 error in atan function
    if x_component == 0 and y_component > 0:
        return 90
    elif x_component == 0 and y_component < 0:
        return 270
    elif x_component > 0 and y_component == 0:
        return 0
    elif x_component < 0 and y_component == 0:
        return 180
    
    # calculate direction using atan function and adjust based on quadrant of the vector, using the positive x axis as 0 degrees
    if x_component >= 0 and y_component >= 0:
        theta = math.degrees(math.atan(y_component/x_component))
    elif x_component <= 0 and y_component >= 0:
        theta = 90 + math.degrees(math.atan(-x_component/y_component))
    elif x_component <= 0 and y_component <= 0:
        theta = 180 + math.degrees(math.atan(y_component/x_component))
    elif x_component >= 0 and y_component <= 0:
        theta = 360 + math.degrees(math.atan(y_component/x_component))
    else:
        raise Exception(f"Error in vector direction calculation: x = {x_component}, y = {y_component}")
    return theta

# calculate the direction of the vector in 3D space using spherical coordinates, with the positive x axis as 0 degrees and the positive z axis as 90 degrees
def calculate_direction_3d(x_component, y_component, z_component):
    # calculate the direction of the vector in 3D space using spherical coordinates, with the positive x axis as 0 degrees and the positive z axis as 90 degrees
    r = calculate_magnitude(x_component, y_component, z_component)
    if r == 0:
        raise Exception("Cannot calculate direction of a zero vector.")
    theta = calculate_direction_2d(x_component, y_component)
    phi = math.degrees(math.acos(z_component/r))
    return theta, phi

def calculate_vector_components(magnitude, direction):
    x_component = magnitude * math.cos(math.radians(direction))
    y_component = magnitude * math.sin(math.radians(direction))
    return x_component, y_component

def calculate_minimum_x_and_y_components(x_location, y_location):
    minimum_x_component = -MAGNITUDE_OF_COORD_RANGE - x_location
    maximum_x_component = MAGNITUDE_OF_COORD_RANGE - x_location

    minimum_y_component = -MAGNITUDE_OF_COORD_RANGE - y_location
    maximum_y_component = MAGNITUDE_OF_COORD_RANGE - y_location
    return minimum_x_component, maximum_x_component, minimum_y_component, maximum_y_component

def generate_random_vector_2d():
    x_location = random.randint(-MAGNITUDE_OF_COORD_RANGE, MAGNITUDE_OF_COORD_RANGE)
    y_location = random.randint(-MAGNITUDE_OF_COORD_RANGE, MAGNITUDE_OF_COORD_RANGE)
        
    x_component = 0
    y_component = 0
    minimum_x_component, maximum_x_component, minimum_y_component, maximum_y_component = calculate_minimum_x_and_y_components(x_location, y_location)
    while x_component == 0 and y_component == 0:
        x_component = random.randint(minimum_x_component, maximum_x_component)
        y_component = random.randint(minimum_y_component, maximum_y_component)
   
    return Vector(2, x_component, y_component, DEFAULT_Z_VALUES_IN_2D, x_location, y_location, DEFAULT_Z_VALUES_IN_2D)

def generate_random_vector_3d():
    random_vector = generate_random_vector_2d()
    
    z_location = random.randint(-MAGNITUDE_OF_COORD_RANGE, MAGNITUDE_OF_COORD_RANGE)
    z_component = 0
    while z_component == 0:
        z_component = random.randint(-MAGNITUDE_OF_COORD_RANGE, MAGNITUDE_OF_COORD_RANGE)

    return Vector(3, random_vector.x_component, random_vector.y_component, z_component, random_vector.x_location, random_vector.y_location, z_location)

def vector_is_in_2_dimensions(vector):
    return vector.number_of_dimensions == 2

class Vector:
    # Initializes a vector object with x, y, and z components and x, y, and z locations
    def __init__(self, number_of_dimensions, x_component, y_component, z_component, x_location, y_location, z_location):
        self.number_of_dimensions = number_of_dimensions
        self.x_component = x_component
        self.y_component = y_component
        self.x_location = x_location
        self.y_location = y_location

        if vector_is_in_2_dimensions(self):
            self.z_component = DEFAULT_Z_VALUES_IN_2D
            self.z_location = DEFAULT_Z_VALUES_IN_2D
        else: 
            self.z_component = z_component
            self.z_location = z_location

    def get_magnitude(self):
        if vector_is_in_2_dimensions(self):
            return calculate_magnitude(self.x_component, self.y_component, 0)
        else:
            return calculate_magnitude(self.x_component, self.y_component, self.z_component)
    
    def get_direction(self):
        if vector_is_in_2_dimensions(self):
            # Returns a single value, theta, which is the angle in the xy plane from the positive x axis, with counterclockwise being positive and clockwise being negative
            return calculate_direction_2d(self.x_component, self.y_component)
        else:
            # Returns two values, theta and phi in degrees formatted as (theta, phi), where theta is the angle in the xy plane from the positive x axis and phi is the angle from the positive z axis
            return calculate_direction_3d(self.x_component, self.y_component, self.z_component)
        
    def get_all_data_and_headers(self):
        if vector_is_in_2_dimensions(self):
            return {
                "magnitude": self.get_magnitude(),
                "x_component": self.x_component,
                "y_component": self.y_component,
                "direction": self.get_direction(),
                "x_location": self.x_location,
                "y_location": self.y_location
            }

        else:
            return {
                "magnitude": self.get_magnitude(),
                "x_component": self.x_component,
                "y_component": self.y_component,
                "z_component": self.z_component,
                "direction": self.get_direction(),
                "x_location": self.x_location,
                "y_location": self.y_location,
                "z_location": self.z_location
            }

# TEST TO GENERATE RANDOM VECTOR IN 2D
# --------------------------------------------------
# random_vector = generate_random_vector_2d()
# print(random_vector.get_all_data_and_headers())

# # TEST TO GENERATE RANDOM VECTOR IN 3D
# # --------------------------------------------------
# random_vector_3d = generate_random_vector_3d()
# print(random_vector_3d.get_all_data_and_headers())
