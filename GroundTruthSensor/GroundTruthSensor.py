from copy import copy
from functools import partial
from multiprocessing import Pool
import time
import dill as pickle
from joblib import Parallel, delayed

class GroundTruthSensor():

    def __init__(self, ego_vehicle, stages):
        self.ego_vehicle = ego_vehicle
        self.stages = stages
        self.z = []
    
    def tick(self, ground_truth_actors, ego_vehicle):
        self.ego_vehicle = ego_vehicle
        x = ground_truth_actors
        z = []
        for stage in self.stages:
            for actor in x:
                if actor.id is ego_vehicle.id:
                    continue
                if actor.type_id == 'spectator':
                    continue
                if stage.check_stage(actor, ego_vehicle):
                    z.append(actor)
            x = z
            z = []
        self.z = x
        return self.z

    def plot(self, test_id, sensor_id):
        for stage in self.stages:
            try:
                stage.plot(test_id, sensor_id)
            except:
                continue