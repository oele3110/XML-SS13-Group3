import re
import sys
import datetime

# from logging_wrapper import *

def openReadFile(file):
	f = open(file,'r')
	return f

def openWriteFile(file):
	f = open(file,'w')
	return f

def initRdf():
	# return '<?xml version="1.0"?>\n<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n\txmlns:md="http://www.w3.org/ns/md/">'
	return '<?xml version="1.0"?>\n<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n\txmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"\n\txmlns:schema="http://schema.org/Article#"\n\txmlns:xsd="http://www.w3.org/2001/XMLSchema#">'

def initXml():
	return '<?xml version="1.1" encoding="UTF-8" standalone="yes"?>\n'

def getTimestamp():
	return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S');

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
	
	url = "http://stackoverflow.com"
	
	# add url
	outputRdf += '\n\t<rdf:Description rdf:about="' + url + '">'
	# add timestamp
	outputRdf += '\n\t\t<xsd:dateTime>' + getTimestamp() + '</xsd:dateTime>'
	
	for line in f:
		pattern1 = '\s*<div (itemscope) (itemtype)="(.*)">'
		pattern2 = '\s*<link (itemprop)="(image)" (href)="(.*)"'
		pattern3 = '\s*<h1 (itemprop)="(name)"><a href="(.*)">(.*)</a></h1>'
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
			# output += '<md:itemscope itemtype="' + matchObj1.group(3) + '">\n'
			# outputRdf += '\n\t<rdf:Description rdf:about="' + url + '">\n\t\t<md:itemscope>\n\t\t\t<rdf:Description rdf:about="' + matchObj1.group(3) + '">'
			outputRdf += '\n\t\t<rdfs:isDefinedBy rdf:resource="http://schema.org/Article" />'
		
		# itemprop = image
		if matchObj2:
			# output += '\t<md:itemprop type="' + matchObj2.group(2) + '">\n\t\t<md:url>' + matchObj2.group(4) + '</md:url>\n\t</md:itemprop>\n'
			# outputRdf += '\n\t\t\t\t<md:itemprop>\n\t\t\t\t\t<rdf:Description rdf:about="#' + matchObj2.group(2) + '">\n\t\t\t\t\t\t<md:url>' +  matchObj2.group(4) + '</md:url>\n\t\t\t\t\t</rdf:Description>\n\t\t\t\t</md:itemprop>'
			outputRdf += '\n\t\t<schema:image rdf:resource="' + matchObj2.group(4) + '" />'
		
		# itemprop = name
		if matchObj3:
			# output += '\t<itemprop type="' + matchObj3.group(2) + '">\n\t\t<md:content>' + matchObj3.group(3) + '</content>\n\t</md:itemprop>\n'
			# outputRdf += '\n\t\t\t\t<md:itemprop>\n\t\t\t\t\t<rdf:Description rdf:about="#' + matchObj3.group(2) + '">\n\t\t\t\t\t\t<md:text>&lt;a href ="' + matchObj3.group(3) + '"&gt;' + matchObj3.group(4) + '&lt;/a&gt;</md:text>\n\t\t\t\t\t</rdf:Description>\n\t\t\t\t</md:itemprop>'
			outputRdf += '\n\t\t<schema:name>&lt;a href ="' + matchObj3.group(3) + '"&gt;' + (matchObj3.group(4).replace("&","&amp;")).replace("<","&lt;") + '&lt;/a&gt; </schema:name>'
		
		# itemprop = description
		if matchDescr:
			
			# <p>
			if matchObj5:
				# output += '&lt;p&gt;' + matchObj5.group(1) + "&lt;/p&gt;\\n\\n"
				outputRdf += '&lt;p&gt;' + (matchObj5.group(1).replace("&","&amp;")).replace("<","&lt;") + "&lt;/p&gt;\\n\\n"
			elif matchObj6a:
				# output += '&lt;p&gt;' + matchObj6a.group(1) + " "
				outputRdf += '&lt;p&gt;' + (matchObj6a.group(1).replace("&","&amp;")).replace("<","&lt;") + " "
			elif matchObj6b:
				# output += matchObj6b.group(1) + "&lt;/p&gt;\\n\\n"
				outputRdf += (matchObj6b.group(1).replace("&","&amp;")).replace("<","&lt;") + "&lt;/p&gt;\\n\\n"
			# <code>
			elif matchObj7a:
				match7a = True
				# output+= matchObj7a.group(1) + '\\n'
				outputRdf += matchObj7a.group(1) + '\\n'
			elif matchObj7b:
				match7a = False
				# output += matchObj7b.group(1) + '\\n'
				outputRdf += matchObj7b.group(1) + '\\n'
			elif match7a:
				# output += re.match('(.*)',line).group(1) + '\\n'
				outputRdf += re.match('(.*)',line).group(1) + '\\n'
			# </div>
			elif matchObj8:
				matchDescr = False
				# output += '</md:text>\n\t</md:itemprop>\n'
				# outputRdf += '</md:text>\n\t\t\t\t\t</rdf:Description>\n\t\t\t\t</md:itemprop>'
				outputRdf += '</schema:description>'
		
		if matchObj4:
			matchDescr = True
			# output += '\t<md:itemprop type="' + matchObj4.group(2) + '">\n\t\t<md:text>'
			outputRdf += '\n\t\t<schema:description>'
		
	outputRdf += '\n\t</rdf:Description>\n</rdf:RDF>'
	
	#f = openWriteFile(outputFile)
	#f.write(output)
	
	f2 = openWriteFile(outputFile)
	f2.write(outputRdf)

