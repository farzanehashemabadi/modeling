import os
import glob
import xlsxwriter
from xlsxwriter import Workbook

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

dir_name = os.path.dirname(__file__)


spill_num = 1

clippers_dir = r"C:\Users\Farzane\Desktop\Master97\Gnome modeling\Postprocessing\clipper"
clippers = glob.glob(clippers_dir + '/*.shp')
Grid_list = [0 for i in range(len(clippers))]
wbname = 'Result{}_{}.xlsx'.format(spill_num, positions[0])



for index, cfs in enumerate(clippers):
    print (index)
    print (Grid_list[index])
    workbook = xlsxwriter.Workbook(os.path.join(dir_name, 'FID{}_{}.xlsx'.format(spill_num, positions)))
    worksheet = workbook.add_worksheet () 
    for row in range (1, len(index)):
        worksheet.write(row, 1, index )


    
  

    





