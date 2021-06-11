@echo off

set polyspace_log_file=%1
set build_log_file=%2
set output_file=%3

python "polyspace.py" %polyspace_log_file% %build_log_file% %output_file%

pause