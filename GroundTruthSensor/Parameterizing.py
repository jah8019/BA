import Stages.FOV_Stage
import Stages.Distance_Stage

class Parameterizing():

    def __init__(self):
        pass

    def load_sensor(self, sensor_id):
        stages = []
        if sensor_id == 1:
            stages.append(Stages.Distance_Stage.Distance_Stage(30))
        if sensor_id == 2:
            stages.append(Stages.Distance_Stage.Distance_Stage(30))
            stages.append(Stages.FOV_Stage.FOV_Stage(80, 30))
        return stages 