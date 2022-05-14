import carla
import numpy as np

class FOV_Stage():

    def __init__(self):
        pass    
    
    def check_stage(self, actor, sensor):
        self.draw_fov(self=self, sensor=sensor)
        ego_location = sensor.ego_vehilce.get_location()
        actor_location = actor.get_location()
        first_vector = [(sensor.fov_right_vector.x - ego_location.x), (sensor.fov_left_vector.x - ego_location.x)]
        second_vector = [(sensor.fov_right_vector.y - ego_location.y), (sensor.fov_left_vector.y - ego_location.y)]
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

    def draw_fov(self, sensor):
        ego_transform = sensor.ego_vehilce.get_transform()
        ego_location = sensor.ego_vehilce.get_location()
        sensor.fov_right_vector = self.draw_line_with_rotation(self=self, ego_transform=ego_transform, ego_location=ego_location, rotation=sensor.fov/2, distance=sensor.distance, sensor=sensor)
        sensor.fov_left_vector = self.draw_line_with_rotation(self=self, ego_transform=ego_transform, ego_location=ego_location, rotation=-sensor.fov/2, distance=sensor.distance, sensor=sensor)
        self.draw_line_with_rotation(self=self, ego_transform=ego_transform, ego_location=ego_location, rotation=0, distance=sensor.distance, sensor=sensor)

    
    def draw_line_with_rotation(self, ego_transform, ego_location, rotation, distance, sensor):
        ego_rotation = ego_transform.rotation
        new_rotation = carla.Rotation(ego_rotation.pitch, ego_rotation.yaw, ego_rotation.roll)
        new_rotation.yaw += rotation
        new_transform = carla.Transform(ego_location, new_rotation)
        new_vector = new_transform.get_forward_vector()
        new_vector.x = new_vector.x * distance
        new_vector.y = new_vector.y * distance
        new_vector.z = new_vector.z * distance
        end_location = carla.Location(ego_location.x + new_vector.x, ego_location.y + new_vector.y, ego_location.z + new_vector.z)
        sensor.world.debug.draw_line(ego_location, end_location, life_time=0.1)
        return end_location