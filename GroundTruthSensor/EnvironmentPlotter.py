import datetime
from typing import Iterable
import matplotlib.pyplot as plt
import Plotpoints as pp
import carla
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes

class Environment_plotter():

    def __init__(self, object_list):
        plt.figure(figsize=(8, 8), dpi=80)
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


    def plot(self, ego_vehicle, test_id):
        id = 410 + test_id
        plt.subplot(id)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.tight_layout()
        bounding_box = ego_vehicle.bounding_box
        self.plot_bounding_box(bounding_box, plt)
        for actor in self.actors:
            if ego_vehicle.id == actor.id:
                continue
            else: 
                plt.plot(actor.x, actor.y, 'k', label="Ground Truth - Fahrzeug", linewidth=0.5)
        for i in range(0, len(self.traffic_signs)):
            sign = self.traffic_signs[i]
            if i == 0:
                plt.scatter(sign.x, sign.y, label="Ground Truth - Ampel", color='black')
            else: 
                plt.scatter(sign.x, sign.y, color='black')
        # for actor in self.dedected_actors:
        #     plt.plot(actor.x, actor.y, 'r', label="Sensordaten - Fahrzeug", linewidth=1)
        # for i in range(0, len(self.dedected_signs)):
        #     sign = self.dedected_signs[i]
        #     if i == 0:
        #         plt.scatter(sign.x, sign.y, label="Sensordaten - Ampel", color='red')    
        #     else: 
        #         plt.scatter(sign.x, sign.y, color='red')
        plt.xlim([-65, 35])
        plt.ylim([-40, -80])
        plt.legend(loc='upper right') 
        if test_id == 1:
            plt.title = "Überholmanöver"
        if test_id == 2:
            plt.title = "Abbiegen eng"
        if test_id == 3:
            plt.title = "Abbiegen weit"       
        self.actors = []
        self.dedected_actors = []

    def plot_zoomed(self, ego_vehicle, test_id):
        id = 410 + test_id
        ax = plt.subplot(id)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.tight_layout()
        plt.xlim([-65, 35])
        plt.ylim([-40, -80])
        plt.grid(True)
        if test_id == 1:
            plt.title = "Überholmanöver"
        if test_id == 2:
            plt.title = "Abbiegen eng"
        if test_id == 3:
            plt.title = "Abbiegen weit" 
        bounding_box = ego_vehicle.bounding_box
        self.plot_bounding_box(bounding_box, plt)
        for actor in self.actors:
            if ego_vehicle.id == actor.id:
                continue
            else: 
                plt.plot(actor.x, actor.y, 'k', label="Ground Truth - Fahrzeug", linewidth=0.5)
        for i in range(0, len(self.traffic_signs)):
            sign = self.traffic_signs[i]
            if i == 0:
                plt.scatter(sign.x, sign.y, label="Ground Truth - Ampel", color='black')
            else: 
                plt.scatter(sign.x, sign.y, color='black')
        for actor in self.dedected_actors:
            plt.plot(actor.x, actor.y, 'r', label="Sensordaten - Fahrzeug", linewidth=1)
        for i in range(0, len(self.dedected_signs)):
            sign = self.dedected_signs[i]
            if i == 0:
                plt.scatter(sign.x, sign.y, label="Sensordaten - Ampel", color='red')    
            else: 
                plt.scatter(sign.x, sign.y, color='red')   
        axis = zoomed_inset_axes(ax, 7, loc=2)
        for actor in self.dedected_actors:
            third = int(len(actor.x)/3)
            third_x = actor.x[:third]
            third_y = actor.y[:third]
            axis.plot(third_x, third_y)
        axis.grid(True)
        self.actors = []
        self.dedected_actors = []
            
    def plot_bounding_box(self, boundingbox, plotter):
        elem = boundingbox.points
        next = elem[1]
        current = elem[0]
        plotter.plot([current.x, next.x], [current.y, next.y],label="Egofahrzeug", color="blue", linewidth=1)
        current = next
        next = elem[3]
        plotter.plot([current.x, next.x], [current.y, next.y], color="blue", linewidth=1)
        current = next
        next = elem[2]
        plotter.plot([current.x, next.x], [current.y, next.y], color="blue", linewidth=1)
        current = next
        next = elem[0]
        plotter.plot([current.x, next.x], [current.y, next.y], color="blue", linewidth=1)
        
    def show_plot(self):
        plt.xlim([35, 65])
        plt.ylim([10, 20])
        plt.legend(loc='upper right')
        plt.show()
        
    def save_plot(self, test_id, sensor_id):  
        plt.legend(loc='upper right')
        plt.savefig("plots/" + "GroundTruth" + str(test_id) + str(sensor_id) + "_Ground_Truth.svg", format="svg",transparent=True)
        print("saved plot")

    def plot_id(self, id, location):
        plt.text(location.x, location.y, str(id), color="red", fontsize=12)