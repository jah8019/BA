import datetime
from operator import index
from typing import Iterable
import matplotlib.pyplot as plt
import Plotpoints as pp
import carla

class Environment_plotter():

    def __init__(self, object_list):
        plt.figure(figsize=(8, 6), dpi=80)
        self.actors = []
        self.dedected_actors = []
        self.traffic_signs = []
        self.dedected_signs = []
        if object_list is Iterable:
            for object in object_list:
                if 'vehicle' in object.type_id:
                    object_location = object.get_location()
                    self.actors.append(pp.Plotpoints(object.id, object_location.x , object_location.y , object.type_id))
                if 'traffic' in object.type_id:
                    self.traffic_signs.append(pp.Plotpoints(object.id, object_location.x , object_location.y , object.type_id))
                    if 'traffic_light' in object.type_id:
                        object.set_state(carla.TrafficLightState.Green)


    def save_environment(self, object_list, z):
        for object in object_list:
            location = object.get_location()
            elem = [x for x in self.actors if x.id == object.id]
            if elem.__len__() == 1:
                self.actors[self.actors.index(elem[0])].x.append(location.x )
                self.actors[self.actors.index(elem[0])].y.append(location.y )
            else:
                if 'vehicle' in object.type_id:
                    self.actors.append(pp.Plotpoints(object.id, location.x, location.y, object.type_id))

            elem = [x for x in self.traffic_signs if x.id == object.id]
            if elem.__len__() == 1:
                self.traffic_signs[self.traffic_signs.index(elem[0])].x.append(location.x )
                self.traffic_signs[self.traffic_signs.index(elem[0])].y.append(location.y )
            else:
                if 'traffic' in object.type_id:
                    self.actors.append(pp.Plotpoints(object.id, location.x, location.y, object.type_id))  
        
        for object in z:
            location = object.get_location()
            elem = [x for x in self.dedected_actors if x.id == object.id]
            if elem.__len__() == 1:
                self.dedected_actors[self.dedected_actors.index(elem[0])].x.append(location.x )
                self.dedected_actors[self.dedected_actors.index(elem[0])].y.append(location.y )
            else:
                if 'vehicle' in object.type_id:
                    self.dedected_actors.append(pp.Plotpoints(object.id, location.x , location.y , object.type_id))
            
            elem = [x for x in self.dedected_signs if x.id == object.id]
            if elem.__len__() == 1:
                self.dedected_signs[self.dedected_signs.index(elem[0])].x.append(location.x )
                self.dedected_signs[self.dedected_signs.index(elem[0])].y.append(location.y )
            else:
                if 'traffic' in object.type_id:
                    self.dedected_signs.append(pp.Plotpoints(object.id, location.x , location.y , object.type_id))


    def plot(self, ego_vehicle, test_id):
        id = 310 + test_id
        plt.subplot(id)
        for actor in self.actors:
            if ego_vehicle.type_id in actor.type_id:
                bounding_box = ego_vehicle.bounding_box
                transform = ego_vehicle.get_transform()
                self.plot_bounding_box(bounding_box, transform)
            else: 
                plt.plot(actor.x, actor.y, 'b', label="Ground-Truth", linewidth=1)
        for sign in self.traffic_signs:
            plt.plot(sign.x, sign.y, 'bo', label="Ground-Truth")
        for actor in self.dedected_actors:
            plt.plot(actor.x, actor.y, 'r--', label="Sensor data", linewidth=3)
        for sign in self.dedected_signs:
            plt.plot(sign.x, sign.y, 'ro', label="Sensor data")    
        plt.xlim([-30, 40])
        plt.ylim([-55, -75])
        plt.legend()
        self.actors = []
        self.dedected_actors = []

    def check_if_same_level(self, x, y):
        if x < y + 1 and x > y - 1:
            return True
        
        return False
            
    def plot_bounding_box(self, boundingbox, transform):

        vertices = boundingbox.get_world_vertices(transform)
        elem = [x for x in vertices if self.check_if_same_level(x.z, vertices[0].z)]
        next = elem[1]
        current = elem[0]
        plt.plot([current.x, next.x], [current.y, next.y], 'r', linewidth=1)
        current = next
        next = elem[3]
        plt.plot([current.x, next.x], [current.y, next.y], 'r', linewidth=1)
        current = next
        next = elem[2]
        plt.plot([current.x, next.x], [current.y, next.y], 'r', linewidth=1)
        current = next
        next = elem[0]
        plt.plot([current.x, next.x], [current.y, next.y], 'r', linewidth=1)
        
    def show_plot(self):
        plt.xlim([35, 65])
        plt.ylim([10, 20])
        plt.legend()
        plt.show()
        
    def save_plot(self, test_id):    
        # plt.xlim([0, 65])
        # plt.ylim([0, 65])
        plt.savefig("tmp" + str(test_id) + "_Ground_Truth.svg", format="svg",transparent=True)
        print("saved plot")

    def plot_id(self, id, location):
        plt.text(location.x, location.y, str(id), color="red", fontsize=12)