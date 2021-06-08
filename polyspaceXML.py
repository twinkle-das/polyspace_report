import time
from os import spawnl
from collections import defaultdict
from xml.dom import minidom
import sys
import re
from Db_Helper import DB_Helper
import datetime

input_file_path = sys.argv[1]
output_file_path = sys.argv[2]
job_build_id = sys.argv[3]
job_name = sys.argv[4]
db_helper = DB_Helper()

sql = '''CREATE TABLE IF NOT EXISTS POLYSPACE(
    id serial PRIMARY KEY,
    build_id int NOT NULL,
    job_name varchar(255) NOT NULL,
    rule_number varchar(255) NOT NULL,
    violation_count int NOT NULL,
    total_violation int NOT NULL,
    modified_on TIMESTAMP NOT NULL
)'''

db_helper.execute_query(sql)
print("Table created successfully........")

def get_violated_rule():
    doc = minidom.Document()
    root = doc.createElement("root")
    doc.appendChild(root)

    build_id = doc.createElement("build_id")
    bid = doc.createTextNode(str(job_build_id))
    build_id.appendChild(bid)

    jname = doc.createElement("job_name")
    jn = doc.createTextNode(str(job_name))
    jname.appendChild(jn)

    root.appendChild(build_id)
    root.appendChild(jname)

    with open(input_file_path, "r") as ip:
        line = ip.readline()
        violations = 0
        regexp = re.compile(r"^rule\s+\w?\d+(\.\d{1,2})?\s+violated\s+\d+\s+\w+")
        rcount_map = defaultdict(int)
        while line:
            line = line.strip()
            if line.__contains__("rules violated"):
                words = line.split()
                violations += int(words[0])

            elif regexp.search(line):
                rules = line.split()
                rnum = rules[1]
                rcount_map[rnum] += int(rules[3])

            line = ip.readline()
        for rn, vc in rcount_map.items():
            rule_violated = doc.createElement("rule_violated")
            rule_number = doc.createElement("rule_number")
            rname = doc.createTextNode(str(rn))
            rule_number.appendChild(rname)

            violation_count = doc.createElement("violation_count")
            vcount = doc.createTextNode(str(vc))
            violation_count.appendChild(vcount)

            rule_violated.appendChild(rule_number)
            rule_violated.appendChild(violation_count)
            root.appendChild(rule_violated)

            # function to insert values in db

            ts = time.time()
            timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            args = (job_build_id, job_name, rn, vc, violations, timestamp)
            db_helper.execute_query("""INSERT INTO POLYSPACE(BUILD_ID, JOB_NAME, RULE_NUMBER, VIOLATION_COUNT, TOTAL_VIOLATION, MODIFIED_ON) 
                VALUES (%s, %s, %s, %s, %s, %s)""", args)

        total_violation = doc.createElement("total_violation")
        tv = doc.createTextNode(str(violations))
        total_violation.appendChild(tv)
        root.appendChild(total_violation)
        
    with open(output_file_path, "w") as op:
        op.write(doc.toprettyxml(indent="\t"))
        print("Successfully Generated XML {}".format(output_file_path))


if __name__ == "__main__":
    get_violated_rule()
