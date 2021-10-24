import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pyplot
from scipy.optimize import curve_fit

## DATA SECTION ##

# maximum delay in semesters
MIN_DELAY = 6
MAX_DELAY = 8

# normalized R vs Price on an yearly series
R_VALUES = [ 0.45,    0.46,    0.53,    0.72,    1.30,    1.99,    2.56,    2.17,    1.76,    1.68,    1.46,    1.35 ]
P_VALUES = [ 2250, 1923.08, 1711.81, 1526.42, 1706.32, 1757.71, 2025.12, 2287.55, 2887.63, 3305.77, 3474.04, 3295.88 ]

BASE_YEAR = 2010
NR_YEARS  = 12

## /DATA SECTION ##

# the first argument is the data vector
# the others are the parameters to be estimated

def objective(r, peq, b, alpha):
        return (peq-b) + b*(r**alpha)

def get_delayed_lists(r, p, d):
    for j in range (0, d):
        p.pop(0)
        r.pop()

    #print(r)
    #print(p)
    return r, p

def evaluate ( r, p, peq, b, alpha ):

    total  = 0
    max_dev = 0
    length = len(p)
    values = []

    # we use the squared deviation so that the error can be summed and averaged
    for j in range(0, length):
        estimation = objective(r[j], peq, b, alpha)
        values.append(estimation)
        cur_dev =  ( p[j] - estimation )**2
        total = total + cur_dev
        if cur_dev > max_dev:
            max_dev = cur_dev

    # we need to apply the square root to be back to proper units
    return values, np.sqrt(total) / length, np.sqrt(max_dev)

def pad_data ( data, target_size, element, left = True ):

    for j in range( target_size - len(data) ):
        if left:
            data.insert(0, element)
        else:
            data.append(element)

    return data

# initial parameters
par0 = [ 2300, 2000, 0.5 ]

# now let's try some interpolation to gain delay space and vary the delay

r_list = []
p_list = []

length=len(R_VALUES)

# create new lists with extra points that will be interpolated
t_values = []

for j in range(0, length):

    r_list.append(R_VALUES[j])
    r_list.append(0)

    p_list.append(P_VALUES[j])
    p_list.append(0)

# remove the last element, which is set to zero on the above code
r_list.pop()
p_list.pop()

# produce lists with interpolated values

for j in range(0, length-1):
    k = 2*j + 1
    r_list[k] = 0.5 * (r_list[k-1] + r_list[k+1] )
    p_list[k] = 0.5 * (p_list[k-1] + p_list[k+1] )

# try to fit with different delays
# note: the more delay, the more data we lose for the fit, so we need a balance if the series is short

# prepare the t axis
for j in range(0, len(r_list)):

    # to be used in the plots
    t_value  = BASE_YEAR + 0.5 * j
    t_values.append(t_value)

for d in range (MIN_DELAY, MAX_DELAY+1):
    
    # call function that returns the delayed lists
    r_delayed, p_delayed = get_delayed_lists(r_list.copy(), p_list.copy(), d)

    plt.xkcd() # <3 <3 <3
    plt.title( 'Lisboa')
    plt.ylabel('EUR')

    try:
        popt, pcov = curve_fit(objective, r_delayed, p_delayed, p0 = par0)
        peq, b, alpha = popt
        p_estimation, error, max_error = evaluate ( r_delayed, p_delayed, peq, b, alpha)

        pad_data(p_estimation, len(t_values), None, True)

        print('with delay', d, 'average error', error, 'maximum error', max_error, 'points', length-0.5*d )
        print(peq, b, alpha, '\n')

        my_label = 'delay ' + str(d)
        plt.plot(t_values, p_estimation, label=my_label )

    except Exception as ex:
        print('could not fit for delay', d, '\n')
        print(ex)

plt.plot(t_values, p_list, label='pm2')

plt.legend(loc='upper right')
plt.show()
# TODO: plots the known points and the candidate curves
