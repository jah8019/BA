import math

class Distance_Stage():

    def __init__(self, distance):
        self.distance = distance

    def square(self, number_to_square):
        return number_to_square * number_to_square

    def get_euklidian_distance(self, sensor_location, location):
        value = self.square(sensor_location.x - location.x) + self.square(sensor_location.y - location.y) + self.square(sensor_location.z - location.z)
        distance_to_vehicle = math.sqrt(value)
        return distance_to_vehicle

    def check_stage(self, actor, sensor):
        actors_location = actor.get_location()
        ego_location = sensor.ego_vehilce.get_location() 
        distance_to_vehicle = self.get_euklidian_distance(ego_location, actors_location)
        actor.distance = distance_to_vehicle
        actor.distance_set = True
        if distance_to_vehicle <= self.distance:
            return True
        else:
            return False

