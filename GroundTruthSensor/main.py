import carla
import GroundTruthSensor
import Parameterizing
import SpawnpointHandler

town_name = 'Town_10'
client = carla.Client('localhost', 2000)
world = client.get_world()

settings = world.get_settings()
settings.synchronous_mode = True # Enables synchronous mode
settings.fixed_delta_seconds = 0.05
world.apply_settings(settings)

traffic_manager = client.get_trafficmanager()
traffic_manager.set_synchronous_mode(True)
traffic_manager.set_random_device_seed(2)

import EnvironmentPlotter       
environemnt_plotter = EnvironmentPlotter.Environment_plotter(world.get_actors())

for test_id in range(1, 3):

    spawnpoint_handler = SpawnpointHandler.SpawnpointHandler(client)
    actors = spawnpoint_handler.setup_test(town_name, test_id)
    ego_vehicle = actors[0]

    parameterizing = Parameterizing.Parameterizing()
    stages = parameterizing.load_sensor(0)
    groundTruthSensor = GroundTruthSensor.GroundTruthSensor(world, ego_vehicle, stages)

    spectator = world.get_spectator()
    spectator.set_transform(ego_vehicle.get_transform())

    timestamp = 0

    while True:
        world.tick()
        z = groundTruthSensor.tick()
        environemnt_plotter.save_environment(world.get_actors(), z)
        timestamp = timestamp + 1
        
        if timestamp == 10*60:
            environemnt_plotter.plot(ego_vehicle, test_id)
            break
    
    for actor in actors:
        actor.destroy()

environemnt_plotter.save_plot(test_id)