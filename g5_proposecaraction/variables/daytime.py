"""
A representation of daylight variable (output)   

"""
from matplotlib import pyplot
import numpy
from fis import fis
from fuzzylogic import combinators
from fuzzylogic.classes import Domain
from fuzzylogic.functions import R, S, triangular

# set parameters of the plot
pyplot.rc("figure", figsize=(10, 5))

# axis's limits
X_FROM, X_TO = 0, 24
Y_FROM, Y_TO = 0, 1.1

# define the domain for Daytime
daytime = Domain("daytime", X_FROM, X_TO, res=0.1)
# define fuzzy sets
daytime.dawn = triangular(4.5, 6.5)
daytime.morning  = triangular(6, 8.5)
daytime.day = triangular(8,19)
daytime.evening = triangular(18,22)
daytime.night = combinators.bounded_sum(S(0, 5), R(21.3,24))

# Add this domain to the FIS
@fis.domain
def define_domain() -> Domain:
    return daytime

def plot():
    """Draw daytime membership functions using pyplot"""
    daytime.dawn.plot()
    daytime.morning.plot()
    daytime.day.plot()
    daytime.evening.plot()
    daytime.night.plot()

    # set y-axis limits
    pyplot.ylim(Y_FROM, Y_TO)
    pyplot.xlim(X_FROM, X_TO)
    # set axis ticks
    pyplot.yticks(numpy.arange(Y_FROM, Y_TO, step=0.1))
    pyplot.xticks(numpy.arange(X_FROM, X_TO, step=1))
    # add grid
    pyplot.grid()

    # name axis
    pyplot.xlabel("o'clock")
    pyplot.ylabel("Truth value")

    # title plot
    pyplot.title("Daytime Fuzzy Sets")

    pyplot.legend(["Dawn", "Morning", "Day", "Evening", "Night"])
    # open window with plot
    pyplot.show()
