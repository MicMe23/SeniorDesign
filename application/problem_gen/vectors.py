import random
import math
import numpy as np

MAGNITUDE_OF_COORD_RANGE = 10

def calculate_magnitude(x_component, y_component):
    return math.sqrt(x_component**2 + y_component**2)

def calculate_direction(x_component, y_component):
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
        theta = 270 + math.degrees(math.atan(-y_component/x_component))
    else:
        raise Exception(f"Error in vector direction calculation: x = {x_component}, y = {y_component}")
    return theta

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

def generate_random_vector():
    x_location = random.randint(-MAGNITUDE_OF_COORD_RANGE, MAGNITUDE_OF_COORD_RANGE)
    y_location = random.randint(-MAGNITUDE_OF_COORD_RANGE, MAGNITUDE_OF_COORD_RANGE)
        
    x_component = 0
    y_component = 0
    minimum_x_component, maximum_x_component, minimum_y_component, maximum_y_component = calculate_minimum_x_and_y_components(x_location, y_location)
    while x_component == 0 and y_component == 0:
        x_component = random.randint(minimum_x_component, maximum_x_component)
        y_component = random.randint(minimum_y_component, maximum_y_component)
   
    return Vector(x_component, y_component, x_location, y_location)

class Vector:
    # If initializing using magnitude, leave x and y component as 0, and if initializing using x and y component, leave magnitude as 0
    def __init__(self, x_component, y_component, x_location, y_location):
        self.x_component = x_component
        self.y_component = y_component
        self.x_location = x_location
        self.y_location = y_location

    def get_magnitude(self):
        return calculate_magnitude(self.x_component, self.y_component)
    
    def get_direction(self):
        return calculate_direction(self.x_component, self.y_component)
    

# # TEST TO GENERATE RANDOM VECTOR
# # --------------------------------------------------
# random_vector = generate_random_vector()
# print(f"Vector with magnitude {random_vector.get_magnitude():.3f}, direction {random_vector.get_direction():.3f}, x component {random_vector.x_component}, y component {random_vector.y_component}, x location {random_vector.x_location}, and y location {random_vector.y_location}")

    

    
