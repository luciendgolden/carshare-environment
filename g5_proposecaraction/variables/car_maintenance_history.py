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
DOMAIN_NAME = "car_maintenance_history"


# define the domain for Temperature
car_maintenance_history = Domain(DOMAIN_NAME, X_FROM, X_TO, res=0.1)
# define sets
car_maintenance_history.very_well = S(0, 3)
car_maintenance_history.well = triangular(2, 5)
car_maintenance_history.moderately  = triangular(4, 7)
car_maintenance_history.poorly = triangular(6, 9)
car_maintenance_history.very_poorly = R(8, 10) 

# Add this domain to the FIS
@fis.domain
def define_domain() -> Domain:
    return car_maintenance_history

def plot():
    """Draw the car_maintenance_history functions using pyplot"""
    car_maintenance_history.very_well.plot()
    car_maintenance_history.well.plot()
    car_maintenance_history.moderately.plot()
    car_maintenance_history.poorly.plot()
    car_maintenance_history.very_poorly.plot()

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
    pyplot.title("Car Maintenance History Fuzzy Sets")

    pyplot.legend(["Very_Well", "Well", "Moderately", "Poorly", "Very_Poorly"])
    # open window with plot
    pyplot.show()