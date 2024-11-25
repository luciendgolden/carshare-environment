"""
A representation of Speed adjustment output variable               
It is dependent on traffic congestion and visibility                              
"""

from matplotlib import pyplot
from fuzzylogic.classes import Domain, Rule
from fuzzylogic.functions import R, S, triangular
from fuzzylogic.hedges import minus
import numpy
from fis import fis

# axis's limits
X_FROM, X_TO = 0, 100
Y_FROM, Y_TO = 0, 1

DOMAIN_NAME = "speed_adjustment"

# define the domain for Speed Adjustment action
speed_adjustment = Domain(DOMAIN_NAME, X_FROM, X_TO, res=0.1)
# define sets
speed_adjustment.very_slow = minus(S(0, 25))
speed_adjustment.slow = triangular(20, 55)
speed_adjustment.moderate = triangular(50, 85)
speed_adjustment.fast = minus(R(85, 100))

# Add this domain to the FIS
@fis.domain
def define_domain() -> Domain:
    return speed_adjustment

def plot():
    """Draw the Speed Adjustment functions using pyplot"""
    speed_adjustment = define_domain()
    speed_adjustment.very_slow.plot()
    speed_adjustment.slow.plot()
    speed_adjustment.moderate.plot()
    speed_adjustment.fast.plot()

    # set y-axis limits
    pyplot.ylim(Y_FROM, Y_TO)
    pyplot.xlim(X_FROM, X_TO)
    # set axis ticks
    pyplot.yticks(numpy.arange(Y_FROM, Y_TO+0.1, step=0.1))
    pyplot.xticks(numpy.arange(X_FROM, X_TO+1, step=10))
    # add grid
    pyplot.grid()

    # name axis
    pyplot.xlabel("%")
    pyplot.ylabel("Truth value")

    # title plot
    pyplot.title("Speed Adjustment Category Fuzzy Sets")

    pyplot.legend(["Very Slow", "Slow", "Moderate", "Fast"])
    # speed adjustment with plot
    pyplot.show()

    # set parameters of the plot
    pyplot.rc("figure", figsize=(10, 5))
