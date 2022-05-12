import carla
import random
import GroundTruthSensor

client = carla.Client('localhost', 2000)
world = client.load_world("Town02")

settings = world.get_settings()
settings.synchronous_mode = True # Enables synchronous mode
settings.fixed_delta_seconds = 0.05
world.apply_settings(settings)

traffic_manager = client.get_trafficmanager()
traffic_manager.set_synchronous_mode(True)

spawn_points = world.get_map().get_spawn_points()

vehicle_blueprint = world.get_blueprint_library().find('vehicle.tesla.model3')
vehicle_blueprint.set_attribute('role_name','ego')
print('\nEgo role_name is set')

spawn_point = random.choice(spawn_points)

ego_vehicle = world.spawn_actor(vehicle_blueprint, spawn_point)
ego_vehicle.set_autopilot(True)

vehicle_blueprints = world.get_blueprint_library().filter('*vehicle*')
for i in range(0,5):
    blueprint = random.choice(vehicle_blueprints)
    spawn_point = random.choice(spawn_points)
    actor = world.try_spawn_actor(blueprint, spawn_point)
    if(actor is not None):
        actor.set_autopilot(True)

spectator = world.get_spectator()
spectator.set_transform(ego_vehicle.get_transform())

world.tick()

groundTruthSensor = GroundTruthSensor.GroundTruthSensor(20, world, ego_vehicle, 30)

while True:
  world.tick()
  groundTruthSensor.tick()