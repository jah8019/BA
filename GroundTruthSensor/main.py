import time
import GroundTruthSensor as sensor
import Parameterizing as pm
import SpawnpointHandler as sh
import CarlaAdapter as ca

town_name = 'Town10'
ego_vehicle_id = 0
input_adapter = ca.Carla_Adapter()

for sensor_id in range(1, 5):
    import EnvironmentPlotter as ep       
    environemnt_plotter = ep.Environment_plotter(input_adapter.get_actors())
    for test_id in range(1, 4):

        spawnpoint_handler = sh.SpawnpointHandler(input_adapter)
        actors = spawnpoint_handler.setup_test(town_name, test_id)
        ego_vehicle_id = spawnpoint_handler.ego_vehicle_id
        ego_vehicle = actors[0]

        parameterizing = pm.Parameterizing()
        stages = parameterizing.load_sensor(sensor_id)
        ground_truth_sensor = sensor.GroundTruthSensor(ego_vehicle, stages)

        timestamp = 0
        combined_times = 0
        combined_times_carla = 0
        combined_times_result_handling = 0
        global_start_time = time.time()
        f = open("Results/Sensor_" + str(sensor_id) + "Test_" + str(test_id) + "_times.txt", "a", buffering=1)
        f.write("Sensor_" + str(sensor_id) + "Test_" + str(test_id) + "_times\n")
        while True:
            start_time_carla_communication = time.time() 
            input_adapter.tick()
            end_time_carla_communication = time.time()

            ground_truth_actors = input_adapter.get_actors() 
            ego_vehicle = input_adapter.get_actor(ego_vehicle_id)
            start_time_algo = time.time()
            z = ground_truth_sensor.tick(ground_truth_actors, ego_vehicle)
            end_time_algo = time.time()
            start_time_result_handling = time.time()
            input_adapter.handle_dedection(z, ego_vehicle)
            environemnt_plotter.save_environment(input_adapter.get_actors(), z)
            end_time_result_handling = time.time()
            timestamp = timestamp + 1
            time_elapsed_algo = end_time_algo - start_time_algo
            combined_times_algo = combined_times + time_elapsed_algo
            time_elapsed_carla = end_time_carla_communication - start_time_carla_communication
            combined_times_carla = combined_times_carla + time_elapsed_carla
            time_elapsed_result_handling = end_time_result_handling - start_time_result_handling
            combined_times_result_handling = combined_times_result_handling + time_elapsed_result_handling
           # f.write(str(timestamp)+ ";" + str(time_elapsed) + "\n")
            if timestamp == 25*60:
                f.write("CombinedTimes_Carla:" + str(combined_times_carla) + "\n")
                f.write("CombinedTimes_Algo:" + str(combined_times_algo) + "\n")
                f.write("CombinedTimes_Result_Handling:" + str(combined_times_result_handling) + "\n")
                f.write("General:" + str(time.time() - global_start_time) + "\n")
                f.close()
                environemnt_plotter.plot(ego_vehicle, test_id)
                break
        input_adapter.clean_up(actors)
    environemnt_plotter.save_plot(test_id, sensor_id)
    ground_truth_sensor.plot(test_id, sensor_id)
