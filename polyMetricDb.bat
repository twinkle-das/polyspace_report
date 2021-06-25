@echo off

set polyspace_log_file=%1
set build_log_file=%2
set threshold_props_file=%3

python "polyMetricDb.py" %polyspace_log_file% %build_log_file% %threshold_props_file%

pause