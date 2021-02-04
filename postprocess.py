### Clip and calculate Risk value ###

import os
import arcpy
#import shapefile
import glob
from arcpy import env

    
# setting my source and target geodatabase 
base_dir = os.path.dirname(__file__)

#setting my clip feature (which is a polygon)
clippers_dir = os.path.join (base_direct, "clipper")
clippers = glob.glob(clippers_dir + '/*.shp')

# Iterate in base path and work with folders

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

src_dirs = [os.path.join(base_direct, f'Result{spill_num}_{position}') for spill_num, position in zip(range(1,101), range(1,17))]



for src_dir in src_dirs:
    des_dir = os.path.join (src_dir, "clipped")
    if not os.path.exists(des_dir):
                os.mkdir(des_dir)
    #r"C:\Users\Farzane\Desktop\Master97\Gnome modeling\Postprocessing\clipped"





    # set a workspace    
    arcpy.env.workspace = src_dir

    fclist = arcpy.ListFeatureClasses()

    # make list of Grids
    Grid_list = [0 for i in range(len(clippers))]


    ###########################################          

    for fc in fclist:
        src_file_dir, src_file_name = src_dir, fc
        for index, cfs in enumerate(clippers):

            clipper_dir, clipper_name = os.path.split(cfs)
            clipper_name = src_file_name.split('.')[0] + "_" + clipper_name 
            output_dir = os.path.join(des_dir , clipper_name)
            clipped = arcpy.Clip_analysis(fc,cfs,output_dir)

            #Calculate zigmaFID for each Grid in a Scenario
            shps = glob.glob (des_dir + '/*.shp')

            for shp in shps:
                fid = set(row[0] for row in arcpy.da.SearchCursor(shp, "FID"))
                count = len (fid)
                #print (count)
                Grid_list[index] += count
                #print (Grid_list[index])





            #import ESI from Grids
            #rows = arcpy.SearchCursor(cfs)
            #Loop through each row in the attributes
            #for row in rows:
            #    Esi = row.getValue("ESI")
                #print (Esi)


            #Calculate Risk Value and add in Attribute table of Grids

            #cur = arcpy.UpdateCursor (cfs)

            #for rad in cur:
                #Riskvalue = (Esi * Grid_list[index] * freq[0])
                #rad.setValue ('Risk_Value', Riskvalue)
                #cur.updateRow (rad)
