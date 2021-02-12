import threading
import Queue
import time
import xlsxwriter
import os
import shutil
from datetime import datetime, timedelta
import _strptime
from gnome.basic_types import datetime_value_2d

import gnome
import numpy as np

from gnome import basic_types

from gnome import scripting as gs
from gnome import utilities
from gnome.utilities.remote_data import get_datafile
from gnome.utilities.inf_datetime import InfDateTime


from gnome.model import Model

from gnome.environment import Wind, WaterSchema, Waves, Water
from gnome.maps import MapFromBNA
from gnome.spill import point_line_release_spill
from gnome.movers import RandomMover, GridWindMover, GridCurrentMover


from gnome.outputters import (Renderer,
                               NetCDFOutput,
                              ShapeOutput)
from gnome.outputters import WeatheringOutput

from gnome.basic_types import numerical_methods

from gnome.weatherers import (Emulsification,
                              Evaporation,
                              NaturalDispersion,
                              #ChemicalDispersion,
                              #Burn,
                              #Skimmer,
                              WeatheringData)



#Position of wells

positions1 = [(49.68, 29.94, 0),
             (49.71, 30.12, 0),
             (49.58, 29.53, 0),
             (49.60, 29.88, 0),
             (49.66, 29.01, 0),
             (50.44, 28.96, 0),
             (49.80, 28.27, 0),
             (54.06, 25.75, 0)]

positions2=[(54.79, 25.69, 0),
             (54.72, 25.89, 0),
             (54.02, 25.54, 0),
             (54.31, 25.48, 0),
             (52.93, 25.53, 0),
             (53.12, 25.96, 0),
             (52.78, 25.92, 0),
             (52.53, 26.31, 0)]
          

substances1 = [u'BAHRGANSAR, OIL & GAS',
u'BAHRGANSAR, OIL & GAS',
u'NOWRUZ',
u'SOROOSH',
u'ABOOZAR',
u'DORROOD',
u'FOROOZAN',
u'SIRRI']

substances2 =[u'SIRRI',
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

spilltimes = lhs(1,samples=1)

for i in range(1):
    spilltimes[:,i] = triang(loc=5,scale=45,c=0.556).ppf(spilltimes[:,i])


spill_dur = spilltimes.astype(int)

#print ("spill duration" + ":",spill_dur)

#define base directory
base_dir = os.path.dirname(__file__)


# !!!!!!!Item should chenged!!!!!!!!!
water = Water (temperature=290.367946, salinity=35.0)
            
def run (position, sub, startday, spilldur, season, spill_num):
   
    

    # !!!!!!!Item should chenged!!!!!!!!!
    wind = Wind (filename= os.path.join(base_dir, 'wind2016.txt'))

    waves = Waves ()


    def make_model(images_dir=os.path.join(base_dir, 'images')):
        print ('initializing the model')

        #print (start_date)

        start_time = startday

        model = Model(start_time=start_time, duration=timedelta(days=30), 
                      #weathering_substeps = 6,
                      time_step=24 * 3600,
                      uncertain=False)

        mapfile = get_datafile(os.path.join(base_dir,'gulf.bna'))

        #mapfile='gulf.bna'

        print ('adding the map')
        model.map = MapFromBNA(mapfile, refloat_halflife=6)  # hours

        #
        # Add the outputters -- render to images, and save out as netCDF
        #

        print ('adding renderer')
        #model.outputters += Renderer(mapfile,
                                    # images_dir,
                                     #size=(800, 600),
                                     #draw_back_to_fore=True)

        

        print ("adding shapefile output")

         # with open("Result {}".format(spill_num), "w") as fp:
         # fp.write("text")
        
        dir_name = os.path.join (base_dir, season, str(position), "Spillnum {}".format(spill_num))
        
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        
        #os.makedirs(dir_name, exist_ok =True)

        for i in range(1, 31, 1):
            model.outputters += ShapeOutput(os.path.join(dir_name, 'gnome_result {id}'.format(id=i)),
                                        zip_output=False,
                                        output_timestep=timedelta(days=i))    

        #
        # Set up the movers:
        #

        print ('adding a RandomMover:')
        model.movers += RandomMover(diffusion_coef=10000)

        print ('adding a simple wind mover:')
    

        
        wind_file = get_datafile(os.path.join(base_dir, 'ECMWF.nc'))
        model.movers += GridWindMover(wind_file)

                                                  

        print ('adding a current mover:')

        # # this is NEMO currents

        curr_file = get_datafile(os.path.join(base_dir, 'Current.nc'))
        model.movers += GridCurrentMover(curr_file,
                                         num_method='Euler');


        
        # # Add some spills (sources of elements)
        

        print ('adding one spill')

        spill = point_line_release_spill(num_elements=1000,
                                                 amount=3200000000 * spilldur, units='grams',
                                                 start_position = position,
                                                 release_time = start_time,
                                                 substance = (sub))
        model.spills += spill

        ####### open excel file 
        print ('adding Excel file')
      
        workbook = xlsxwriter.Workbook(os.path.join(dir_name, 'Result {}_{}.xlsx'.format(spill_num, position)))
        worksheet = workbook.add_worksheet () 
        worksheet.write ('A1', spilldur*3200)
        workbook.close()

        
        print ('adding weatherers and cleanup options:')

        model.environment += [water,wind, waves]
        model.weatherers += Evaporation()
        model.weatherers += Emulsification()
        model.weatherers += NaturalDispersion()
        model.full_run()
        return model
    return make_model()
     


#loop for scenarios

def senarios (positions, substances, str_days, str_times, spill_dur, season, startspill_num):
    spill_num = startspill_num
    for i in positions:
        for ss in substances:
            for index, j in enumerate(str_days):
                # !!!!!!!Item should chenged!!!!!!!!!
                start_date = datetime.strptime('2016 {}'.format (j[0]), '%Y %j')
                for t in str_times[index]:
                    new_start_date = start_date.replace (hour = t)
                    for z in spill_dur[index]:
                        run(i, ss, new_start_date, z, season, spill_num)
                        spill_num += 1





if __name__ == "__main__":
    #Creating Thread
    t1 = threading.Thread (target=senarios, args=(positions1, substances1, str_days, str_times, spill_dur, 'Winter', 1))
    t2 = threading.Thread (target=senarios, args=(positions2, substances2, str_days, str_times, spill_dur, 'Winter', 101))
    

    # Starting thread1
    t1.start()
    # Starting thread2
    t2.start()
    #starttime from days of Summer
    startdays = lhs(1,samples=1)

    startdays = uniform(loc=182,scale=92).ppf(startdays)

    str_days = startdays.astype(int)
    #!!!!!!!! Item should changed!!!!!!
    water = Water (temperature=311.3736, salinity=35.0)

    t3 = threading.Thread (target=senarios, args=(positions1, substances1, str_days, str_times, spill_dur, 'Summer', 201))
    t4 = threading.Thread (target=senarios, args=(positions2, substances2, str_days, str_times, spill_dur, 'Summer', 301))
    # Starting thread3
    t3.start()
    # Starting thread4
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()