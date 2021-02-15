$a = Start-Process - C:/Python27/ArcGIS10.8/python -ArgumentList ("testprocess.py","1")
$b = Start-Process - C:/Python27/ArcGIS10.8/python -ArgumentList ("testprocess.py","2")


$a | wait-process
$b | wait-process