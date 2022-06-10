import SpawnpointHandler
import carla

client = carla.Client('localhost', 2000)
spawnpointHandler = SpawnpointHandler.SpawnpointHandler(client)

spawnpointHandler.draw_spawn_points()