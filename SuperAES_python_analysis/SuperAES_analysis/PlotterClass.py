import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from pylab import cm
import numpy as np

class PlotterClass:
    lw = 2  #linewidth
    def __init__(self, data, params):
        self.probs = data
        self.params = params
    """
    def __truncate(self, number, digits) -> float:
        # Improve accuracy with floating point operations, to avoid truncate(16.4, 2) = 16.39 or truncate(-1.13, 2) = -1.12
        nbDecimals = len(str(number).split('.')[1])
        if nbDecimals <= digits:
            return number
        stepper = 10.0 ** digits
        return math.trunc(stepper * number) / stepper

    def generate_slider(self, label, valmin, valmax, valinit, valstep, axes_list):

        f = plt.axes(axes_list)
        slider = Slider(f, label, valmin, valmax, valinit=valinit, valstep=valstep)
        return slider


    def gen_data_sigma(self,sigmas):
        plots = []
        for sigma in sigmas:
            x = [x[0] for x in self.probs if x[1] == sigma and x[3]==self.params['f']]  # distance
            y = [x[2] for x in self.probs if x[1] == sigma and x[3]==self.params['f']]  # prob
            plots.append((x, y))
        return plots
    def gen_data_distance(self,distances):
        plots = []
        for dist in distances:
            x = [x[1] for x in self.probs if x[0] == dist and x[3]==self.params['f']]  # distance
            y = [x[2] for x in self.probs if x[0] == dist and x[3]==self.params['f']]  # prob
            plots.append((x, y))
        return plots
    """
    def plot_sigmas(self):
        # Create a subplot
        fig, ax = plt.subplots()
        plt.subplots_adjust(bottom=0.35)
        #plt.xlim((1, 10))
        sv = 0.1  # define the starting value of sigma
        #sigmas = [1, 3, 5, 8, 12]
        #colors = ["#4D1A1A", "#B03C3C", "#D94A4A", "#C68B8A", "#FFC2B5"]
        #plots_data = self.gen_data_sigma(sigmas)
        #for i in range(len(sigmas)):
        ax.plot(self.probs,lw=self.lw) #label="σ = "+str(sel.val), color=colors[i], lw=self.lw)
        #ax.legend()
        plt.xlabel("Distance (km) ")
        plt.ylabel("Probability")
        plt.title("Probability(distance)")
        # display graph
        plt.show()
