from operator import index
import matplotlib.pyplot as plt
import Plotpoints as pp

class Environment_plotter():

    def __init__(self, object_list):
        plt.figure(figsize=(8, 6), dpi=80)
        self.actors = []
        self.dedected = []
        for object in object_list:
            if 'vehicle' in object.type_id:
                object_location = object.get_location()
                self.actors.append(pp.Plotpoints(object.id, object_location.x , object_location.y , object.type_id))

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
        for object in z:
            location = object.get_location()
            elem = [x for x in self.dedected if x.id == object.id]
            if elem.__len__() == 1:
                self.dedected[self.dedected.index(elem[0])].x.append(location.x )
                self.dedected[self.dedected.index(elem[0])].y.append(location.y )
            else:
                if 'vehicle' in object.type_id:
                    self.dedected.append(pp.Plotpoints(object.id, location.x , location.y , object.type_id))

    def plot(self, ego_vehicle, test_id):
        id = 510 + test_id
        plt.subplot(id)
        for actor in self.actors:
            if ego_vehicle.type_id in actor.type_id:
                bounding_box = ego_vehicle.bounding_box
                transform = ego_vehicle.get_transform()
                self.plot_bounding_box(bounding_box, transform)
            else: 
                plt.plot(actor.x, actor.y, 'b', label="Ground-Truth")
        for actor in self.dedected:
            plt.plot(actor.x, actor.y, 'r--', label="Sensor data")
        # plt.xlim([30, 65])
        # plt.ylim([0, 35])
        plt.legend()
        self.actors = []
        self.dedected = []
            
    def plot_bounding_box(self, boundingbox, transform):
        vertices = boundingbox.get_world_vertices(transform)
        elem = [x for x in vertices if x.z == vertices[0].z]
        next = elem[1]
        current = elem[0]
        plt.plot([current.x, next.x], [current.y, next.y], 'r')
        current = next
        next = elem[3]
        plt.plot([current.x, next.x], [current.y, next.y], 'r')
        current = next
        next = elem[2]
        plt.plot([current.x, next.x], [current.y, next.y], 'r')
        current = next
        next = elem[0]
        plt.plot([current.x, next.x], [current.y, next.y], 'r')
        
    def show_plot(self):
        plt.xlim([35, 65])
        plt.ylim([10, 20])
        plt.legend()
        plt.show()
        
    def save_plot(self, test_id):    
        plt.savefig("tmp")