   
$a = Start-Process -NoNewWindow C:\Python27\ArcGIS10.8\python -ArgumentList ("testprocess.py","1")
$b = Start-Process -NoNewWindow C:\Python27\ArcGIS10.8\python -ArgumentList ("testprocess.py","2")
$c = Start-Process -NoNewWindow C:\Python27\ArcGIS10.8\python -ArgumentList ("testprocess.py","3")
$d = Start-Process -NoNewWindow C:\Python27\ArcGIS10.8\python -ArgumentList ("testprocess.py","4")

$a | wait-process
$b | wait-process
$c | wait-process
$d | wait-process