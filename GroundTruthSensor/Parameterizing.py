import FOV_Stage as FOV
import Stages.Distance_Stage as D
import Stages.Gausian_Stage as G
import Range_Resolution_Stage as RR

class Parameterizing():

    def load_sensor(self, sensor_id):
        stages = []
        if sensor_id == 0:
            return stages
        if sensor_id == 1:
            stages.append(D.Distance_Stage(35))
        if sensor_id == 2:
            stages.append(FOV.FOV_Stage(120, 35))
        if sensor_id == 3:
            stages.append(RR.Range_Resolution_Stage(0.3))
        if sensor_id == 4:
            stages.append(D.Distance_Stage(35))
            stages.append(FOV.FOV_Stage(120, 35))
            stages.append(RR.Range_Resolution_Stage(0.3))
        return stages