import matplotlib.pyplot as plt
import Plotpoints as pp

class Environment_plotter():

    def __init__(self, object_list, ego_vehicle):
        self.actors = []
        self.dedected = []
        ego_location = ego_vehicle.get_location()
        for object in object_list:
            if 'vehicle' in object.type_id:
                object_location = object.get_location()
                self.actors.append(pp.Plotpoints(object.id, object_location.x - ego_location.x, object_location.y - ego_location.x, object.type_id))

    def save_environment(self, object_list, ego_vehicle, z):
        ego_location = ego_vehicle.get_location()
        for object in object_list:
            location = object.get_location()
            elem = [x for x in self.actors if x.id == object.id]
            if elem.__len__() == 1:
                self.actors[self.actors.index(elem[0])].x.append(location.x - ego_location.x)
                self.actors[self.actors.index(elem[0])].y.append(location.y - ego_location.y)
            else:
                if 'vehicle' in object.type_id:
                    self.actors.append(pp.Plotpoints(object.id, location.x - ego_location.x, location.y - ego_location.y, object.type_id))
        for object in z:
            location = object.get_location()
            elem = [x for x in self.dedected if x.id == object.id]
            if elem.__len__() == 1:
                self.dedected[self.dedected.index(elem[0])].x.append(location.x - ego_location.x)
                self.dedected[self.dedected.index(elem[0])].y.append(location.y - ego_location.y)
            else:
                if 'vehicle' in object.type_id:
                    self.dedected.append(pp.Plotpoints(object.id, location.x - ego_location.x, location.y - ego_location.y, object.type_id))

    def plot(self):
        for actor in self.actors:
            plt.plot(actor.x, actor.y, label=actor.type_id)
        # for object in self.dedected:
        #     plt.plot(actor.x, actor.y, label=actor.type_id)
            
            

    def show_plot(self):
        plt.legend()
        plt.show()
        
    def save_plot(self):    
        plt.savefig("tmp")

    # def update_spectator(self):
    #     ego_location = self.ego_vehicle.get_transform().location
    #     ego_rotation = self.ego_vehicle.get_transform().rotation
    #     location = carla.Location(ego_location.x, ego_location.y, ego_location.z + 70)
    #     rotation = carla.Rotation(ego_rotation.pitch - 90, ego_rotation.yaw, ego_rotation.roll)
    #     transform = carla.Transform(location, rotation)
    #     self.spectator.set_transform(transform)


