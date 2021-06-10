import time
from os import spawnl
from collections import defaultdict
from xml.dom import minidom
import sys
import re
from Db_Helper import DB_Helper
import datetime

polyspace_log_file = sys.argv[1]
threshold_properties_file = sys.argv[2]
build_log_file = sys.argv[3]
output_file = sys.argv[4]
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

def set_xml_data(doc, tag_name, data_name, parent):
    elem = doc.createElement(tag_name)
    text_node = doc.createTextNode(data_name)
    elem.appendChild(text_node)
    parent.appendChild(elem)

def get_violated_rule():
    doc = minidom.Document()
    root = doc.createElement("root")
    doc.appendChild(root)

    with open(threshold_properties_file, "r") as tp_file:
        line = tp_file.readline()
        while line:
            if line.__contains__("="):
                tag, data = line.split("=")
                set_xml_data(doc, tag, data, root)
            line = tp_file.readline()
    
    with open(build_log_file, "r") as bl_file:
        line = bl_file.readline()
        while line:
            if line.__contains__("~"):
                tag, data = line.split("~")
                set_xml_data(doc, tag, data, root)
                if tag == "Build_ID":
                    bid_value = data
                if tag == "Job_Name":
                    job_name_value = data
            line = bl_file.readline()

    with open(polyspace_log_file, "r") as lf_file:
        line = lf_file.readline()
        violations = 0
        regexp = re.compile(r"^rule\s+\w?\d+(\.\d{1,2})?\s+violated\s+\d+\s+\w+")
        rcount_map = defaultdict(int)

        while line:
            line = line.strip()
            if line.__contains__("rules violated"):
                words = line.split()
                violations = int(words[0])
            elif regexp.search(line):
                rules = line.split()
                rnum = rules[1]
                rcount_map[rnum] = int(rules[3])
            line = lf_file.readline()

        for rn, vc in rcount_map.items():

            rule_violated = doc.createElement("Rule_Violated")
            rule_number = doc.createElement("Rule_Number")
            rname = doc.createTextNode(str(rn))
            rule_number.appendChild(rname)

            violation_count = doc.createElement("Violation_Count")
            vcount = doc.createTextNode(str(vc))
            violation_count.appendChild(vcount)

            rule_violated.appendChild(rule_number)
            rule_violated.appendChild(violation_count)
            root.appendChild(rule_violated)

            # function to insert values in db

            ts = time.time()
            timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            db_helper.execute_query(f"""INSERT INTO POLYSPACE(BUILD_ID, JOB_NAME, RULE_NUMBER, VIOLATION_COUNT, TOTAL_VIOLATION, MODIFIED_ON) 
            VALUES ('{bid_value}', '{job_name_value}', '{rn}', '{vc}', '{violations}', '{timestamp}')""")
        
        set_xml_data(doc, "Total_Violation", str(violations), root)

    with open(output_file, "w") as op:
        op.write(doc.toprettyxml(indent="\t"))
    
    with open(output_file) as op_file:
        line = op_file.readline()
        xml_str = ""
        while line:
            regexp1 = re.compile(r".*</root>")
            regexp2 = re.compile(r"<.*>(.*?)</.*>")
            if regexp1.search(line) or regexp2.search(line):
                xml_str = xml_str + line
            elif not line.__contains__("</"):
                line.rstrip()
                xml_str = xml_str + line
            elif line.__contains__("</Rule_Violated>"):
                xml_str = xml_str + line
            else:
                xml_str = xml_str.rstrip() + line
            line = op_file.readline()

    with open(output_file, "w") as op_file:
        op_file.write(xml_str)
    print("Successfully Generated XML {}".format(output_file))

if __name__ == "__main__":
    get_violated_rule()
