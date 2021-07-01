import re
from bs4 import BeautifulSoup as bs
from bs4 import NavigableString
import ntpath
from collections import defaultdict

class HtmlParser:
    def __init__(self, input):
        with open(input) as f:
            self.soup = bs(f.read(), 'lxml')

    def get_file_and_functions(self, metric, threshold):
        file_and_functions = defaultdict(list)
        for metric_path in self.soup(text=re.compile(fr"\({metric}\)")):  # Fetching the full metric filename path
            p = metric_path.parent.parent.parent  # finding the <p> tag
            tables = p.find_next_sibling('table')  # finding the <table> tag
            for table in tables:
                if not isinstance(table, NavigableString):  # check for blank spaces
                    rows = table.findChildren('tr')
                    # finding the function (2nd col) and value (3rd col) from the table
                    for row in rows:
                        function_column = row.findAll('td')[1].findChild('p').findChild('span').text
                        value_column = row.findAll('td')[2].findChild('p').findChild('span').text
                        if function_column.lower() == 'function' and value_column.lower() == 'value':
                            continue
                        if float(value_column) == threshold:
                            filepath = metric_path.split("\n")[0]
                            base_path, filename = ntpath.split(filepath)
                            file = ntpath.basename(base_path) + "\\" + filename # fetching path from src
                            file_and_functions[file].append(function_column)
        return file_and_functions
