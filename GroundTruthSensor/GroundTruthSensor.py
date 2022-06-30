import multiprocessing
import time
from joblib import Parallel, delayed

class GroundTruthSensor():

    def __init__(self, ego_vehicle, stages):
        self.ego_vehilce = ego_vehicle
        self.stages = stages
        self.z = []
        self.f = open("Time_Stages.txt", "a", buffering=1)
        self.f.write("-----------start")


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
    
    def tick(self, ground_truth_actors):
        x = ground_truth_actors.copy()
        half = int(len(x)/2)
        x_first = x[half:]
        x_second = x[:half]
        x_full = [x_first, x_second]
        self.z = []
        z = Parallel(n_jobs=8, backend="threading")(delayed(self.check_actor_all_stages)(partial_list) for partial_list in x_full)
        if z[0] is not None and z[1] is not None:
            z = z[0]+z[1]
        if z[0] is not None and z[1] is None:
            z = z[0]
        if z[1] is not None and z[0] is None:
            z = z[1]
        self.z = [elem for elem in z if elem is not None]
        # for actor in x:
        #     self.check_actor_all_stages(actor)
        return self.z

    def check_actor_all_stages(self, actors):
        z = []
        for actor in actors:
            if actor.id is self.ego_vehilce.id:
                return
            if actor.type_id == 'spectator':
                return
            for stage in self.stages:
                if not stage.check_stage(actor, self):
                    return
            z.append(actor)
        return z

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