
#############################################################################################
#                                                                                           #
#   A representation of "Johnny's air-conditioner" example from the "FuzzyLogic" slides.    #
#   Usage:                                                                                  #
#        python temperature_test.py [temp|speed]                                            #
#                                                                                           #
#############################################################################################

from matplotlib import pyplot
import numpy
import sys
from fuzzylogic.classes import Domain, Rule
from fuzzylogic.functions import R, S, triangular

# set parameters of the plot
pyplot.rc("figure", figsize=(10, 5))

# axis's limits
TEMP_X_FROM, TEMP_X_TO = 0, 30
SPEED_X_FROM, SPEED_X_TO = 0, 100
Y_FROM, Y_TO = 0, 1

# define the domain for Temperature
temperature = Domain("temperature", TEMP_X_FROM, TEMP_X_TO, res=0.1)
# define sets
temperature.cold = S(0, 10)
temperature.cool = triangular(0, 17.5, c=12.5) # parameter "c" is the peak of the triangle, default is the middle
temperature.pleasant = triangular(15,20)
temperature.warm = triangular(17.5,27.5)
temperature.hot = R(25,30)

# define the domain for Speed
speed = Domain("speed", SPEED_X_FROM, SPEED_X_TO, res=0.1)
# define sets
speed.minimal = S(0, 30)
speed.slow = triangular(10,50)
speed.medium = triangular(40, 60)
speed.fast = triangular(50, 90)
speed.blast = R(70, 100)


# calculate membership values for input value 8
result = temperature(8)
# print the values for every set
for set in result:
    print(f"{set}: {result[set]}")

# Define rules
# Why the coma? Read: https://github.com/Python-Fuzzylogic/fuzzylogic/discussions/26
    # tl;dr the first argument must be iterable
R1 = Rule({(temperature.cold,): speed.minimal})
R2 = Rule({(temperature.cool,): speed.slow})
R3 = Rule({(temperature.pleasant,): speed.medium})
R4 = Rule({(temperature.warm,): speed.fast})
R5 = Rule({(temperature.hot,): speed.blast})

# Combine rules into a ruleset
rules = R1 | R2 | R3 | R4 | R5      # method 1
rules = sum([R1, R2, R3, R4, R5])   # method 2 (they are identical)

# Set input values for domains
values = {temperature: 8}

# Output ruleset results
print(R1(values))
print(R2(values))
print(R3(values))        # I don't see a way to get the actual weights. The Rule.__call__ function includes defuzzyfication with COG...
print(R4(values))        #... If we need weights, I guess we can fork the library -- Oleksii
print(R5(values))

# Output the defuzzified value using COG
print(rules(values))


def plot_temp():
    """Draw the temperature functions using pyplot"""
    temperature.cold.plot()
    temperature.cool.plot()
    temperature.pleasant.plot()
    temperature.warm.plot()
    temperature.hot.plot()

    # set y-axis limits
    pyplot.ylim(-0.1,1.1)
    # set axis ticks
    pyplot.yticks(numpy.arange(Y_FROM, Y_TO + 0.1, step=0.1))
    pyplot.xticks(numpy.arange(TEMP_X_FROM, TEMP_X_TO + 1, step=2.5))
    # add grid
    pyplot.grid()

def plot_speed():
    """Draw the speed functions using pyplot"""
    speed.minimal.plot()
    speed.slow.plot()
    speed.medium.plot()
    speed.fast.plot()
    speed.blast.plot()

    # set y-axis limits
    pyplot.ylim(-0.1,1.1)
    # set axis ticks
    pyplot.yticks(numpy.arange(Y_FROM, Y_TO + 0.1, step=0.1))
    pyplot.xticks(numpy.arange(SPEED_X_FROM, SPEED_X_TO + 1, step=10))
    # add grid
    pyplot.grid()

# Use either plot_temp() or plot_speed() to draw a corresponding plot
if len(sys.argv) == 2:
    if sys.argv[1] == "temp":
        plot_temp()
        pyplot.show() # Open a window with the plot
    elif sys.argv[1] == "speed":
        plot_speed()
        pyplot.show() # Open a window with the plot
else:
    print("Plot wasn't created. To create and show it, use \"temp\" or \"speed\" as first command line argument.")
