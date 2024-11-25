"""
<<<<<<< HEAD
A representation of Open windows output variable                                              
=======
A representation of output variable (example)                                              
>>>>>>> origin/main
"""

from matplotlib import pyplot
import numpy
from rules import fis
from fuzzylogic.classes import Domain
from fuzzylogic.functions import S, R

# axis's limits
X_FROM, X_TO = 0, 100
Y_FROM, Y_TO = 0, 1
# !!! domain name should be equal to the file name to allow dynamic imports (see rules.py and fuzzylogic.classes.rule_from_table)
DOMAIN_NAME = "template"

# Define the domain
template = Domain(DOMAIN_NAME, X_FROM, X_TO, res=0.1)
# define sets
template.set1 = S(0, 50)
template.set2 = R(50,100)

# Add this domain to the FIS
@fis.domain
def define_domain() -> Domain:
    return template

def plot():
    """Draw the functions using pyplot"""
    # set parameters of the plot
    pyplot.rc("figure", figsize=(10, 5))

    template.set1.plot()
    template.set2.plot()

    # set y-axis limits
    pyplot.ylim(Y_FROM, Y_TO)
    pyplot.xlim(X_FROM, X_TO)
    # set axis ticks
    pyplot.yticks(numpy.arange(Y_FROM, Y_TO+0.1, step=0.1))
    pyplot.xticks(numpy.arange(X_FROM, X_TO+1, step=10))
    # add grid
    pyplot.grid()

    # name axis
    pyplot.xlabel("xlabel")
    pyplot.ylabel("ylabel")

    # title plot
    pyplot.title(f"Template Fuzzy Sets")

    pyplot.legend(["Not recommended", "Recommended", "Highly recommended"])
    # open window with plot
    pyplot.show()

