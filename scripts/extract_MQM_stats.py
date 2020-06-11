#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import sys

import tokeniser

sys.stdin = codecs.getreader('utf-8')(sys.stdin)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stderr = codecs.getwriter('utf-8')(sys.stderr)

def count_tokens(string):
	return len(tokeniser.represent_tomaz(tokeniser.process['standard'](tokeniser.generate_tokenizer('hr'),string,'hr'),0).encode('utf8').strip().split('\n'))	
		

doc=False
tokenNo=0
errorhash={'Total error count':0} #the number of tokens that have a certain error markup

openIssues=[]

for line in sys.stdin:
	line=line.strip()
	try:
		ID=line.split(', ')[1]
		tag=line.split(', ')[2]
	except:
		pass
	if line == 'open doc':
		doc=True
		continue
	elif line== 'close doc':
		doc=False
		continue
	elif line.split(', ')[0] == 'mqm:startIssue':
		openIssues.append((ID,tag))
		for tjupl in openIssues:
			if tjupl[1]=='Omission':
				if tjupl[1] not in errorhash:
					errorhash[tjupl[1]]=1
				else:
					errorhash[tjupl[1]]+=1
# IF counting all agreement errors as affecting only 2 tokens (due to long-distance agreement) 					
#			elif tjupl[1] in ['Agreement','Case','Number','Gender']:
#				if tjupl[1] not in errorhash:
#					errorhash[tjupl[1]]=2
#				else:
#					errorhash[tjupl[1]]+=2
		continue
	elif line.split(', ')[0] == 'mqm:endIssue':
		for openIssue in openIssues:
			if openIssue[0]==(ID):
				openIssues.remove(openIssue)
				continue
	elif len(openIssues) > 0:
		length=count_tokens(line)
		tokenNo+=length
		for tjupl in openIssues:
			#if tjupl[1] not in ['Agreement','Case','Number','Gender']:
			if tjupl[1] not in errorhash:
				errorhash[tjupl[1]]=length
			else:
				errorhash[tjupl[1]]+=length
	elif len(openIssues) == 0:
		tokenNo+=count_tokens(line)


errorhash['Total error count']=sum(errorhash.values())

print '### Error breakdown ###'
for entry in errorhash:
	print entry+': '+str(errorhash[entry])
print 'Total token count: '+str(tokenNo)
