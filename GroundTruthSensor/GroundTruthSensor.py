import carla
from cupshelpers import setPPDPageSize


class GroundTruthSensor():

    fov_right_vector = None
    fov_left_vector = None

    def __init__(self, distance, world, ego_vehicle, fov, stages):
        self.distance = distance
        self.world = world
        self.ego_vehilce = ego_vehicle
        self.fov = fov
        self.stages = stages

    def tick(self):
        actors = self.world.get_actors()
        for actor in actors:
            self.check_actor(actor)  
    
    def check_actor(self, actor):
        if actor.id is self.ego_vehilce.id:
            return False
        for stage in self.stages:
            if not stage.check_stage(self=stage, actor=actor, sensor=self):
                return False
        print(actor.type_id, " dedected")
        self.draw_arrow_from_ego(actor)
        return True
    
    def draw_arrow_from_ego(self, actor):
        actors_location = actor.get_location()
        ego_location = self.ego_vehilce.get_location() 
        self.world.debug.draw_arrow(ego_location, actors_location, life_time=0.1)