import sys

polyspace_log_file = sys.argv[1]
threshold_properties_file = sys.argv[2]
build_log_file = sys.argv[3]

def append_file(content):
    with open(build_log_file, "a+") as bl_file:
        bl_file.seek(0)
        data = bl_file.read(100)
        if len(data) > 0 :
            bl_file.write("\n")
        bl_file.write(content)

def check_threshold_property():
    with open(polyspace_log_file, "r") as pl_file:
        line = pl_file.readline()
        total_violation = 0
        while line:
            line = line.strip()
            if line.__contains__("rules violated"):
                words = line.split()
                total_violation = int(words[0])
                print(total_violation)
            line = pl_file.readline()
    with open(threshold_properties_file, "r") as tp_file:
        line = tp_file.readline()
        while line:
            line = line.strip()
            if line.__contains__("="):
                property, value = line.split("=")
                if property.strip() == "violation":
                    violation_threshold = int(value.strip())
            line = tp_file.readline()
    if total_violation > violation_threshold:
        append_file("Quality_Analysis~Failure")
    else:
        append_file("Quality_Analysis~Successful")
    print("Data appended successfully......")

if __name__ == "__main__":
    check_threshold_property()