import carla

class SpawnpointHandler():

    def __init__(self, client):
        self.client = client

    def draw_spawn_points(self):
        world = self.client.get_world()

        settings = world.get_settings()
        settings.synchronous_mode = True # Enables synchronous mode
        settings.fixed_delta_seconds = 0.05
        world.apply_settings(settings)

        traffic_manager = self.client.get_trafficmanager()
        traffic_manager.set_synchronous_mode(True)
        traffic_manager.set_random_device_seed(3)

        spawn_points = world.get_map().get_spawn_points()

        index = 0
        for spawnpoint in spawn_points:
            world.debug.draw_string(spawnpoint.location, str(index), life_time=100.0)
            index = index + 1
        spectator = world.get_spectator()
        while(True):
            world.tick()

    def setup_test(self, test_id):
        actors = []
        world = self.client.get_world()
        spawn_points = world.get_map().get_spawn_points()
        traffic_manager = self.client.get_trafficmanager()

        vehicle_blueprint = world.get_blueprint_library().find('vehicle.tesla.model3')
        spawn_point_1 =  spawn_points[47]
        ego_vehicle = world.spawn_actor(vehicle_blueprint, spawn_point_1)
        traffic_manager.ignore_lights_percentage(ego_vehicle, 100)
        actors.append(ego_vehicle)

        if test_id == 1:
            # Route 2
            spawn_point_2 =  spawn_points[45]
            # Create route 2 from the chosen spawn points
            route_2 = []
            route_2.append(spawn_points[2].location)
            vehicle_blueprint = world.get_blueprint_library().find('vehicle.tesla.cybertruck')
            second_vehicle = world.spawn_actor(vehicle_blueprint, spawn_point_2)
            second_vehicle.set_autopilot(True)
            traffic_manager.set_path(second_vehicle, route_2)
            traffic_manager.ignore_lights_percentage(second_vehicle, 100)
            actors.append(second_vehicle)

        if test_id == 2:
            # Route 3
            spawn_point_3 =  spawn_points[117]
            # Create route 3 from the chosen spawn points
            route_3 = []
            route_3.append(spawn_points[3].location)
            vehicle_blueprint = world.get_blueprint_library().find('vehicle.volkswagen.t2')
            third_vehicle = world.spawn_actor(vehicle_blueprint, spawn_point_3)
            third_vehicle.set_autopilot(True)
            traffic_manager.set_path(third_vehicle, route_3)
            actors.append(third_vehicle)

        if test_id == 3:
            # Route 4
            spawn_point_4 =  spawn_points[93]
            # Create route 4 from the chosen spawn points
            route_4 = []
            route_4.append(spawn_points[58].location)
            vehicle_blueprint = world.get_blueprint_library().find('vehicle.audi.etron')
            fourth_vehicle = world.spawn_actor(vehicle_blueprint, spawn_point_4)
            fourth_vehicle.set_autopilot(True)
            traffic_manager.set_path(fourth_vehicle, route_4)
            actors.append(fourth_vehicle)

        if test_id == 4:
            # Route 5
            spawn_point_5 =  spawn_points[101]
            # Create route 5 from the chosen spawn points
            route_5 = []
            route_5.append(spawn_points[59].location)
            vehicle_blueprint = world.get_blueprint_library().find('vehicle.audi.a2')
            fifth_vehicle = world.spawn_actor(vehicle_blueprint, spawn_point_5)
            fifth_vehicle.set_autopilot(True)
            traffic_manager.set_path(fifth_vehicle, route_5)
            actors.append(fifth_vehicle)

        if test_id == 5:
            # Route 6
            spawn_point_6 =  spawn_points[134]
            # Create route 6 from the chosen spawn points
            route_6 = []
            route_6.append(spawn_points[2].location)
            vehicle_blueprint = world.get_blueprint_library().find('vehicle.audi.tt')
            sixth_vehicle = world.spawn_actor(vehicle_blueprint, spawn_point_6)
            sixth_vehicle.set_autopilot(True)
            traffic_manager.set_path(sixth_vehicle, route_6)
            actors.append(sixth_vehicle)

        return actors

