"""
A representation of temperature variable (output)                                                    
"""

from matplotlib import pyplot
import numpy
from fis import fis
from fuzzylogic.classes import Domain
from fuzzylogic.functions import R, S, triangular, trapezoid

# axis's limits
X_FROM, X_TO = 0, 40
Y_FROM, Y_TO = 0, 1
# !!! domain name should be equal to the file name to allow dynamic imports (see rules.py and fuzzylogic.classes.rule_from_table)
DOMAIN_NAME = "temperature"

# define the domain
temperature = Domain(DOMAIN_NAME, X_FROM, X_TO, res=0.1)
# define sets
temperature.cold = S(0, 10)
temperature.cool = triangular(8, 18)
temperature.warm = trapezoid(15, 18, 22, 25)
temperature.hot = triangular(22,35)
temperature.extreme = R(32, 40)

# Add this domain to the FIS
@fis.domain
def define_domain():
    return temperature

def print_temperature_result(input, omit_zeros=False):
    """Calculate and print membership values for input"""
    result = temperature(input)
    for set in result:
        if (not omit_zeros or (omit_zeros and result[set] > 0.00001)):
            print(f"{set}: {result[set]}")

def plot():
    """Draw the temperature functions using pyplot"""

    # set parameters of the plot
    pyplot.rc("figure", figsize=(10, 5))

    temperature.cold.plot()
    temperature.cool.plot()
    temperature.warm.plot()
    temperature.hot.plot()
    temperature.extreme.plot()

    # set y-axis limits
    pyplot.ylim(Y_FROM, Y_TO+0.05)
    pyplot.xlim(X_FROM, X_TO)
    # set axis ticks
    pyplot.yticks(numpy.arange(Y_FROM, Y_TO+0.1, step=0.1))
    pyplot.xticks(numpy.arange(X_FROM, X_TO+1, step=2.5))
    # add grid
    pyplot.grid()

    # name axis
    pyplot.xlabel("Celsius")
    pyplot.ylabel("Truth value")

    # title plot
    pyplot.title("Temperature Fuzzy Sets")

    pyplot.legend(["Cold", "Cool", "Warm", "Hot", "Extreme"])
    # open window with plot
    pyplot.show()