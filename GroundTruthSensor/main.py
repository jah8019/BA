import carla
import GroundTruthSensor
import Parameterizing
import SpawnpointHandler

client = carla.Client('localhost', 2000)
world = client.get_world()

settings = world.get_settings()
settings.synchronous_mode = True # Enables synchronous mode
settings.fixed_delta_seconds = 0.05
world.apply_settings(settings)

traffic_manager = client.get_trafficmanager()
traffic_manager.set_synchronous_mode(True)
traffic_manager.set_random_device_seed(1)


spawnpoint_handler = SpawnpointHandler.SpawnpointHandler(client)
ego_vehicle = spawnpoint_handler.setup_test()

parameterizing = Parameterizing.Parameterizing
stages = parameterizing.load_sensor(1)
groundTruthSensor = GroundTruthSensor.GroundTruthSensor(world, ego_vehicle, stages)

spectator = world.get_spectator()
spectator.set_transform(ego_vehicle.get_transform())

import EnvironmentPlotter
environemnt_plotter = EnvironmentPlotter.Environment_plotter(world.get_actors(), ego_vehicle)

timestamp = 0

while True:
    world.tick()
    z = groundTruthSensor.tick()
    environemnt_plotter.save_environment(world.get_actors(), ego_vehicle, z)
    timestamp = timestamp + 1
    
    if timestamp == 5*60:
        environemnt_plotter.plot()
        environemnt_plotter.show_plot()
        break

