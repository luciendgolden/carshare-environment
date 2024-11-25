
##########################################################################
#                                                                        #
#   A representation of "Height" example from the "FuzzyLogic" slides.   #
#                                                                        #
##########################################################################

from matplotlib import pyplot
from fuzzylogic.classes import Domain
from fuzzylogic.functions import R, S, triangular

# set parameters of the plot
pyplot.rc("figure", figsize=(10, 10)) 

# Define domain
Height = Domain("height", 150, 210, res=0.1)

# S(x,y) defines a linear descending function
Height.short = S(160,170)
# add the function to the plot
Height.short.plot()

# R(x,y) defins a linear ascending function
Height.tall = R(180,190)
Height.tall.plot()

# triangular(x,y) defines a triangular function
Height.average = triangular(165, 185)
Height.average.plot()

# calculate membership values for input value 184
result = Height(184)
# print the values for every set
for set in result:
    print(f"{set}: {result[set]}")

# draw graph (a window should pop up after executing this script)
pyplot.show()
