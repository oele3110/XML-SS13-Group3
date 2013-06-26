import rdf
import re

def buildHeader():
	return "<html>\n<head>\n\t<title>history</title>\n</head>\n<body>\n<h1>History</h1>\n\n"

def buildFooter():
	return "\n</body>\n</html>"

def getHistory(query):
	
	pattern1 = '\s*<binding name="s"><uri>(.*)</uri></binding>\s*'
	pattern2 = '\s*<binding name="o"><literal>(.*)</literal></binding>\s*'
	
	history = rdf.queryDatabase(query)
	resource = None
	timestamp = None
	dictionary = None
	
	html = buildHeader()
	
	historyArray = re.split("\n", history)
	
	for line in historyArray:

		matchObj1 = re.match(pattern1, line)
		if matchObj1:
			#print matchObj1.group(1)
			resource = matchObj1.group(1)

		matchObj2 = re.match(pattern2, line)
		if resource and matchObj2:
			#print matchObj2.group(1)
			timestamp = matchObj2.group(1)
			tempDict = { timestamp : resource}
			if not dictionary:
				dictionary = tempDict
			else:
				dictionary.update(tempDict)
		
		if resource and timestamp:
			resource = None
			timestamp = None
	
	for key in sorted(dictionary.iterkeys(), reverse = True):
		print key + "\t" + dictionary[key]
		html += "<p>" + key + " : <a href=\"" + dictionary[key] + "\">" + dictionary[key] + "</a></p>\n"
	
	html += buildFooter()
	
	f = open("history.html", "w")
        f.write(html)
        f.flush()
        f.close()
	
	return html

getHistory("PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT * WHERE {?s xsd:dateTime ?o}")
