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

positions = [(49.68, 29.94, 0),
             (49.71, 30.12, 0),
             (49.58, 29.53, 0),
             (49.60, 29.88, 0),
             (49.66, 29.01, 0),
             (50.44, 28.96, 0),
             (49.80, 28.27, 0),
             (54.06, 25.75, 0),
             (54.79, 25.69, 0),
             (54.72, 25.89, 0),
             (54.02, 25.54, 0),
             (54.31, 25.48, 0),
             (52.93, 25.53, 0),
             (53.12, 25.96, 0),
             (52.78, 25.92, 0),
             (52.53, 26.31, 0)]

seasons = ['Winter', 'Summer']

src_dirs = [os.path.join(base_dir, seasons, str(positions),'Spillnum {}'.format(spill_num) for spill_num in (range(1,101))]



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
    for index, cfs in enumerate(clippers):
        for fc in fclist:
            src_file_dir, src_file_name = src_dir, fc
            clipper_dir, clipper_name = os.path.split(cfs)
            clipper_name = src_file_name.split('.')[0] + "_" + clipper_name 
            
            output_dir = os.path.join(des_dir , clipper_name)
            clipped = arcpy.Clip_analysis(fc,cfs,output_dir)
            cell = arcpy.SearchCursor(cfs)
            for row1 in cell:
                Area = row1.getValue ('Area')
                ESI = row1.getValue ('ESI')
           
            #Calculate zigmaFID for each Grid in a Scenario
            x = re.search('gnome_result(.*)\.shp', src_file_name)
            name = '/*{}_{}'.format(x.group(1), clipper_id)
            #print(name)
            shp = glob.glob (des_dir + name)[0]
            #print (shps)
            mass = sum((r[0] for r in arcpy.da.SearchCursor(shp, ['Mass'])))
            Grid_list[index] += mass

        MCF= (Grid_list[index]) / (30 * Area)
        Risk1 = MCF * ESI
        print (index, Risk1)
               
        result_file = os.path.join(src_dir, "Risk.csv")
        with open (result_file, 'a') as file:
            f = csv.writer (file)
            f.writerow([index, Risk1])

            
          
        
        
        
#set(row[0] for row in arcpy.da.SearchCursor(shp, "FID"))
#count = len (fid)
         
#+= count
    
        
            

                




