


import os

import shutil
from datetime import datetime, timedelta
from gnome.basic_types import datetime_value_2d

import gnome
import numpy as np

from gnome import basic_types

from gnome import scripting
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
          


# latin hypercube sampling

from pyDOE import lhs 
from scipy.stats.distributions import triang,uniform

#starttime from days of year
startdays = lhs(1,samples=10)

startdays = uniform(loc=1,scale=90).ppf(startdays)

str_days = startdays.astype(int)

#print ("start days" + ":",str_days.astype(int))

spill_num = 1


##########################

#spillduration from triang_distributin(5,50,30)

spilltimes = lhs(10,samples=10)

for i in range(10):
    spilltimes[:,i] = triang(loc=5,scale=45,c=0.556).ppf(spilltimes[:,i])


spill_dur = spilltimes.astype(int)

#print ("spill duration" + ":",spill_dur)






            
def run (position, startday, spilldur):
    #define base directory
    path='C:/Users/Farzane/Desktop/Master97/Gnome modeling/2016'
    
    base_dir = os.path.dirname(__file__)

    water = Water (temperature=290.367946, salinity=35.0)

    wind = Wind (filename= 'C:/Users/Farzane/Desktop/Master97/Gnome modeling/2016/wind2016.txt')

    waves = Waves(water, wind)


    def make_model(images_dir=os.path.join(base_dir, 'images')):
        print ('initializing the model')

        #print (start_date)

        start_time = start_date

        model = Model(start_time=start_time, duration=timedelta(days=30), 
                      #weathering_substeps = 6,
                      time_step=24 * 3600,
                      uncertain=True)

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

        #print ("adding netcdf output")
     #   netcdf_output_file = os.path.join(base_dir,'gulf_output.nc')
      #scripting.remove_netcdf(netcdf_output_file)
    #    model.outputters += NetCDFOutput(netcdf_output_file, which_data='all',
     #                                    output_timestep=timedelta(hours=24))


        print ("adding shapefile output")

        

        # with open("Result {}".format(spill_num), "w") as fp:
            # fp.write("text")
        
        dir_name = "Result {}".format(spill_num)
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

        for b in range(1, 31, 1):
            model.outputters += ShapeOutput(os.path.join(base_dir, dir_name, 'gnome_result{id}'.format(id=b)),
                                        zip_output=False,
                                        output_timestep=timedelta(days=b))    

        #
        # Set up the movers:
        #

        print ('adding a RandomMover:')
        model.movers += RandomMover(diffusion_coef=10000)

        print ('adding a simple wind mover:')
    #    model.movers += constant_wind_mover(5, 315, units='m/s')

        wind_file = get_datafile(os.path.join(base_dir, 'nc3ECMWF2016.nc'))
        model.movers += GridWindMover(wind_file)
                                         

        print ('adding a current mover:')

        # # this is NEMO currents

        curr_file = get_datafile(os.path.join(base_dir, 'current2016nc3.nc'))
        model.movers += GridCurrentMover(curr_file,
                                         num_method='Euler');


            # #
        # # Add some spills (sources of elements)
        # #

        print ('adding one spill')

        spill = point_line_release_spill(num_elements=1000,
                                                 amount=4000 * spilldur, units='m^3',
                                                 start_position = position,
                                                 release_time = start_time,
                                                 substance =( u'BAHRGANSAR, OIL & GAS'))
        model.spills += spill


        
        print ('adding weatherers and cleanup options:')

        model.environment += [water, wind, waves]

        model.weatherers += Evaporation(water, wind)
        model.weatherers += Emulsification(waves)
        model.weatherers += NaturalDispersion(waves, water)
        model.full_run()
        return model
    return make_model()
     





#loop for scenarios
for i in positions:
    for index, j in enumerate(str_days):
        start_date = datetime.strptime('2016 {}'.format (j[0]), '%Y %j')
        for z in spill_dur[index]:
            run(i, start_date, z)
            spill_num += 1
