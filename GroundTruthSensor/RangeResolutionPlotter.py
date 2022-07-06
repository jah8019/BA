from textwrap import indent
import matplotlib.pyplot as plt

class Range_Resolution_Plotter:

    def __init__(self, max_distance):
        self.max_distance = max_distance
        self.distance = []
        self.noise = []
        self.index = 0

    def save_range_resolution(self, distance, noise):
        if distance > self.max_distance:
            return
        self.index = self.index + 1
        self.distance.append(distance)
        self.noise.append(noise)

    def plot(self, test_id, sensor_id):
        plt.figure(figsize=(8, 8), dpi=80)
        plt.xlabel('Abstand')
        plt.ylabel('Rauschen')
        plt.title = "Winkelauflösung"       
        plt.plot(self.distance, self.noise, color="black", linewidth=1)
        plt.savefig("plots/range_resolution/" + str(test_id) + str(sensor_id) + "_Range_Resolution.svg", format="svg",transparent=True)
        print("saved plot")
        self.distance = []
        self.noise = []

        