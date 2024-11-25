"""
A representation of gas station variable (output)                                          
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
# !!! domain name should be equal to the file name to allow dynamic imports (see rules.py and fuzzylogic.classes.rule_from_table)
DOMAIN_NAME = "gas_station"

# Define the domain for Gas station action
gas_station = Domain(DOMAIN_NAME, X_FROM, X_TO, res=0.1)
# define sets
gas_station.no = S(0, 40)
gas_station.some = very(triangular(25, 70))
gas_station.large = R(50, 100)

# Add this domain to the FIS
@fis.domain
def define_domain() -> Domain:
    return gas_station


def plot():
    """Draw the gas station functions using pyplot"""
    gas_station.no.plot()
    gas_station.some.plot()
    gas_station.large.plot()

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
    pyplot.title("Gas Station Fuzzy Sets")

    pyplot.legend(["No incentive", "Some incentive", "Large incentive"])
    # open window with plot
    pyplot.show()

    # set parameters of the plot
    pyplot.rc("figure", figsize=(10, 5))