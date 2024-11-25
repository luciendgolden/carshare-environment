"""
A representation of nearby points of interest (poi) variable (input)

"""
from matplotlib import pyplot
import numpy
from fis import fis
from fuzzylogic import combinators
from fuzzylogic.classes import Domain
from fuzzylogic.functions import R, S, triangular

# set parameters of the plot
pyplot.rc("figure", figsize=(10, 5))

# axis's limits
X_FROM, X_TO = 0, 1.1
Y_FROM, Y_TO = 0, 1.1

# define the domain for POI
poi = Domain("poi", X_FROM, X_TO, res=0.1)
# define fuzzy sets
poi.scarce = S(0.0, 0.2)
poi.few  = triangular(0.15, 0.4)
poi.few = poi.few.normalized()
poi.moderate = triangular(0.35,0.6)
poi.moderate = poi.moderate.normalized()
poi.many = triangular(0.55,0.8)
poi.many = poi.many.normalized()
poi.abundant = R(0.7,1.0)

# Add this domain to the FIS
@fis.domain
def define_domain() -> Domain:
    return poi

def plot():
    """Draw poi membership functions using pyplot"""
    poi.scarce.plot()
    poi.few.plot()
    poi.moderate.plot()
    poi.many.plot()
    poi.abundant.plot()

    # set y-axis limits
    pyplot.ylim(Y_FROM, Y_TO)
    pyplot.xlim(X_FROM, X_TO)
    # set axis ticks
    pyplot.yticks(numpy.arange(Y_FROM, Y_TO, step=0.1))
    pyplot.xticks(numpy.arange(X_FROM, X_TO, step=0.1))
    # add grid
    pyplot.grid()

    # name axis
    pyplot.xlabel("Number POIs")
    pyplot.ylabel("Truth value")

    # title plot
    pyplot.title("POI Fuzzy Sets")

    pyplot.legend(["Scarce", "Few", "Moderate", "Many", "Abundant"])
    # open window with plot
    pyplot.show()
