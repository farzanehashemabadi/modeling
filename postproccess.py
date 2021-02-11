import csv
import os
import glob
import arcpy
from arcpy import env



# setting my source and target geodatabase 
base_dir = os.path.dirname(__file__)

#setting my clip feature (which is a polygon)
clippers_dir = os.path.join(base_dir, 'clipper')
clippers = glob.glob(clippers_dir + '/*.shp')

# Iterate in base path and work with folders

arcpy.env.parallelProcessingFactor = "100%"

seasons = 'Winter'

src_dirs = [os.path.join(base_dir, seasons, 'Result {}'.format(spill_num)) for spill_num in range(1, 65)]



for src_dir in src_dirs:
    des_dir = os.path.join (src_dir, "clipped")
    if not os.path.exists(des_dir):
        os.mkdir(des_dir)
    
    #set a workspace    
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
            cell = arcpy.SearchCursor(cfs)
            for row1 in cell:
                Area = row1.getValue ('Area')
                ESI = row1.getValue ('ESI')
            print (index)
            

            #Calculate zigmaFID for each Grid in a Scenario
            shps = glob.glob (des_dir + '/*.shp')

            for shp in shps:
                mass = sum((r[0] for r in arcpy.da.SearchCursor(shp, ['Mass'])))
                Grid_list[index] += mass
            
            MCF= (Grid_list[index]) / (30 * Area)
            Risk1 = MCF * ESI
            print (Risk1)
            
            result_file = os.path.join(src_dir, "Risk.csv")
            with open ('result_file', 'w') as file:
                f = csv.writer (file)
                f.writerows ('index, Risk1')
        

               
            

            
          
        
        
        
#set(row[0] for row in arcpy.da.SearchCursor(shp, "FID"))
#count = len (fid)
         
#+= count
    
        
            

                




