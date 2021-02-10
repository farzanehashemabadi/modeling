import threading
import Queue
import time
#import xlsxwriter
import os
#import shutil
from datetime import datetime, timedelta







#Position of wells

positions1 = [(49.68, 29.94, 0),
             (49.71, 30.12, 0),
             (49.58, 29.53, 0),
             (49.60, 29.88, 0),
             (49.66, 29.01, 0),
             (50.44, 28.96, 0),
             (49.80, 28.27, 0),
             (54.06, 25.75, 0)]

positions2 = [(54.79, 25.69, 0),
             (54.72, 25.89, 0),
             (54.02, 25.54, 0),
             (54.31, 25.48, 0),
             (52.93, 25.53, 0),
             (53.12, 25.96, 0),
             (52.78, 25.92, 0),
             (52.53, 26.31, 0)]
          

substances = [u'BAHRGANSAR, OIL & GAS',
u'BAHRGANSAR, OIL & GAS',
u'NOWRUZ',
u'SOROOSH',
u'ABOOZAR',
u'DORROOD',
u'FOROOZAN',
u'SIRRI',
u'SIRRI',
u'SIRRI',
u'SIRRI',
u'SIRRI',
u'SALMON',
u'SALMON',
u'SALMON',
u'SALMON']


# latin hypercube sampling

from pyDOE import lhs 
from scipy.stats.distributions import triang,uniform

#starttime from days of winter
startdays = lhs(1,samples=10)

startdays = uniform(loc=1,scale=91).ppf(startdays)

str_days = startdays.astype(int)

#print ("start days" + ":",str_days.astype(int))

spill_num = 1
#############################

starttimes = lhs(1,samples=10)

starttimes = uniform(loc=0,scale=24).ppf(starttimes)

str_times = starttimes.astype(int)

#print ("start times" + ":",str_times.astype(int))


##########################

#spillduration from triang_distributin(5,50,30)

spilltimes = lhs(10,samples=10)

for i in range(10):
    spilltimes[:,i] = triang(loc=5,scale=45,c=0.556).ppf(spilltimes[:,i])


spill_dur = spilltimes.astype(int)


#print ("spill duration" + ":",spill_dur)


#filepath = os.path.join(base_dir, 'Scenarios.txt')
#with open(filepath, 'w') as f:
#    f.write("%s\n" % str_days)
#    f.write("%s\n" %str_times)   
#    f.write("%s\n" %spill_dur)
#f.close() 

base_dir = os.path.dirname(__file__)
            
def run (position, sub, startday, spilldur, season):
    print (position, sub, startday, spilldur, season)
    #define base directory
    #path='/home/farzaneh.hashemabadi.student/2016'
     





#loop for scenarios
#Class of Threading
class OperatorThread(threading.Thread):
    def __init__(self, q):
        threading.Thread.__init__(self)
        self.q = q
    def senarios (positions1, substances, str_days, str_times, spill_dur, season):
        print ("Inside Thread")
        for i in positions1:
            for ss in substances:
                for index, j in enumerate(str_days):
                    start_date = datetime.strptime('2016 {}'.format (j[0]), '%Y %j')
                    for t in str_times[index]:
                        new_start_date = start_date.replace (hour = t)
                        for z in spill_dur[index]:
                            run(i, ss, new_start_date, z, season)
    def senarios (positions2, substances, str_days, str_times, spill_dur, season):
        print ("Inside Thread")
        for i in positions2:
            for ss in substances:
                for index, j in enumerate(str_days):
                    start_date = datetime.strptime('2016 {}'.format (j[0]), '%Y %j')
                    for t in str_times[index]:
                        new_start_date = start_date.replace (hour = t)
                        for z in spill_dur[index]:
                            run(i, ss, new_start_date, z, season)
                            
    senarios (positions1, substances, str_days, str_times, spill_dur, 'Winter')
    senarios (positions2, substances, str_days, str_times, spill_dur, 'Winter')

    #starttime from days of Summer
    startdays = lhs(1,samples=10)

    startdays = uniform(loc=182,scale=91).ppf(startdays)

    str_days = startdays.astype(int)

    senarios (positions1, substances, str_days, str_times, spill_dur, 'Summer')
    senarios (positions2, substances, str_days, str_times, spill_dur, 'Summer')


q = Queue.Queue()
for i in range (4):
    print("Creating thread number %s" %i)
    t = OperatorThread(q)
    t.setDaemon(True)
    t.start()
    print ("Theard")

