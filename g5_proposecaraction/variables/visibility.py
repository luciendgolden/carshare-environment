from matplotlib import pyplot
import numpy
from fis import fis
from fuzzylogic.classes import Domain
from fuzzylogic.functions import R, S, triangular

# set parameters of the plot
pyplot.rc("figure", figsize=(10, 5))

# axis's limits
X_FROM, X_TO = 20, 250
Y_FROM, Y_TO = 0, 1.1

# define the domain for Visibility
visibility = Domain("visibility", X_FROM, X_TO, res=0.1)
# define fuzzy sets
visibility.foggy = S(20, 80)
visibility.rainy = triangular(60, 120)
visibility.drizzle = triangular(110,150)
visibility.hazy = triangular(140,200)
visibility.clear = R(190,200)

# Add this domain to the FIS
@fis.domain
def define_domain() -> Domain:
    return visibility

def plot():
    """Draw visibility membership functions using pyplot"""
    visibility.foggy.plot()
    visibility.rainy.plot()
    visibility.drizzle.plot()
    visibility.hazy.plot()
    visibility.clear.plot()

    # set y-axis limits
    pyplot.ylim(Y_FROM, Y_TO)
    pyplot.xlim(X_FROM, X_TO)
    # set axis ticks
    pyplot.yticks(numpy.arange(Y_FROM, Y_TO, step=0.1))
    pyplot.xticks(numpy.arange(X_FROM, X_TO, step=20))
    # add grid
    pyplot.grid()

    # name axis
    pyplot.xlabel("meters")
    pyplot.ylabel("Truth value")

    # title plot
    pyplot.title("Visibility Fuzzy Sets")

    pyplot.legend(["Foggy", "Rainy", "Drizzle", "Hazy", "Clear"])
    # open window with plot
    pyplot.show()
