# Written by Ho Yeung, Lee Martin in 28 November 2018
#python countdistinct.py xxx.csv "MAC Address"
#python countdistinct.py aa.csv hello
import sys
import os
import pandas as pd
import datetime as dt
import re
import numpy as np
from dateutil import parser
import datetime
import csv

if len(sys.argv) == 3:
    print(sys.argv[1])
    print(sys.argv[2])
else:
    sys.exit(0)

def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

currentdirectory = os.getcwd()
starttime=datetime.datetime.now()
os.environ['TZ'] = 'China/Hong Kong'
df4 = pd.DataFrame()
data = pd.read_csv(os.path.join(currentdirectory,sys.argv[1]))
df4 = df4.append(data)

print datetime.datetime.now()-starttime

starttime=datetime.datetime.now()

headers = []
count = 0
with open(os.path.join(currentdirectory,sys.argv[1]), 'rb') as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader, None)

dff4 = (df4.groupby(sys.argv[2])[sys.argv[2]].count())
dff4.to_csv("UniqueMacAddress.csv", sep=',')

line_prepender("UniqueMacAddress.csv", ",".join(headers)+ ",count")

contents2 = []
headers = []
with open(os.path.join(os.path.join(currentdirectory, "UniqueMacAddress.csv")), 'r') as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader, None)
    contents2 = []
    for row in reader:
        contents2 = contents2 + [[row[0], row[len(row)-1]]]
    contents2 = [[headers[0],headers[len(row)-1]]] + contents2

with open(os.path.join(currentdirectory,'graph.html'), 'r') as file :
    filedata = file.read()

# Replace the target string
filedata = filedata.replace('#Data', re.sub(r"'(\d+)'", r'\1', str(','.join( str(a) for a in contents2 ))))

with open(os.path.join(currentdirectory,'graph2.html'), 'w') as file:
    file.write(filedata)

import webbrowser, os
chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
webbrowser.get(chrome_path).open(os.path.join(currentdirectory, "graph2.html"))
