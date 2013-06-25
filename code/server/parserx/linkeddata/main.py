import re
import sys

# from logging_wrapper import *

def openReadFile(file):
	f = open(file,'r+')
	return f

def openWriteFile(file):
	f = open(file,'w')
	return f

# creates rdf file which contains resource as subject only
# input: (unspecified) rdf file, which contains reource as subject /object
# and http-link to resource (full link with protocol)
def parse(inputFile, outputFile, resource):
	
	pattern_any_description = '\s*<rdf:Description rdf:about=(.*)>'
	pattern_rsrc_as_subj = '\s*<rdf:Description rdf:about="'+resource+'">'
	pattern_close_description = '\s*</rdf:Description>'

	outputRdf = ""
	
	f = openReadFile(inputFile)
	lines = f.readlines()
	eof_index = len(lines) 
	i=0;

	# init_phase: get every line before first rdf-description tag
	while i<(eof_index):
		
		# check if description tag
		matchObj1 = re.match(pattern_any_description, lines[i])
		if matchObj1:
			# print "\n ------ BREAK ------ \n"
			break
		
		# get next line
		outputRdf += (lines[i])
		# print "[i="+str(i)+"]\n" + lines[i]
		i += 1
		
	# select only rdf-descriptions with resource as subject
	while i<(eof_index):

		# check if valid (rsrc as subj) description tag
		matchObj1 = re.match(pattern_rsrc_as_subj, lines[i])
		if matchObj1:
			# copy valid description
			isDescription = True
			while isDescription:
				outputRdf += (lines[i])
				# print "[i="+str(i)+"]\n" + lines[i]
				i += 1
				
				# check if description tag gets closed
				matchObj1 = re.match(pattern_close_description, lines[i])
				if matchObj1:
					outputRdf += (lines[i])
					# print "[i="+str(i)+"]\n" + lines[i]
					# print "\n ------ isFalse ------ \n"
					isDescription = False
		i += 1	

	# final_phase: get closing tags after last rdf-description tags
	outputRdf += (lines[eof_index-1])
	# print "[i="+str(eof_index-1)+"]\n" + lines[eof_index-1]

	# create file
	f2 = openWriteFile(outputFile)
	f2.write(outputRdf)
	f2.close()

# returns rdf string which contains resource as subject only
# input: (unspecified) rdf file, which contains reource as subject /object
# and http-link to resource (full link with protocol)
def parse2(resource, rdfData):
	
	pattern_any_description = '\s*<rdf:Description rdf:about=(.*)>'
	pattern_rsrc_as_subj = '\s*<rdf:Description rdf:about="'+resource+'">'
	pattern_close_description = '\s*</rdf:Description>'

	outputRdf = ""
	
	lines = rdfData
	eof_index = len(lines) 
	i=0;

	# init_phase: get every line before first rdf-description tag
	while i<(eof_index):
		
		# check if description tag
		matchObj1 = re.match(pattern_any_description, lines[i])
		if matchObj1:
			# print "\n ------ BREAK ------ \n"
			break
		
		# get next line
		outputRdf += (lines[i])
		# print "[i="+str(i)+"]\n" + lines[i]
		i += 1
		
	# select only rdf-descriptions with resource as subject
	while i<(eof_index):

		# check if valid (rsrc as subj) description tag
		matchObj1 = re.match(pattern_rsrc_as_subj, lines[i])
		if matchObj1:
			# copy valid description
			isDescription = True
			while isDescription:
				outputRdf += (lines[i])
				# print "[i="+str(i)+"]\n" + lines[i]
				i += 1
				
				# check if description tag gets closed
				matchObj1 = re.match(pattern_close_description, lines[i])
				if matchObj1:
					outputRdf += (lines[i])
					# print "[i="+str(i)+"]\n" + lines[i]
					# print "\n ------ isFalse ------ \n"
					isDescription = False
		i += 1	

	# final_phase: get closing tags after last rdf-description tags
	outputRdf += (lines[eof_index-1])
	# print "[i="+str(eof_index-1)+"]\n" + lines[eof_index-1]

	# return manipulated rdf
	return outputRdf

# string URL: dbpedia ressource URI http://dbpedia.org/resource/Klaus_Wowereit 
# string input: string containing all rdf-information
def run(url, input):
	inputArray = re.split("\r\n", input)
	return parse2(url, inputArray)


def main():
	if len(sys.argv) != 4:
		print 'run as:\n\tpython main.py inputFile outputFile resource'
	else:
		inputFile = sys.argv[1]
		outputFile = sys.argv[2]
		resource = sys.argv[3]
		print 'input file: ' + inputFile
		print 'output file: ' + outputFile
		print 'output file: ' + resource
		print 'creating subject-based RDF file'
		parse(inputFile, outputFile, resource)
main()
