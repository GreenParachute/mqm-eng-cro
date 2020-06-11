#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import sys

#sys.stdin = codecs.getreader('utf-8')(sys.stdin)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stderr = codecs.getwriter('utf-8')(sys.stderr)


def count_sentence_errors(doc):
	
	sent=False
	sent_counter=0
	sent_annos={}
	
	for line in doc:
		line=line.strip()
		
		try:
			ID=line.split(', ')[1]
			tag=line.split(', ')[2]
		except:
			pass
	
		error_c=0
		
		if line == 'open doc':
			sent=True
			sent_counter+=1
			sent_annos[sent_counter]=[]
			continue
		elif line== 'close doc':
			sent=False
			continue
		elif line.split(', ')[0] == 'mqm:startIssue':
			if tag not in sent_annos[sent_counter]:
				sent_annos[sent_counter].append(tag)

	return sent_annos	#sent_annos=={1:['Mistranslation'], 2:['Unintelligible','Agreement'], ...}

def calculate_kappa(xyyes,xyesyno,xnoyyes,xyno):
	a=xyyes
	b=xyesyno
	c=xnoyyes
	d=xyno
	
	po=(float(a)+d)/(a+b+c+d)

	marginala=((float(a)+b)*(a+c))/(a+b+c+d)
	marginalb=((c+d)*(b+d))/(float(a)+b+c+d)
	pe=(marginala+marginalb)/(float(a)+b+c+d)

	kappa=(po-pe)/(1.0-pe)
	
	return kappa

annotator1=codecs.open("/path/to/first/annotator/*.parsed/file/", "r") 
annotator2=codecs.open("/path/to/second/annotator/*.parsed/file/", "r") 

a1_errors=count_sentence_errors(annotator1)
a2_errors=count_sentence_errors(annotator2)


a1a2yes={'Accuracy':0,'Mistranslation':0,'Omission':0,'Addition':0,'Untranslated':0,'Fluency':0,'Unintelligible':0,'Register':0,'Spelling':0,'Grammar':0,'Word order':0,'Function words':0,'Extraneous':0,'Incorrect':0,'Missing':0,'Word form':0,'Part of speech':0,'Tense/aspect/mood':0,'Agreement':0,'Number':0,'Gender':0,'Case':0}
a1noa2yes={'Accuracy':0,'Mistranslation':0,'Omission':0,'Addition':0,'Untranslated':0,'Fluency':0,'Unintelligible':0,'Register':0,'Spelling':0,'Grammar':0,'Word order':0,'Function words':0,'Extraneous':0,'Incorrect':0,'Missing':0,'Word form':0,'Part of speech':0,'Tense/aspect/mood':0,'Agreement':0,'Number':0,'Gender':0,'Case':0}
a1yesa2no={'Accuracy':0,'Mistranslation':0,'Omission':0,'Addition':0,'Untranslated':0,'Fluency':0,'Unintelligible':0,'Register':0,'Spelling':0,'Grammar':0,'Word order':0,'Function words':0,'Extraneous':0,'Incorrect':0,'Missing':0,'Word form':0,'Part of speech':0,'Tense/aspect/mood':0,'Agreement':0,'Number':0,'Gender':0,'Case':0}
a1a2no={'Accuracy':0,'Mistranslation':0,'Omission':0,'Addition':0,'Untranslated':0,'Fluency':0,'Unintelligible':0,'Register':0,'Spelling':0,'Grammar':0,'Word order':0,'Function words':0,'Extraneous':0,'Incorrect':0,'Missing':0,'Word form':0,'Part of speech':0,'Tense/aspect/mood':0,'Agreement':0,'Number':0,'Gender':0,'Case':0}

#a1_errors={1:[],2:[], 3:['Mistranslation'], 4:['Mistranslation','Untranslated']}
#a1_errors={1:[],2:['Mistranslation'], 3:[], 4:['Mistranslation','Missing']}


