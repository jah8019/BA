import numpy.random

class Gausian_Stage():

    def __init__(self, max_range_meter):
        self.max_range = max_range_meter

    def check_stage(self, actor, sensor):
        offset = numpy.random.normal(0, self.max_range)
        location = actor.get_location()
        actor.location.x = location.x + offset
        actor.location.y = location.y + offset
        return True