#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

reference=[]
m3=[]
hybrid=[]
nmt=[]

import csv

with open("path/to/your/csv/file.csv", "rb") as input:
	annotation = csv.reader(input, delimiter=",", quotechar='"')
	for line in annotation:
		sentID=line[0]
		sourcesent=line[1]
		refsent=line[2]
		#m3sys=line[3]
		nmtsys=line[3]
		m3sys=line[4]
		hybridsys=line[5]
		
		reference.append(refsent)
		m3.append(m3sys)
		hybrid.append(hybridsys)
		nmt.append(nmtsys)
"""
hybriddata=open('path/to/output/destination.data', 'w')
hybriddata.write('<docs>\n')

for sentence in hybrid:
	doc = '<doc>'+ sentence + '</doc>'
	hybriddata.write(doc+'\n')
	
hybriddata.write('</docs>\n')
hybriddata.close()


m3data=open('path/to/output/destination.data', 'w')
m3data.write('<docs>\n')

for sentence in m3:
	doc = '<doc>'+ sentence + '</doc>'
	m3data.write(doc+'\n')

m3data.write('</docs>\n')
m3data.close()
"""

nmtdata=open('path/to/output/destination.data', 'w')
nmtdata.write('<docs>\n')

for sentence in nmt:
	doc = '<doc>'+ sentence + '</doc>'
	nmtdata.write(doc+'\n')

nmtdata.write('</docs>\n')
nmtdata.close()
