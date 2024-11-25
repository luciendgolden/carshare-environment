"""
A representation of Recommend ride-sharing output variable               
It's dependent on traffic congestion and daytime                               
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
DOMAIN_NAME = "ride_sharing"

# define the domain for Ride Sharing action
ride_sharing = Domain(DOMAIN_NAME, X_FROM, X_TO, res=0.1)
# define sets
ride_sharing.no = minus(S(0, 35))
ride_sharing.recommended = triangular(30, 70)
ride_sharing.highly = minus(R(60, 100))
#print("Ride Sharing Domain was defined")

# Add this domain to the FIS
@fis.domain
def define_domain() -> Domain:
    return ride_sharing

def plot():
    """Draw the Ride Sharing functions using pyplot"""
    ride_sharing = define_domain()
    ride_sharing.no.plot()
    ride_sharing.recommended.plot()
    ride_sharing.highly.plot()

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
    pyplot.title("Ride Sharing Fuzzy Sets")

    pyplot.legend(["Not recommended", "Recommended", "Highly recommended"])
    # ride sharing with plot
    pyplot.show()

    # set parameters of the plot
    pyplot.rc("figure", figsize=(10, 5))
