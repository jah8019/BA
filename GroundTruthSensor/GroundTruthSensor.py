import carla
from cupshelpers import setPPDPageSize

class GroundTruthSensor():

    def __init__(self, world, ego_vehicle, stages):
        self.world = world
        self.ego_vehilce = ego_vehicle
        self.stages = stages

    def tick(self):
        ground_truth_actors = self.world.get_actors()
        z = []
        for actor in ground_truth_actors:
            if(self.check_actor(actor)):
                z.append(actor)
        return z
    
    def check_actor(self, actor):
        if actor.id is self.ego_vehilce.id:
            return False
        if actor.type_id == 'spectator':
            return False
        for stage in self.stages:
            if not stage.check_stage(actor, self):
                return False
        print(actor.type_id, " dedected")
        self.draw_arrow_from_ego(actor)
        return True
    
    def draw_arrow_from_ego(self, actor):
        actors_location = actor.get_location()
        ego_location = self.ego_vehilce.get_location() 
        self.world.debug.draw_arrow(ego_location, actors_location, life_time=0.1)