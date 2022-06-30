import math
import numpy

class Range_Resolution_Stage:
    def __init__(self, resolution):
        self.resolution = resolution

    def check_stage(self, actor, sensor):
        distance = actor.distance
        if actor.distance_set is False:
            distance = self.calculate_distance(actor, sensor)
        max_offset = (self.resolution / 360) * 2 * math.pi * distance
        offset = numpy.random.normal(0, max_offset)
        location = actor.get_location()
        actor.location.x = location.x + offset
        actor.location.y = location.y + offset
        return True

    def calculate_distance(self, actor, sensor):
        sensor_location = sensor.ego_vehicle.location
        actor_location = actor.location
        return self.get_euklidian_distance(sensor_location, actor_location)
        
    def get_euklidian_distance(self, sensor_location, location):
        value = self.square(sensor_location.x - location.x) + self.square(sensor_location.y - location.y) + self.square(sensor_location.z - location.z)
        distance_to_vehicle = math.sqrt(value)
        return distance_to_vehicle