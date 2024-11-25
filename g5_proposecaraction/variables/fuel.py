"""
A representation of fuel variable (input)
                                          
"""

from matplotlib import pyplot
import numpy
from fis import fis
from fuzzylogic.classes import Domain
from fuzzylogic.functions import R, S, triangular, bounded_sigmoid, trapezoid

# axis's limits
X_FROM, X_TO = 0, 40
Y_FROM, Y_TO = 0, 1
# !!! domain name should be equal to the file name to allow dynamic imports (see rules.py and fuzzylogic.classes.rule_from_table)
DOMAIN_NAME = "fuel"

# Define the domain for Template action
fuel = Domain(DOMAIN_NAME, X_FROM, X_TO, res=0.1)
# define sets/functions
fuel.empty = bounded_sigmoid(5, 7.5, inverse=True) # range is 0, 10
fuel.some = triangular(5,20)
fuel.enough = trapezoid(15,20,25,30)
fuel.full = bounded_sigmoid(30,35) # range is 25-40

# Add this domain to the FIS
@fis.domain
def define_domain() -> Domain:
    return fuel

def print_fuel_result(input, omit_zeros=False):
    """Calculate and print membership values for input"""
    result = fuel(input)
    for set in result:
        if (not omit_zeros or (omit_zeros and result[set] > 0.00001)):
            print(f"{set}: {result[set]}")

def plot():
    """Draw the fuel functions using pyplot"""

    # set parameters of the plot
    pyplot.rc("figure", figsize=(10, 5))

    fuel.empty.plot()
    fuel.some.plot()
    fuel.enough.plot()
    fuel.full.plot()

    # set y-axis limits
    pyplot.ylim(Y_FROM, Y_TO+0.05)
    pyplot.xlim(X_FROM, X_TO)
    # set axis ticks
    pyplot.yticks(numpy.arange(Y_FROM, Y_TO+0.1, step=0.1))
    pyplot.xticks(numpy.arange(X_FROM, X_TO+1, step=2.5))
    # add grid
    pyplot.grid()

    # name axis
    pyplot.xlabel("Liters")
    pyplot.ylabel("Truth value")

    # title plot
    pyplot.title("Fuel Fuzzy Sets")

    pyplot.legend(["Empty", "Some", "Enough", "Full"])
    # open window with plot
    pyplot.show()