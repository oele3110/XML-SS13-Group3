import re
import sys

def openReadFile(file):
	f = open(file,'r')
	return f

def openWriteFile(file):
	f = open(file,'w')
	return f

def parse(inputFile, outputFile):
	
	#inputFile = 'sample.htm'
	#outputFile = 'output.xml'
	
	f = openReadFile(inputFile)
	out = ''
	output = ''
	matchDescr = False
	match6a = False
	
	for line in f:
		pattern1 = '\s*<div (itemscope)="(.*)" (itemtype)="(.*)">'
		pattern2 = '\s*<link (itemprop)="(image)" (href)="(.*)"'
		pattern3 = '\s*<h1 (itemprop)="(name)"><a (href)="(.*)"\s.*>(.*)</a></h1>'
		pattern4 = '\s*<div .* (itemprop)="(description)">'
		pattern5 = '\s*<p>(.*)</p>'
		pattern6a = '\s*<p>(.*)'
		pattern6b = '\s*(.*)</p>'
		pattern7 = '\s*</div>'
		
		matchObj1 = re.match(pattern1, line)
		matchObj2 = re.match(pattern2, line)
		matchObj3 = re.match(pattern3, line)
		matchObj4 = re.match(pattern4, line)
		matchObj5 = None
		matchObj7 = None
		if matchDescr:
			matchObj5 = re.match(pattern5, line)
			matchObj6a = re.match(pattern6a, line)
			matchObj6b = re.match(pattern6b, line)
			matchObj7 = re.match(pattern7, line)
		
		
		# itemscope itemtype
		if matchObj1:
			out = out + matchObj1.group(1) + "\n\t" + matchObj1.group(3) + ": " + matchObj1.group(4) + "\n\n"
			output += '<?xml version="1.1" encoding="UTF-8" standalone="yes"?>\n<itemscope>\n\t<itemtype>' + matchObj1.group(4) + '</itemtype>\n\t<itemprops>\n'
		
		# itemprop = image
		if matchObj2:
			out = out + matchObj2.group(1) + "\n\t" + matchObj2.group(2) + "\n\t" + matchObj2.group(3) + ": " + matchObj2.group(4) + "\n\n"
			output += '\t\t<itemprop>\n\t\t\t<type>' + matchObj2.group(2) + '</type>\n\t\t\t<href>' + matchObj2.group(4) + '</href>\n\t\t</itemprop>\n'
		
		# itemprop = name
		if matchObj3:
			out = out + matchObj3.group(1) + "\n\t" + matchObj3.group(2) + "\n\t" + matchObj3.group(3) + ": " + matchObj3.group(4) + "\n\t" + matchObj3.group(5) + "\n\n"
			output += '\t\t<itemprop>\n\t\t\t<type>' + matchObj3.group(2) + '</type>\n\t\t\t<href>' + matchObj3.group(4) + '</href>\n\t\t\t<content>' + matchObj3.group(5) + '</content>\n\t\t</itemprop>\n'
		
		# itemprop = description
		if matchDescr:
			#out = out + line
			if matchObj5:
				#print 'pattern5'
				out = out + matchObj5.group(1) + "\\n\\n"
				output += matchObj5.group(1) + "\\n\\n"
			elif matchObj6a:
				#print 'pattern6a'
				out = out + matchObj6a.group(1) + " "
				output += matchObj6a.group(1) + " "
			elif matchObj6b:
				#print 'pattern6b'
				out = out + matchObj6b.group(1) + "\\n\\n"
				output += matchObj6b.group(1) + "\\n\\n"
			elif matchObj7:
				#print 'pattern7'
				matchDescr = False
				output += '</content>\n\t\t</itemprop>\n'
		
		if matchObj4:
			#print 'pattern4'
			matchDescr = True
			out = out + matchObj4.group(1) + "\n\t" + matchObj4.group(2) + "\n"
			output += '\t\t<itemprop>\n\t\t\t<type>' + matchObj4.group(2) + '</type>\n\t\t\t<content>'

	output += '\t</itemprops>\n</itemscope>'
	#print "\n" + output
	
	
	f = openWriteFile(outputFile)
	f.write(output)


def main():
	if len(sys.argv) != 3:
		print 'run as:\n\tpython main.py inputFile outputFile'
	else:
		inputFile = sys.argv[1]
		outputFile = sys.argv[2]
		print 'input file: ' + inputFile
		print 'output file: ' + outputFile
		print 'start parsing file'
		parse(inputFile, outputFile)

main()