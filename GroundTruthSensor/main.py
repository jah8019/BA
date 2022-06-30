import time
import GroundTruthSensor as sensor
import Parameterizing as pm
import SpawnpointHandler as sh
import CarlaAdapter as ca

town_name = 'Town10'
ego_vehicle_id = 0
input_adapter = ca.Carla_Adapter()

for sensor_id in range(4, 5):
    import EnvironmentPlotter as ep       
    environemnt_plotter = ep.Environment_plotter(input_adapter.get_actors())
    for test_id in range(1, 4):

        spawnpoint_handler = sh.SpawnpointHandler(input_adapter)
        actors = spawnpoint_handler.setup_test(town_name, test_id)
        ego_vehicle_id = spawnpoint_handler.ego_vehicle_id
        ego_vehicle = actors[0]

        parameterizing = pm.Parameterizing(input_adapter)
        stages = parameterizing.load_sensor(sensor_id)
        ground_truth_sensor = sensor.GroundTruthSensor(ego_vehicle, stages)

        timestamp = 0
        global_start_time = time.time()
        f = open("Sensor_" + str(sensor_id) + "Test_" + str(test_id) + "_times.txt", "a", buffering=1)
        f.write("Sensor_" + str(sensor_id) + "Test_" + str(test_id) + "_times\n")
        while True:
            start_time = time.time()
            input_adapter.tick()
            ground_truth_actors = input_adapter.get_actors() 
            ego_vehicle = input_adapter.get_actor(ego_vehicle_id)
            ground_truth_sensor.ego_vehilce = ego_vehicle
            z = ground_truth_sensor.tick(ground_truth_actors)
            input_adapter.handle_dedection(z, ego_vehicle)
            environemnt_plotter.save_environment(input_adapter.get_actors(), z)
            timestamp = timestamp + 1
            end_time = time.time()
            time_elapsed = end_time-start_time
            f.write(str(timestamp)+ ";" + str(time_elapsed) + "\n")
            if timestamp == 10*60:
                f.write("General:" + str(time.time() - global_start_time))
                f.close()
                environemnt_plotter.plot(ego_vehicle, test_id, sensor_id)
                
                break
        ground_truth_sensor.close()
        input_adapter.clean_up(actors)
            

    environemnt_plotter.save_plot(test_id, sensor_id)