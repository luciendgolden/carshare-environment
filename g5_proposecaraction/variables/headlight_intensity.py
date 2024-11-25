"""
A representation of headlight intensity output variable
It is dependent on daytime and visibility
"""

from matplotlib import pyplot
import numpy
from fis import fis
from fuzzylogic.classes import Domain, Rule
from fuzzylogic.functions import R, S, triangular
from fuzzylogic.hedges import very

# axis's limits
X_FROM, X_TO = 0, 100
Y_FROM, Y_TO = 0, 1
# Define domain name for headlight_intensity
DOMAIN_NAME = "headlight_intensity"

# Define the domain
headlight_intensity = Domain(DOMAIN_NAME, X_FROM, X_TO, res=0.1)
# define sets
headlight_intensity.low = S(0, 40)
headlight_intensity.medium = very(triangular(30, 80))
headlight_intensity.high = R(70, 100)


# Add this domain to the FIS
@fis.domain
def define_domain() -> Domain:
    return headlight_intensity


def plot():
    """Draw the functions using pyplot"""
    # set parameters of the plot
    pyplot.rc("figure", figsize=(10, 5))

    headlight_intensity.low.plot()
    headlight_intensity.medium.plot()
    headlight_intensity.high.plot()

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
    pyplot.title(f"Headlight Intensity Fuzzy Sets")

    pyplot.legend(["Low", "Medium", "High"])
    # open window with plot
    pyplot.show()

