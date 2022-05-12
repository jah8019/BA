from pydoc import text
from tabnanny import check
import carla
from sympy import symbols, Eq, solve
import numpy as np


class GroundTruthSensor():

    fov_right_vector = None
    fov_left_vector = None

    def __init__(self, distance, world, ego_vehicle, fov):
        self.distance = distance
        self.world = world
        self.ego_vehilce = ego_vehicle
        self.fov = fov

    def tick(self):
        self.draw_fov(self.fov, self.distance)
        actors = self.world.get_actors()
        for actor in actors:
            self.check_actor(actor)  
    
    def check_actor(self, actor):
            if actor.id is self.ego_vehilce.id:
                return False
            if not self.is_into_distance(actor, self.distance):
                return False
            if not self.is_inside_of_fov_numpy(actor):
                return False
            print(actor.type_id, " dedected")
            self.draw_arrow_from_ego(actor)
            return True

    def is_into_distance(self, actor, distance):
        actors_location = actor.get_location()
        ego_location = self.ego_vehilce.get_location() 
        distance_to_vehicle = actors_location.distance(ego_location)
        if distance_to_vehicle <= distance:
            return True
        else:
            return False

    def is_inside_of_fov_numpy(self, actor):
        ego_location = self.ego_vehilce.get_location()
        actor_location = actor.get_location()
        first_vector = [(self.fov_right_vector.x - ego_location.x), (self.fov_right_vector.y - ego_location.y)]
        second_vector = [(self.fov_left_vector.x - ego_location.x), (self.fov_left_vector.y - ego_location.y)]
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

    def draw_arrow_from_ego(self, actor):
        actors_location = actor.get_location()
        ego_location = self.ego_vehilce.get_location() 
        self.world.debug.draw_arrow(ego_location, actors_location, life_time=0.1)

    def draw_fov(self, length, fov):
        ego_transform = self.ego_vehilce.get_transform()
        ego_location = self.ego_vehilce.get_location()
        self.fov_right_vector = self.draw_line_with_rotation(ego_transform, ego_location, fov/2, length)
        self.fov_left_vector = self.draw_line_with_rotation(ego_transform, ego_location, -fov/2, length)
        self.draw_line_with_rotation(ego_transform, ego_location, 0, length)

    def draw_line_with_rotation(self, ego_transform, ego_location, rotation, length):
        ego_rotation = ego_transform.rotation
        new_rotation = carla.Rotation(ego_rotation.pitch, ego_rotation.yaw, ego_rotation.roll)
        new_rotation.yaw += rotation
        new_transform = carla.Transform(ego_location, new_rotation)
        new_vector = new_transform.get_forward_vector()
        new_vector.x = new_vector.x * length
        new_vector.y = new_vector.y * length
        new_vector.z = new_vector.z * length
        end_location = carla.Location(ego_location.x + new_vector.x, ego_location.y + new_vector.y, ego_location.z + new_vector.z)
        self.world.debug.draw_line(ego_location, end_location, life_time=0.1)
        return end_location







    def is_inside_of_fov_sympy(self, actor):
        ego_location = self.ego_vehilce.get_location()
        actor_location = actor.get_location()
        
        r, l = symbols("r, l")
        equation_x = Eq(ego_location.x + r * (self.fov_right_vector.x - ego_location.x) + l * (self.fov_left_vector.x - ego_location.x), actor_location.x)
        equation_y = Eq(ego_location.y + r * (self.fov_right_vector.y - ego_location.y) + l * (self.fov_left_vector.y - ego_location.y), actor_location.y)
        #equation_z = Eq(ego_location.z + r * (self.fov_right_vector.z - ego_location.z) + l * (self.fov_left_vector.z - ego_location.z), actor_location.z)
        #Z wird vernachlässigt
        solution = solve((equation_x, equation_y), (r, l))
        if(solution[r] < 0 or solution[r] > 1):
            return False
        if(solution[l] < 0 or solution[l] > 1):
            return False
        else:
            return True
