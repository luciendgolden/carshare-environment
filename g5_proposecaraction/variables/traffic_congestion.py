from matplotlib import pyplot
import numpy
from fis import fis
from fuzzylogic.classes import Domain
from fuzzylogic.functions import R, S, triangular

# set parameters of the plot
pyplot.rc("figure", figsize=(10, 5))

# axis's limits
X_FROM, X_TO = 0, 50
Y_FROM, Y_TO = 0, 1.05

# define the domain for Traffic Congestion
traffic_congestion = Domain("traffic congestion", X_FROM, X_TO, res=0.1)
# define sets
traffic_congestion.highly_congested = S(0, 20)
traffic_congestion.average = triangular(15, 45)
traffic_congestion.uncongested = R(40,50)

# Add this domain to the FIS
@fis.domain
def define_domain() -> Domain:
    return traffic_congestion

def plot_traffic_congestion():
    """Draw traffic congestion membership functions using pyplot"""
    traffic_congestion.uncongested.plot()
    traffic_congestion.average.plot()
    traffic_congestion.highly_congested.plot()

    # set y-axis limits
    pyplot.ylim(Y_FROM, Y_TO)
    pyplot.xlim(X_FROM, X_TO)
    # set axis ticks
    pyplot.yticks(numpy.arange(Y_FROM, Y_TO, step=0.1))
    pyplot.xticks(numpy.arange(X_FROM, X_TO, step=5))
    # add grid
    pyplot.grid()

    # name axis
    pyplot.xlabel("km/h")
    pyplot.ylabel("Truth value")

    # title plot
    pyplot.title("Traffic Congestion Fuzzy Sets")

    pyplot.legend(["Uncongested", "Average", "Highly Congested"])
    # open window with plot
    pyplot.show()