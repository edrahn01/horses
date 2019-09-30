#!/usr/bin/env python

import subprocess
import os
from os.path import expanduser



default = expanduser('~/horse/charts/')
for chart in os.listdir(default):
    if chart in ['texts', 'htmls']:
        continue

    paths = chart[:-4].split('/')
    chart = paths[-1]
    print(chart)

    text = "%s/texts/%s.txt"%(default, chart)
    html = "%s/htmls/%s"%(default, chart)
    chart = "%s/%s.pdf"%(default, chart)

    executable = expanduser('~/poppler/build/utils/pdftotext')
    proc = subprocess.run([executable, chart, text], capture_output=True)
    if proc.stderr:
        print("ERROR!:%s"%(proc.stderr))

    executable = expanduser('~/poppler/build/utils/pdftohtml')
    proc = subprocess.run([executable, '-i', '-c', chart, html], capture_output=True)
    if proc.stderr:
        print("ERROR!:%s"%(proc.stderr))
