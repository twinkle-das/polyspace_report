import time
from Db_Helper import DB_Helper
import datetime
import sys
import re
from collections import defaultdict
from xml.dom import minidom

polyspacelog_file = sys.argv[1]
build_log_file = sys.argv[2]
threshold_properties_file = sys.argv[3]
db_helper = DB_Helper()

db_helper.execute_query("DROP TABLE IF EXISTS CI_metrics")

sql = '''CREATE TABLE CI_metrics(
    id serial PRIMARY KEY,
    jobname varchar(255) NOT NULL,
    build_id int NOT NULL,
    violation int NOT NULL,
    cyclomatic_complexity int NOT NULL,
    language_scope decimal NOT NULL,
    goto_statements int NOT NULL,
    return_statements int NOT NULL,
    modified_on TIMESTAMP NOT NULL
)'''

db_helper.execute_query(sql)
print("Table created successfully........")

doc = minidom.Document()
root = doc.createElement("root")
doc.appendChild(root)

with open(build_log_file, "r") as bl_file:
    line = bl_file.readline()
    while line:
        if line.__contains__("~"):
            tag, data = line.split("~")
            if tag == "Build_ID":
                bid_value = data
            if tag == "Job_Name":
                job_name_value = data
        line = bl_file.readline()

with open(threshold_properties_file, "r") as tp_file:
    map = {}
    line = tp_file.readline()
    while line:
        line = line.strip()
        if line.__contains__("="):
            property, value = line.split("=")
            if value.__contains__("-"):
                min_val, max_val = value.split("-")
                map[str(property.strip())] = max_val
            else:
                map[str(property.strip())] = value.strip()
        line = tp_file.readline()
    cc_val = int(map.get("CC"))
    ls_val = float(map.get("LS"))
    gs_val = int(map.get("GS"))
    rs_val = int(map.get("RS"))

with open(polyspacelog_file, "r") as pl_file:
    line = pl_file.readline()
    total_violation = 0
    while line:
        line = line.strip()
        if line.__contains__("rules violated"):
            words = line.split()
            total_violation = int(words[0])
        line = pl_file.readline()
ts = time.time()
timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
db_helper.execute_query(f'''INSERT INTO CI_metrics(
    JOBNAME,
    BUILD_ID,
    VIOLATION, 
    CYCLOMATIC_COMPLEXITY, 
    LANGUAGE_SCOPE, 
    GOTO_STATEMENTS, 
    RETURN_STATEMENTS, 
    MODIFIED_ON) 
VALUES ('{job_name_value}','{bid_value}','{total_violation}','{cc_val}','{ls_val}','{gs_val}','{rs_val}','{timestamp}')
''')
print("Values inserted successfully......")