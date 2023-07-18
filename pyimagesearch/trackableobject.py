import numpy as np

class TrackableObject:
    def __init__(self, objectID, centroid):

        self.objectID = objectID
        self.centroid = [centroid]

        self.timestamp = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
        self.position = {'A': None, 'B': None, 'C': None, 'D': None}
        self.lastPoint = False
        
        # intialize the object speeds in MPH and KMPH
        self.speedMPH = None,
        self.speedKMPH = None,

        #intialize two booleans 1.objects speed has already been estimated or not, and 2.objects speed has been logged or not
        self.estimated = False,
        self.logged = False,

        #intialize the direction of the object
        self.direction = None

    def calculate_speed(self, estimatedSpeed):
        #calculate speed in kmph and mph
        self.speedKMPH = np.average(estimatedSpeed)
        miles_per_one_kilometer = 0.621371
        self.speedMPH = self.speedKMPH * miles_per_one_kilometer

        
        


