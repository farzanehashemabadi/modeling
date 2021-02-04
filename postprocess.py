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

src_dir = os.path.join (base_direct, "Results_winter2016")



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
        

        

        

            


        
        

        
    
        




        






       
       
        
        


    
    


   
        
    
