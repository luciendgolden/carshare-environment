"""
A representation of Ride time variable    
                                              
"""

from matplotlib import pyplot
import numpy
from fis import fis
from fuzzylogic.classes import Domain
from fuzzylogic.functions import R, S, triangular, bounded_sigmoid

# axis's limits
X_FROM, X_TO = 0, 60
Y_FROM, Y_TO = 0, 1
# !!! domain name should be equal to the file name to allow dynamic imports (see rules.py and fuzzylogic.classes.rule_from_table)
DOMAIN_NAME = "ride_time"

# define the domain for Ride time
ride_time = Domain(DOMAIN_NAME, X_FROM, X_TO, res=0.1)
# define sets
ride_time.short = S(0,15)
ride_time.average = triangular(10,25)
ride_time.long = triangular(20,40)
ride_time.very = bounded_sigmoid(40, 50) # range is 30-60
#ride_time.very = R(30, 60)

# Add this domain to the FIS
@fis.domain
def define_domain():
    return ride_time


def print_ride_time_result(input, omit_zeros=False):
    """Calculate and print membership values for input"""
    result = ride_time(input)
    for set in result:
        if (not omit_zeros or (omit_zeros and result[set] > 0.01)):
            print(f"{set}: {result[set]}")

def plot():
    """Draw the ride time functions using pyplot"""
    ride_time = define_domain()
    # set parameters of the plot
    pyplot.rc("figure", figsize=(10, 5))

    ride_time.short.plot()
    ride_time.average.plot()
    ride_time.long.plot()
    ride_time.very.plot()

    # set y-axis limits
    pyplot.ylim(Y_FROM, Y_TO+0.05)
    pyplot.xlim(X_FROM, X_TO)
    # set axis ticks
    pyplot.yticks(numpy.arange(Y_FROM, Y_TO+0.1, step=0.1))
    pyplot.xticks(numpy.arange(X_FROM, X_TO+1, step=10))
    # add grid
    pyplot.grid()

    # name axis
    pyplot.xlabel("Minutes")
    pyplot.ylabel("Truth value")

    # title plot
    pyplot.title("Ride time Fuzzy Sets")

    pyplot.legend(["Short", "Average", "Long", "Very long"])
    # open window with plot
    pyplot.show()
