import FOV_Stage as FOV
import Stages.Distance_Stage as D
import Stages.Gausian_Stage as G
import Range_Resolution_Stage as RR

class Parameterizing():
    def __init__(self):
        self.rangeStage = RR.Range_Resolution_Stage(0.3)

    def load_sensor(self, sensor_id):
        stages = []
        if sensor_id == 0:
            stages.append(false_stage())
        if sensor_id == 1:
            return stages
        if sensor_id == 2:
            stages.append(D.Distance_Stage(35))
        if sensor_id == 3:
            stages.append(FOV.FOV_Stage(120, 35))
        if sensor_id == 4:
            stages.append(self.rangeStage)
        if sensor_id == 5:
            stages.append(D.Distance_Stage(35))
            stages.append(FOV.FOV_Stage(120, 35))
            stages.append(self.rangeStage)
        return stages

class false_stage():

    def check_stage(self, actor, ego_vehicle):
        return False

    def plot(self, test_id, sensor_id):
        return