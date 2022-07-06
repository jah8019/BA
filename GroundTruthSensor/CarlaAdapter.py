import carla
import Model.Object as o
import Model.Location as l
import Model.Bounding_Box as bb
import Model.Rotation as r

class Carla_Adapter():

    def __init__(self):
        self.client = carla.Client('localhost', 2000)
        self.world = self.client.get_world() 
        self.trafficmanager = self.start_up()
        self.spectator = self.world.get_spectator()
        self.actors = self.get_actors()

    def start_up(self):
        settings = self.world.get_settings()
        settings.synchronous_mode = True # Enables synchronous mode
        #settings.fixed_delta_seconds = None
        #settings.fixed_delta_seconds = 1/60
        settings.fixed_delta_seconds = 0.05
        self.world.apply_settings(settings)
        
        traffic_manager = self.client.get_trafficmanager()
        traffic_manager.set_synchronous_mode(True)
        traffic_manager.set_random_device_seed(2)

    def get_actors(self):
        actors = self.world.get_actors()
        generic_actors = []
        for actor in actors:
            generic_actor = self.get_object(actor)
            generic_actors.append(generic_actor)
        return generic_actors

    def get_object(self, actor):
        location = actor.get_location()
        generic_location = l.Location(location.x, location.y, location.z)
        type_id = actor.type_id 
        transform = actor.get_transform()
        rotation = transform.rotation
        generic_rotation = r.Rotation(rotation.pitch, rotation.yaw, rotation.roll)
        id = actor.id
        generic_bounding_box = None
        try:
            bounding_box = actor.bounding_box
            vertices = bounding_box.get_world_vertices(transform)
            generic_vertices = []
            for vertice in vertices:
                generic_vertice = l.Location(vertice.x, vertice.y, vertice.z)
                generic_vertices.append(generic_vertice)
            generic_bounding_box = bb.Bounding_Box([x for x in generic_vertices if self.check_if_same_level(x.z, generic_vertices[0].z)])
        except:
            generic_bounding_box = None
        return o.Object(generic_location, generic_rotation, type_id, id, generic_bounding_box)

    def get_actor(self, id):
        actor = self.world.get_actor(id)
        generic_actor = self.get_object(actor)
        return generic_actor

    def check_if_same_level(self, x, y):
        if x < y + 1 and x > y - 1:
            return True
        else:
            return False

    def draw_line(self, ego_location, end_location, life_time):
        carla_start_location = carla.Location(ego_location.x, ego_location.y, ego_location.z)
        carla_end_location = carla.Location(end_location.x, end_location.y, end_location.z)
        self.world.debug.draw_line(carla_start_location, carla_end_location, life_time)

    def clean_up(self, actors):
        for actor in actors:
            carla_actor = self.world.get_actor(actor.id)
            carla_actor.destroy()

    def tick(self):
        self.world.tick()

    def handle_dedection(self, z, ego_vehicle):
        for actor in z:
            actors_location = self.world.get_actor(actor.id).get_location()
            ego_location = self.world.get_actor(ego_vehicle.id).get_location()
            print(actor.type_id, " dedected")
            self.world.debug.draw_arrow(ego_location, actors_location, life_time=0.1)