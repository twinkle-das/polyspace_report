@echo off

set polyspace_log_file=%1
set build_log_file=%2

python "polyViolationDb.py" %polyspace_log_file% %build_log_file%

pause