$a = Start-Process -NoNewWindow python -ArgumentList ("WinterScript.py","1")
$b = Start-Process -NoNewWindow python -ArgumentList ("WinterScript.py","2")
$c = Start-Process -NoNewWindow python -ArgumentList ("SummerScript.py","3")
$d = Start-Process -NoNewWindow python -ArgumentList ("SummerScript.py","4")

$a | wait-process
$b | wait-process
$c | wait-process
$d | wait-process
