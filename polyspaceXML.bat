@echo off

set polyspace_log_file=%1
set build_log_file=%2
set threshold_properties_file=%3
set output_file=%4

python "polyspaceXML.py" %polyspace_log_file% %build_log_file% %threshold_properties_file% %output_file%

pause