from matplotlib import pyplot
import numpy
from fuzzylogic.classes import Domain
from fuzzylogic.functions import R, S, triangular
from fis import fis

# set parameters of the plot
pyplot.rc("figure", figsize=(10, 5))

# axis's limits
X_FROM, X_TO = 0, 10
Y_FROM, Y_TO = 0, 1
DOMAIN_NAME = "car_goes_for_maintenance"


# define the domain for Temperature
car_goes_for_maintenance = Domain(DOMAIN_NAME, X_FROM, X_TO, res=0.1)
# define sets
car_goes_for_maintenance.not_recommended = S(0, 4)
car_goes_for_maintenance.recommended = triangular(3, 7)
car_goes_for_maintenance.highly_recommended  = R(6, 10)

# Add this domain to the FIS
@fis.domain
def define_domain() -> Domain:
    return car_goes_for_maintenance

def plot():
    """Draw the car_goes_for_maintenance functions using pyplot"""
    car_goes_for_maintenance.not_recommended.plot()
    car_goes_for_maintenance.recommended.plot()
    car_goes_for_maintenance.highly_recommended.plot()

    # set y-axis limits
    pyplot.ylim(Y_FROM, Y_TO)
    pyplot.xlim(X_FROM, X_TO)
    # set axis ticks
    pyplot.yticks(numpy.arange(Y_FROM, Y_TO, step=0.1))
    pyplot.xticks(numpy.arange(X_FROM, X_TO, step=2))
    # add grid
    pyplot.grid()

    # name axis
    pyplot.xlabel("Car Age")
    pyplot.ylabel("Truth value")

    # title plot
    pyplot.title("Car Goes for Maintenance Fuzzy Sets")

    pyplot.legend(["Not Recommended", "Recommended", "Highly Recommended"])
    # open window with plot
    pyplot.show()