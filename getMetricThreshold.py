import sys
import re
from bs4 import BeautifulSoup as bs
from bs4 import NavigableString
from collections import defaultdict

print("Argument List:", str(sys.argv))
code_metric_file = sys.argv[1]
threshold_props_file = sys.argv[2]
lookup_table = ['Cyclomatic Complexity', 'Language Scope', 'Number of Goto Statements', 'Number of Return Statements']
bad_chars = ["[", "]", "'"]


with open(code_metric_file, "r") as f:
    soup = bs(f.read(), 'lxml')
    file_and_functions = defaultdict(list)
    for func_metric in soup(text=re.compile(r'Function Metrics')):
        p = func_metric.parent.parent.parent  # finding the <p> tag
        tables = p.find_next_sibling('table') # finding the <table> tag
        for table in tables:
            if not isinstance(tables, NavigableString):  # check for blank spaces
                rows = tables.findChildren('tr')
                # finding the function (1st col) and value (2nd col) from the table
                for row in rows:
                    metric_column = row.findAll('td')[0].findChild('p').findChild('span').text
                    value_column = row.findAll('td')[1].findChild('p').findChild('span').text
                    if metric_column == 'Metric' and value_column == 'Values (Min .. Max)':
                        continue
                    if metric_column in lookup_table:
                        file_and_functions[metric_column].append(value_column)
                break
        
with open(threshold_props_file, "w") as op:
    for key, value in file_and_functions.items():
        value_listToStr = ' '.join(map(str, value))
        op.write(f'{key}={value_listToStr}'+'\n')
print(f"Successfully generated threshold properties file {threshold_props_file}")
