"""
Create plot for the fuzzy variable.
Usage:
    python create_plot.py [temperature|ride_time|visibility|etc]
"""
import sys, os, importlib
from utils.helpers import get_variable_ref as ref

# draw and open a plot. Second argument is the variable name
# the variable module must define plot() function for this to work
if len(sys.argv) > 1:
    variable = sys.argv[1]
    plot = getattr(ref(variable), 'plot')
    plot()