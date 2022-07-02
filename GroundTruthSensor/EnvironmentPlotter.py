import datetime
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
            if 'vehicle' in object.type_id:
                elem = [x for x in self.actors if x.id == object.id]
                if elem.__len__() == 1:
                    self.actors[self.actors.index(elem[0])].x.append(location.x )
                    self.actors[self.actors.index(elem[0])].y.append(location.y )
                else:
                    self.actors.append(pp.Plotpoints(object.id, location.x, location.y, object.type_id))
            
            if 'traffic' in object.type_id:
                elem = [x for x in self.traffic_signs if x.id == object.id]
                if elem.__len__() == 0:
                    self.traffic_signs.append(pp.Plotpoints(object.id, location.x, location.y, object.type_id))  
        
        for object in z:
            location = object.get_location()
            elem = [x for x in self.dedected_actors if x.id == object.id]
            if elem.__len__() == 1:
                self.dedected_actors[self.dedected_actors.index(elem[0])].x.append(location.x )
                self.dedected_actors[self.dedected_actors.index(elem[0])].y.append(location.y )
            else:
                if 'vehicle' in object.type_id:
                    self.dedected_actors.append(pp.Plotpoints(object.id, location.x , location.y , object.type_id))
            
            if 'traffic.stop' in object.type_id or 'traffic.traffic_light' in object.type_id:
                elem = [x for x in self.dedected_signs if x.id == object.id]
                if elem.__len__() == 0:        
                    self.dedected_signs.append(pp.Plotpoints(object.id, location.x , location.y , object.type_id))


    def plot(self, ego_vehicle, test_id, sensor_id):
        id = 410 + test_id
        plt.subplot(id)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.tight_layout() 
        for actor in self.actors:
            if ego_vehicle.type_id in actor.type_id:
                bounding_box = ego_vehicle.bounding_box
                self.plot_bounding_box(bounding_box)
            else: 
                plt.plot(actor.x, actor.y, 'k', label="Ground Truth", linewidth=0.5)
        for sign in self.traffic_signs:
            plt.scatter(sign.x, sign.y, color='black')
        for actor in self.dedected_actors:
            # if(sensor_id < 3):
            plt.plot(actor.x, actor.y, 'r', label="Sensor data", linewidth=1)
            # else:
            #    plt.plot(actor.x, actor.y, 'r', label="Sensor data", linewidth=0.5)
        for sign in self.dedected_signs:
            plt.scatter(sign.x, sign.y, label="Ground Truth", color='red')    
        plt.xlim([-65, 35])
        plt.ylim([-40, -80])
        plt.legend()
        self.actors = []
        self.dedected_actors = []
            
    def plot_bounding_box(self, boundingbox):

        elem = boundingbox.points
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
        
    def save_plot(self, test_id, sensor_id):    
        plt.savefig("tmp" + str(test_id) + str(sensor_id) + "_Ground_Truth.svg", format="svg",transparent=True)
        print("saved plot")

    def plot_id(self, id, location):
        plt.text(location.x, location.y, str(id), color="red", fontsize=12)