def parse2(url, input):

	# info(url)
	# info(input[:100])

	if not url:
		url = ''
	
	outputRdf = initRdf()
	
	matchDescr = False
	strMatch4 = ''
	match6a = False
	match7a = False
	foundItemscope = False
	isMicrodata = False
	
	# add url
	outputRdf += '\n\t<rdf:Description rdf:about="' + url + '">'
	# add timestamp
	outputRdf += '\n\t\t<xsd:dateTime>' + getTimestamp() + '</xsd:dateTime>'
	
	for line in input:
		pattern1 = '\s*<div (itemscope) (itemtype)="(.*)">'
		pattern2 = '\s*<link (itemprop)="(image)" (href)="(.*)"'
		pattern3 = '\s*<h1 (itemprop)="(name)"><a href="(.*)">(.*)</a></h1>'
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
			# outputRdf += '\n\t<rdf:Description rdf:about="' + url + '">\n\t\t<md:itemscope>\n\t\t\t<rdf:Description rdf:about="' + matchObj1.group(3) + '">'
			outputRdf += '\n\t\t<rdfs:isDefinedBy rdf:resource="http://schema.org/Article" />'
		
		# itemprop = image
		if matchObj2:
			# outputRdf += '\n\t\t\t\t<md:itemprop>\n\t\t\t\t\t<rdf:Description rdf:about="#' + matchObj2.group(2) + '">\n\t\t\t\t\t\t<md:url>' +  matchObj2.group(4) + '</md:url>\n\t\t\t\t\t</rdf:Description>\n\t\t\t\t</md:itemprop>'
			outputRdf += '\n\t\t<schema:image rdf:resource="' + matchObj2.group(4) + '" />'
		
		# itemprop = name
		if matchObj3:
			# outputRdf += '\n\t\t\t\t<md:itemprop>\n\t\t\t\t\t<rdf:Description rdf:about="#' + matchObj3.group(2) + '">\n\t\t\t\t\t\t<md:text>&lt;a href ="' + matchObj3.group(3) + '"&gt;' + matchObj3.group(4) + '&lt;/a&gt;</md:text>\n\t\t\t\t\t</rdf:Description>\n\t\t\t\t</md:itemprop>'
			outputRdf += '\n\t\t<schema:name>&lt;a href ="' + matchObj3.group(3) + '"&gt;' + (matchObj3.group(4).replace("&","&amp;")).replace("<","&lt;") + '&lt;/a&gt; </schema:name>'
		
		# itemprop = description
		if matchDescr:
			
			# <p>
			if matchObj5:
				outputRdf += '&lt;p&gt;' + (matchObj5.group(1).replace("&","&amp;")).replace("<","&lt;") + "&lt;/p&gt;\\n\\n"
			elif matchObj6a:
				outputRdf += '&lt;p&gt;' + (matchObj6a.group(1).replace("&","&amp;")).replace("<","&lt;") + " "
			elif matchObj6b:
				outputRdf += (matchObj6b.group(1).replace("&","&amp;")).replace("<","&lt;") + "&lt;/p&gt;\\n\\n"
			# <code>
			elif matchObj7a:
				match7a = True
				outputRdf += matchObj7a.group(1) + '\\n'
			elif matchObj7b:
				match7a = False
				outputRdf += matchObj7b.group(1) + '\\n'
			elif match7a:
				outputRdf += re.match('(.*)',line).group(1) + '\\n'
			# </div>
			elif matchObj8:
				matchDescr = False
				# outputRdf += '</md:text>\n\t\t\t\t\t</rdf:Description>\n\t\t\t\t</md:itemprop>'
				outputRdf += '</schema:description>'
		
		if matchObj4:
			matchDescr = True
			# outputRdf += '\n\t\t\t\t<md:itemprop>\n\t\t\t\t\t<rdf:Description rdf:about="#' + matchObj4.group(2) + '">\n\t\t\t\t\t\t<md:text>'
			outputRdf += '\n\t\t<schema:description>'
		
	outputRdf += '\n\t</rdf:Description>\n</rdf:RDF>'
	
	return outputRdf

def run(url, input):
	inputArray = re.split("\r\n", input)
	rdf = parse2(url, inputArray)
	return rdf
	

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

if __name__ == "__main__":
	main()
