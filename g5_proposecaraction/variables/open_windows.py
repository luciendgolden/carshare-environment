"""
A representation of Open windows output variable                                              
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
DOMAIN_NAME = "open_windows"

# define the domain for Open windows action
open_windows = Domain(DOMAIN_NAME, X_FROM, X_TO, res=0.1)
# define sets
open_windows.no = minus(S(0, 43))
open_windows.rec = triangular(30, 70)
open_windows.hig = minus(R(60, 100))
#print("Open windows Domain was defined")

# Add this domain to the FIS
@fis.domain
def define_domain() -> Domain:
    return open_windows

def plot():
    """Draw the Open windows functions using pyplot"""
    open_windows = define_domain()
    open_windows.no.plot()
    open_windows.rec.plot()
    open_windows.hig.plot()

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
    pyplot.title("Open windows Fuzzy Sets")

    pyplot.legend(["Not recommended", "Recommended", "Highly recommended"])
    # open window with plot
    pyplot.show()

    
    # set parameters of the plot
    pyplot.rc("figure", figsize=(10, 5))
