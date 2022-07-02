from copy import copy
import time
import dill as pickle
from unittest import result
from joblib import Parallel, delayed

def check_actor_all_stages(actors, ego_vehicle, stages):
    z = []
    for actor in actors:
        if actor.id is ego_vehicle.id:
            continue
        if actor.type_id == 'spectator':
            continue
        for stage in stages:
            if not stage.check_stage(actor, ego_vehicle):
                break
            z.append(actor)
    return z

class GroundTruthSensor():

    def __init__(self, ego_vehicle, stages):
        self.ego_vehicle = ego_vehicle
        self.stages = stages
        self.z = []
        self.f = open("Time_Stages.txt", "a", buffering=1)
        self.f.write("-----------start")
    
    def tick(self, ground_truth_actors, ego_vehicle):
        self.ego_vehicle = ego_vehicle
        x = ground_truth_actors
        half = int(len(x)/2)
        x_first = x[half:]
        x_second = x[:half]
        x_full = [x_first, x_second]
        self.z = []
        stages_array = [copy(self.stages)]
        ego_vehicle_array = [copy(ego_vehicle)]
        result = Parallel(n_jobs=2)(delayed(check_actor_all_stages)(actor, ego_vehicle, stages) for actor in x_full for ego_vehicle in ego_vehicle_array for stages in stages_array) 
        result1 = result[0]
        result2 = result[1]
        if result1 is not None and result2 is not None:
            z = result1 + result2
        if result1 is not None and result2 is None:
            z = result1
        if result2 is not None and result1 is None:
            z = result2
        self.z = z
        # for actor in x:
        #     self.check_actor_all_stages(actor)
        return self.z

    # def tick(self, ground_truth_actors):
    #     x = ground_truth_actors.copy()
    #     z = []
    #     id = 0
    #     for stage in self.stages:
    #         start_time = time.time()
    #         stages = [stage]
    #         z = Parallel(n_jobs=1, backend="threading")(delayed(self.check_actor)(actor, stage) for actor in x for stage in stages)
    #         # for actor in x:
    #         #     if(self.check_actor(actor, stage) is not None):
    #         #         z.append(actor)
    #         x = []
    #         for elem in z:
    #             if elem is not None:
    #                 x.append(elem)
    #         z = []   
    #         self.f.write("Stage: " + str(id) + " time:" + str(time.time() - start_time) + "\n")
    #         id = id + 1
    #     return x

    def check_actor(self, actor, stage):
        if actor.id is self.ego_vehilce.id:
            return
        if actor.type_id == 'spectator':
            return
        if not stage.check_stage(actor, self):
            return
        return actor

    def close(self):
        self.f.close()