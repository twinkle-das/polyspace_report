#!/usr/bin/env python3

import sys
import os
from lxml import etree
import GetFileName as filename

XSLPATH = sys.argv[1]
XMLPATH = sys.argv[2]
HTMLFOLDERPATH = sys.argv[3]

HTMLPATH = HTMLFOLDERPATH+'\\' + \
    filename.GetFileNameWithoutExtension(XMLPATH)+'.html'

if os.path.isfile(XMLPATH):
    XSLT_DOC = etree.parse(XSLPATH)
    XSLT_TRANSFORMER = etree.XSLT(XSLT_DOC)
    SOURCE_DOC = etree.parse(XMLPATH)
    OUTPUT_DOC = XSLT_TRANSFORMER(SOURCE_DOC)
    with open(HTMLPATH, 'w+') as f:
        f.write(str(OUTPUT_DOC))
    print(f"Successfully Generated HTML file {HTMLPATH}")