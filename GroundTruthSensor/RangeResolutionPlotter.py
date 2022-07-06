import matplotlib.pyplot as plt


class Range_Resolution_Plotter:

    def __init__(self):
        plt.figure(figsize=(8, 8), dpi=80)
        self.range_resolution = []

    def save_range_resolution(self, distance, noise):
        self.range_resolution.append([distance, noise])

    def plot(self, test_id, sensor_id):
        plt.xlabel('Abstand')
        plt.ylabel('Rauschen')
        plt.title = "Winkelauflösung"       
        for entry in self.range_resolution:
            plt.plot(entry)
        plt.savefig("plots/range_resolution/" + str(test_id) + str(sensor_id) + "_Range_Resolution.svg", format="svg",transparent=True)
        print("saved plot")
        self.range_resolution = []

        