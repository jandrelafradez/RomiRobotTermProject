from array import array

class Centroid:
    def __init__(self,measurements):

        self.measurements = measurements
        # Creates sum variable for weighted sum
        self.weight_sum = 0
        # Creates an array of weights of the sensors
        self.weights = array('h',[-7,-5,-2,-1,1,2,5,7])

    def weighted_sum(self):

        self.weight_sum = 0
        # Loops through the measurements to determine a centroid of the sensor array
        for i,val in enumerate(self.measurements):
            # Add the value times the weight of the sensor to the centroid
            self.weight_sum += val * self.weights[i]
        # Return the centroid value
        return self.weight_sum





