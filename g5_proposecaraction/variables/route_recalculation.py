"""
A representation of Route recalculation output variable               
It's dependent on traffic congestion and ride time                               
"""

from matplotlib import pyplot
import numpy
from fis import fis
from fuzzylogic.classes import Domain, Rule
from fuzzylogic.functions import R, S, triangular
from fuzzylogic.hedges import minus

# axis's limits
X_FROM, X_TO = 0, 100
Y_FROM, Y_TO = 0, 1
# !!! domain name should be equal to the file name to allow dynamic imports (see rules.py and fuzzylogic.classes.rule_from_table)
DOMAIN_NAME = "route_recalculation"

# define the domain for Route Recalculation action
route_recalculation = Domain(DOMAIN_NAME, X_FROM, X_TO, res=0.1)
# define sets
route_recalculation.no = minus(S(0, 35))
route_recalculation.recommended = triangular(30, 70)
route_recalculation.highly = minus(R(60, 100))
#print("Route Recalculation Domain was defined")

# Add this domain to the FIS
@fis.domain
def define_domain() -> Domain:
    return route_recalculation

def plot():
    """Draw the Route Recalculation functions using pyplot"""
    route_recalculation = define_domain()
    route_recalculation.no.plot()
    route_recalculation.recommended.plot()
    route_recalculation.highly.plot()

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
    pyplot.title("Route Recalculation Fuzzy Sets")

    pyplot.legend(["Not recommended", "Recommended", "Highly recommended"])
    # route recalculation with plot
    pyplot.show()

    # set parameters of the plot
    pyplot.rc("figure", figsize=(10, 5))
