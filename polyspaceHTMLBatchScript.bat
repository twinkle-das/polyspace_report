@echo off

set xsl_file_path=%1
set xml_file_path=%2
set output_file_path=%3

python "polyspaceSummary.py" %xsl_file_path% %xml_file_path% %output_file_path%

pause