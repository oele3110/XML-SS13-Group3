import re
import sys

def openReadFile(file):
	f = open(file,'r')
	return f

def openWriteFile(file):
	f = open(file,'w')
	return f

def initRdf():
	return '<?xml version="1.0"?>\n<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">'

def initXml():
	return '<?xml version="1.1" encoding="UTF-8" standalone="yes"?>\n'

def parse(inputFile, outputFile):
	
	#inputFile = 'sample.htm'
	#outputFile = 'output.xml'
	
	f = openReadFile(inputFile)
	
	output = initXml()
	outputRdf = initRdf()
	
	matchDescr = False
	strMatch4 = ''
	match6a = False
	match7a = False
	
	
	for line in f:
		pattern1 = '\s*<div (itemscope) (itemtype)="(.*)">'
		pattern2 = '\s*<link (itemprop)="(image)" (href)="(.*)"'
		pattern3 = '\s*<h1 (itemprop)="(name)">(.*)</h1>'
		pattern4 = '\s*<div .* (itemprop)="(description)">'
		pattern5 = '\s*<p>(.*)</p>'
		pattern6a = '\s*<p>(.*)'
		pattern6b = '\s*(.*)</p>'
		pattern7a = '\s*(<pre><code>.*)'
		pattern7b = '\s*(</code></pre>)'
		pattern8 = '\s*</div>'
		
		matchObj1 = re.match(pattern1, line)
		matchObj2 = re.match(pattern2, line)
		matchObj3 = re.match(pattern3, line)
		matchObj4 = re.match(pattern4, line)
		if matchDescr:
			matchObj5 = re.match(pattern5, line)
			matchObj6a = re.match(pattern6a, line)
			matchObj6b = re.match(pattern6b, line)
			matchObj7a = re.match(pattern7a, line)
			matchObj7b = re.match(pattern7b, line)
			matchObj8 = re.match(pattern8, line)
		
		
		# itemscope itemtype
		if matchObj1:
			output += '<itemscope itemtype="' + matchObj1.group(3) + '">\n'
			outputRdf += '\n\t<itemscope>\n\t\t<rdf:Description rdf:about="' + matchObj1.group(3) + '">'
		
		# itemprop = image
		if matchObj2:
			output += '\t<itemprop type="' + matchObj2.group(2) + '">\n\t\t<href>' + matchObj2.group(4) + '</href>\n\t</itemprop>\n'
			outputRdf += '\n\t\t\t<itemprop>\n\t\t\t\t<rdf:Description rdf:about="' + matchObj2.group(2) + '">\n\t\t\t\t\t<href>' +  matchObj2.group(4) + '</href>\n\t\t\t\t</rdf:Description>\n\t\t\t</itemprop>'
		
		# itemprop = name
		if matchObj3:
			output += '\t<itemprop type="' + matchObj3.group(2) + '">\n\t\t<content>' + matchObj3.group(3) + '</content>\n\t</itemprop>\n'
			outputRdf += '\n\t\t\t<itemprop>\n\t\t\t\t<rdf:Description rdf:about="' + matchObj3.group(2) + '">\n\t\t\t\t\t<' + matchObj3.group(2) + '>' + matchObj3.group(3) + '</' + matchObj3.group(2) + '>\n\t\t\t\t</rdf:Description>\n\t\t\t</itemprop>'
		
		# itemprop = description
		if matchDescr:
			
			# <p>
			if matchObj5:
				output += '<p>' + matchObj5.group(1) + "</p>\\n\\n"
				outputRdf += '<p>' + matchObj5.group(1) + "</p>\\n\\n"
			elif matchObj6a:
				output += '<p>' + matchObj6a.group(1) + " "
				outputRdf += '<p>' + matchObj6a.group(1) + " "
			elif matchObj6b:
				output += matchObj6b.group(1) + "</p>\\n\\n"
				outputRdf += matchObj6b.group(1) + "</p>\\n\\n"
			# <code>
			elif matchObj7a:
				match7a = True
				output+= matchObj7a.group(1) + '\\n'
				outputRdf += matchObj7a.group(1) + '\\n'
			elif matchObj7b:
				match7a = False
				output += matchObj7b.group(1) + '\\n'
				outputRdf += matchObj7b.group(1) + '\\n'
			elif match7a:
				output += re.match('(.*)',line).group(1) + '\\n'
				outputRdf += re.match('(.*)',line).group(1) + '\\n'
			# </div>
			elif matchObj8:
				matchDescr = False
				output += '</content>\n\t</itemprop>\n'
				outputRdf += '</' + strMatch4 + '>\n\t\t\t\t</rdf:Description>\n\t\t\t</itemprop>'
		
		if matchObj4:
			matchDescr = True
			strMatch4 = matchObj4.group(2)
			output += '\t<itemprop type="' + matchObj4.group(2) + '">\n\t\t<content>'
			outputRdf += '\n\t\t\t<itemprop>\n\t\t\t\t<rdf:Description rdf:about="' + matchObj4.group(2) + '">\n\t\t\t\t\t<' + matchObj4.group(2) + '>'

	output += '</itemscope>'
	outputRdf += '\n\t\t</rdf:Description>\n\t</itemscope>\n</rdf:RDF>'
	
	#f = openWriteFile(outputFile)
	#f.write(output)
	
	f2 = openWriteFile(outputFile)
	f2.write(outputRdf)


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