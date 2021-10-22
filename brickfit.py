from matplotlib import pyplot
from scipy.optimize import curve_fit

## DATA SECTION ##

# normalized demand - 3y delay
r_values_01 = [    0.45,    0.46,    0.53,    0.72,    1.30,    1.99,    2.56,    2.17,    1.76 ]
p_values_01 = [ 1526.42, 1706.32, 1757.71, 2025.12, 2287.55, 2887.63, 3305.77, 3474.04, 3295.88 ]

## /DATA SECTION ##

# the first argument is the data vector
# the others are the parameters to be estimated

def objective(r, peq, b, alpha):
        return (peq-b) + b*(r**alpha)

# initial parameters

# even with very different seed values it converges to ~ the same
par0 = [ 2300, 2000, 0.5 ]

popt, _ = curve_fit(objective, r_values_01, p_values_01, p0 = par0)
peq, b, alpha = popt

print('with normalized demand')
print(peq, b, alpha)
