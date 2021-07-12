import time
from Db_Helper import DB_Helper
import datetime
import sys
import re
from collections import defaultdict
from xml.dom import minidom
import operator

polyspacelog_file = sys.argv[1]
build_log_file = sys.argv[2]
db_helper = DB_Helper()

sql = '''CREATE TABLE IF NOT EXISTS tbl_violation_details(
    id serial PRIMARY KEY,
    build_id int NOT NULL,
    violation_code varchar(255) NOT NULL,
    count int NOT NULL,
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

with open(polyspacelog_file, "r") as pl_file:
    line = pl_file.readline()
    regexp = re.compile(r"^rule\s+\w?\d+(\.\d{1,2})?\s+violated\s+\d+\s+\w+")
    rcount_map = defaultdict(int)
    while line:
        line = line.strip()
        if regexp.search(line):
            rules = line.split()
            rnum = rules[1]
            rcount_map[rnum] = int(rules[3])
        line = pl_file.readline()
    sorted_rcount_map = dict(sorted(rcount_map.items(), key=operator.itemgetter(1), reverse=True))
    for rn, vc in sorted_rcount_map.items():
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        try:
            db_helper.execute_query(f'''INSERT INTO tbl_violation_details(BUILD_ID, VIOLATION_CODE, COUNT, MODIFIED_ON) 
            VALUES ('{bid_value}', '{rn}', '{vc}', '{timestamp}')''')
        except NameError as e:
            print ('ERROR.....One or more column data missing missing!!', e)
            print("Database insertion unsuccessful......")
    print("Values inserted successfully......")