#agreement overall and for every existing error category
for sentence in a1_errors:
	if len(a1_errors[sentence]) == 0 and len(a2_errors[sentence]) == 0:
		for error in a1a2no:
			a1a2no[error]+=1
	elif len(a1_errors[sentence]) == 0 and len(a2_errors[sentence]) > 0:
		for error in a1noa2yes:
			if error in a2_errors[sentence]:
				a1noa2yes[error]+=1
			else:
				a1a2no[error]+=1
	elif len(a1_errors[sentence]) > 0 and len(a2_errors[sentence]) == 0:
		for error in a1yesa2no:
			if error in a1_errors[sentence]:
				a1yesa2no[error]+=1
			else:
				a1a2no[error]+=1
	elif len(a1_errors[sentence]) > 0 and len(a2_errors[sentence]) > 0:
		for error in a1a2yes:
			if error in a2_errors[sentence] and error in a1_errors[sentence]:
				a1a2yes[error]+=1				
			elif error in a2_errors[sentence] and error not in a1_errors[sentence]:
				a1noa2yes[error]+=1
			elif error not in a2_errors[sentence] and error in a1_errors[sentence]:
				a1yesa2no[error]+=1
			else:
				a1a2no[error]+=1	

print 'Total kappa: '+str(calculate_kappa(sum(a1a2yes.values()),sum(a1yesa2no.values()),sum(a1noa2yes.values()),sum(a1a2no.values())))

lista=[a1a2yes,a1noa2yes,a1a2no,a1yesa2no]

for error_counts in lista:
	for error_type in error_counts:
		if error_type in ['Mistranslation','Addition','Omission','Untranslated']:
			error_counts['Accuracy']+=error_counts[error_type]
		if error_type in ['Number','Gender','Case']:
			error_counts['Agreement']+=error_counts[error_type]
		if error_type in ['Extraneous','Missing','Incorrect']:
			error_counts['Function words']+=error_counts[error_type]

for error_counts in lista:
	for error_type in error_counts:
		if error_type in ['Part of speech','Tense/aspect/mood','Agreement']:
			error_counts['Word form']+=error_counts[error_type]

for error_counts in lista:
	for error_type in error_counts:
		if error_type in ['Word form','Word order','Function words']:
			error_counts['Grammar']+=error_counts[error_type]

for error_counts in lista:
	for error_type in error_counts:
		if error_type in ['Spelling','Register','Grammar','Unintelligible']:
			error_counts['Fluency']+=error_counts[error_type]

for error in a1a2yes:
	try:
		print 'Kappa for '+error+': '+str(calculate_kappa(a1a2yes[error],a1yesa2no[error],a1noa2yes[error],a1a2no[error]))
	except:
		print 'Oops, problem with '+error

a1a2yes=0
a1noa2yes=0
a1yesa2no=0
a1a2no=0

#a1_errors={1:[],2:[], 3:['Mistranslation'], 4:['Mistranslation','Untranslated']}
#a2_errors={1:[],2:['Mistranslation'], 3:[], 4:['Mistranslation','Missing']}

#agreement for 'any' error per sentence

for sentence in a1_errors:
	print 'filip:', a1_errors[sentence]
	print 'denis', a2_errors[sentence]
	if len(a1_errors[sentence]) == 0 and len(a2_errors[sentence]) == 0:
		a1a2no+=1
		print 'a1a2no', a1a2no
	elif len(a1_errors[sentence]) == 0 and len(a2_errors[sentence]) > 0:
		a1noa2yes+=1
		print 'a1noa2yes', a1noa2yes
	elif len(a1_errors[sentence]) > 0 and len(a2_errors[sentence]) == 0:
		a1yesa2no+=1
		print 'a1yesa2no', a1yesa2no
	elif len(a1_errors[sentence]) > 0 and len(a2_errors[sentence]) > 0:
		a1a2yes+=1
		print 'a1a2yes', a1a2yes
	#sys.stdin.readline()

print a1a2yes, a1noa2yes, a1yesa2no, a1a2no

print 'Overall kappa: '+str(calculate_kappa(a1a2yes,a1yesa2no,a1noa2yes,a1a2no))
