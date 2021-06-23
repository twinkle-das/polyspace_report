from collections import defaultdict
from xml.dom import minidom
import sys
import re
from htmlParser import HtmlParser

polyspacelog_file = sys.argv[1]
build_log_file = sys.argv[2]
threshold_properties_file = sys.argv[3]
output_file = sys.argv[4]

def read_threshold_file():
    map = {}
    with open(threshold_properties_file, "r") as tp_file:
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
    return map


def set_nested_xml_data(doc, metric_name_tag, max_value_tag, max_val_data, file_name_tag, func_name_tag, metric_data, parent):
    metric_name_elem = doc.createElement(metric_name_tag)
    max_value_elem = doc.createElement(max_value_tag)
    max_value_node = doc.createTextNode(max_val_data)
    max_value_elem.appendChild(max_value_node)
    metric_name_elem.appendChild(max_value_elem)
    for file_name, func_name in metric_data.items():
        file_name_elem = doc.createElement(file_name_tag)
        file_name_elem.setAttribute("filename", file_name)
        func_name_elem = doc.createElement(func_name_tag)
        for fn in range(len(func_name)-1):
            func_name_node = doc.createTextNode(func_name[fn] + ",")
            func_name_elem.appendChild(func_name_node)
        func_name_node = doc.createTextNode(func_name[-1])
        func_name_elem.appendChild(func_name_node)
        file_name_elem.appendChild(func_name_elem)
        metric_name_elem.appendChild(file_name_elem)
        parent.appendChild(metric_name_elem)

def set_xml_data(doc, tag_name, data_name, parent):
    elem = doc.createElement(tag_name)
    text_node = doc.createTextNode(data_name)
    elem.appendChild(text_node)
    parent.appendChild(elem)

def get_violated_rule():
    map = read_threshold_file()
    print("Threshold values Passed: ", map)
    hp = HtmlParser()
    cc_data = hp.get_file_and_functions("Cyclomatic Complexity", float(map.get('CC')))
    print("Fetched Cyclomatic Complexity files and functions successfully......")

    ls_data = hp.get_file_and_functions("Language Scope", float(map.get('LS')))
    print("Fetched Language Scope files and functions successfully......")

    gs_data = hp.get_file_and_functions("Number of Goto Statements", float(map.get('GS')))
    print("Fetched Number of Goto Statements files and functions successfully......")

    rs_data = hp.get_file_and_functions("Number of Return Statements", float(map.get('RS')))
    print("Fetched Return Statements files and functions successfully......")
    doc = minidom.Document()
    root = doc.createElement("root")
    doc.appendChild(root)

    with open(build_log_file, "r") as bl_file:
        line = bl_file.readline()
        while line:
            if line.__contains__("~"):
                tag, data = line.split("~")
                set_xml_data(doc, tag, data, root)
            line = bl_file.readline()
    set_nested_xml_data(
        doc,
        "Cyclomatic_Complexity",
        "max_value", 
        map.get('CC'),
        "file_name",
        "func_name",
        cc_data,
        root
    )
    set_nested_xml_data(
        doc,
        "Language_Scope",
        "max_value",
        map.get('LS'),
        "file_name",
        "func_name",
        ls_data,
        root
    )
    set_nested_xml_data(
        doc,
        "Goto_Statements",
        "max_value", 
        map.get('GS'),
        "file_name",
        "func_name",
        gs_data,
        root
    )
    set_nested_xml_data(
        doc,
        "Return_Statements",
        "max_value", 
        map.get('RS'),
        "file_name",
        "func_name",
        rs_data,
        root
    )
    print("Successfully set the data in xml for all threshold types......")

    with open(polyspacelog_file, "r") as pl_file:
        line = pl_file.readline()
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
            line = pl_file.readline()

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

        set_xml_data(doc, "Total_Violation", str(violations), root)

    with open(output_file, "w") as op:
        op.write(doc.toprettyxml(indent="\t"))
    print(f"Successfully generated XML {output_file}")

if __name__ == "__main__":
    get_violated_rule()
