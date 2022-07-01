import numpy as np
import sys
import math
sys.path.append('../')
import Model.Rotation as r
import Model.Location as l


class FOV_Stage():

    fov_right_vector = None
    fov_left_vector = None

    def __init__(self, fov, distance, debug_adapter):
        self.fov = fov
        self.distance = distance
        self.debug_adapter = debug_adapter
    
    def check_stage(self, actor, ego_vehicle):
        ego_location = ego_vehicle.get_location()
        self.set_fov(ego_vehicle)
        ego_location = ego_vehicle.get_location()
        actor_location = actor.get_location()
        first_vector = [(self.fov_right_vector.x - ego_location.x), (self.fov_left_vector.x - ego_location.x)]
        second_vector = [(self.fov_right_vector.y - ego_location.y), (self.fov_left_vector.y - ego_location.y)]
        a = np.array([first_vector, second_vector])
        third_vector = [(actor_location.x - ego_location.x), (actor_location.y - ego_location.y)]
        b = np.array(third_vector)
        solution = np.linalg.solve(a,b)
        if(solution[0] < 0 or solution[0] > 1):
            return False
        if(solution[1] < 0 or solution[1] > 1):
            return False
        else:
            return True

    def set_fov(self, ego_vehicle):
        ego_rotation = ego_vehicle.get_rotation()
        ego_location = ego_vehicle.get_location()
        self.fov_right_vector = self.draw_line_with_rotation(ego_rotation, ego_location, self.fov/2, self.distance)
        self.fov_left_vector = self.draw_line_with_rotation(ego_rotation, ego_location, -self.fov/2, self.distance)
    
    def draw_line_with_rotation(self, ego_rotation, ego_location, rotation, distance):
        new_rotation = r.Rotation(ego_rotation.pitch, ego_rotation.yaw, ego_rotation.roll)
        new_rotation.yaw += rotation
        new_vector = self.get_forward_vector(new_rotation)
        x = new_vector[0] * distance
        y = new_vector[1] * distance
        z = new_vector[2] * distance
        end_location = l.Location(ego_location.x + x, ego_location.y + y, ego_location.z + z)
        self.debug_adapter.draw_line(ego_location, end_location, life_time=0.1)
        return end_location

    def get_forward_vector(self, rotation):
        cp = math.cos(math.radians(rotation.pitch))
        sp = math.sin(math.radians(rotation.pitch))
        cy = math.cos(math.radians(rotation.yaw))
        sy = math.sin(math.radians(rotation.yaw))
        return [cy * cp, sy * cp, sp]