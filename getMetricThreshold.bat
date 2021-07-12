@echo off

set code_metric_file=%1
set threshold_properties_file=%2

python "getMetricThreshold.py" %code_metric_file% %threshold_properties_file%

pause