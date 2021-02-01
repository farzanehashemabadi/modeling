from datetime import datetime

import numpy as np

from pyDOE import lhs 
from scipy.stats.distributions import triang,uniform



#Position of wells

positions = [(49.68, 29.94, 0)]
             #(49.71, 30.12, 0),
             #(49.58, 29.53, 0),
             #(49.60, 29.88, 0),
             #(49.66, 29.01, 0),
             #(50.44, 28.96, 0),
             #(49.80, 28.27, 0),
             #(54.06, 25.75, 0),
             #(54.79, 25.69, 0),
             #(54.72, 25.89, 0),
             #(54.02, 25.54, 0),
             #(54.31, 25.48, 0),
             #(52.93, 25.53, 0),
             #(53.12, 25.96, 0),
             #(52.78, 25.92, 0),
             #(52.53, 26.31, 0)]
             


#latin hypercube sampling


#starttime from days of year

startdays = lhs(1,samples=1)

startdays = uniform(loc=1,scale=91).ppf(startdays)

str_days = startdays.astype(int)

#print ("start days" + ":",str_days.astype(int))
#############################

starttimes = lhs(1,samples=1)

starttimes = uniform(loc=0,scale=24).ppf(starttimes)

str_times = starttimes.astype(int)

#print ("start times" + ":",str_times.astype(int))

##########################

#spillduration from triang_distributin(5,50,30)

spilltimes = lhs(10,samples=2)

for i in range(10):
    spilltimes[:,i] = triang(loc=5,scale=45,c=0.556).ppf(spilltimes[:,i])


spill_dur = spilltimes.astype(int)

#print ("spill duration" + ":",spill_dur)
#########################################

#loop for scenarios

#spill_num=[]

for i in positions:
    for index, d in enumerate(str_days):
        start_date = datetime.strptime('2016 {}'.format (d[0]), '%Y %j')
        for t in str_times[index]:
            for z in spill_dur[index]:
                print (i, start_date, t, z)




    











