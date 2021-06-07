@echo off

set input_file_path=%1
set output_file_path=%2

python "polyspaceXML.py" %input_file_path% %output_file_path%

pause