@echo off

set polyspace_log_file=%1
set threshold_properties_file=%2
set build_log_file=%3

python "checkViolation.py" %polyspace_log_file% %threshold_properties_file% %build_log_file%

pause