"""
A representation of recommendation for stopping output variable
It is dependent on temperature and nearby poi
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
# Define domain name for recommendation for stopping
DOMAIN_NAME = "recommendation_for_stopping"

# Define the domain
recommendation_for_stopping = Domain(DOMAIN_NAME, X_FROM, X_TO, res=0.1)
# define sets
recommendation_for_stopping.notAdvised = S(0, 35)
recommendation_for_stopping.optional = very(triangular(30, 70))
recommendation_for_stopping.advised = R(60, 100)


# Add this domain to the FIS
@fis.domain
def define_domain() -> Domain:
    return recommendation_for_stopping


def plot():
    """Draw the functions using pyplot"""
    # set parameters of the plot
    pyplot.rc("figure", figsize=(10, 5))

    recommendation_for_stopping.notAdvised.plot()
    recommendation_for_stopping.optional.plot()
    recommendation_for_stopping.advised.plot()

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
    pyplot.title(f"Reccomendation for Stopping Fuzzy Sets")

    pyplot.legend(["Not Advised", "Optional", "Advised"])
    # open window with plot
    pyplot.show()

