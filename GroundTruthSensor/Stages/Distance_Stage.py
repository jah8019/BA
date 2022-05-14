class Distance_Stage():

    def __init__(self):
        pass

    def check_stage(self, actor, sensor):
        actors_location = actor.get_location()
        ego_location = sensor.ego_vehilce.get_location() 
        distance_to_vehicle = actors_location.distance(ego_location)
        if distance_to_vehicle <= sensor.distance:
            return True
        else:
            return False
