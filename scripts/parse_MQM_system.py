#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.parsers.expat
import sys
import codecs

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

def start_element(name, attrs):
	if name=='doc':
		sys.stdout.write('open '+name+'\n')
	else:	
		if len(attrs) > 1:
			sys.stdout.write(name+', '+attrs['id']+', '+attrs[u'type']+'\n')
		elif len(attrs) == 1:
			sys.stdout.write(name+', '+attrs['id']+'\n')
		

def end_element(name):
	if name == 'doc':
		sys.stdout.write('close '+name+'\n\n')
	
def char_data(data):
	if data !='\n':
		sys.stdout.write(data+'\n')
	
parser = xml.parsers.expat.ParserCreate()

parser.StartElementHandler = start_element
parser.EndElementHandler = end_element
parser.CharacterDataHandler= char_data


for line in sys.stdin:
	parser.Parse(line)
