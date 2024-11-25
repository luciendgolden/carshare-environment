"""
A representation of Supply customer with a snack and water output variable               
It's dependent on ride time and temperature                               
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
DOMAIN_NAME = "supply_amenities"

# define the domain for Supply Amenities action
supply_amenities = Domain(DOMAIN_NAME, X_FROM, X_TO, res=0.1)
# define sets
supply_amenities.no = minus(S(0, 35))
supply_amenities.recommended = triangular(30, 70)
supply_amenities.highly = minus(R(60, 100))
#print("Supply Amenities Domain was defined")

# Add this domain to the FIS
@fis.domain
def define_domain() -> Domain:
    return supply_amenities

def plot():
    """Draw the Supply Amenities functions using pyplot"""
    supply_amenities = define_domain()
    supply_amenities.no.plot()
    supply_amenities.recommended.plot()
    supply_amenities.highly.plot()

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
    pyplot.title("Supply Amenities Fuzzy Sets")

    pyplot.legend(["Not recommended", "Recommended", "Highly recommended"])
    # supply amenities with plot
    pyplot.show()

    # set parameters of the plot
    pyplot.rc("figure", figsize=(10, 5))
