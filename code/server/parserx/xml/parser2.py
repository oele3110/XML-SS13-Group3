from lxml import etree
from StringIO import StringIO
import datetime
from xml.sax.saxutils import escape

XSLT_STYLESHEET = ""

def getTimestamp():
	return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S');

def createStylesheet(url):
	return '''\
	<xsl:stylesheet version="1.0"
	     xmlns="http://www.openarchives.org/OAI/2.0/"
	     xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	     xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
	     xmlns:dc="http://purl.org/dc/elements/1.1/"
	     xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
	     xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
	     xmlns:xsd="http://www.w3.org/2001/XMLSchema#">

	     <xsl:template match="ListRecords/record/metadata">
	         <xsl:element name="rdf:Description">
	             <xsl:attribute name="rdf:about">
	                 <xsl:value-of select="oai_dc:dc/dc:identifier"/>
	             </xsl:attribute>
	             <xsl:text>&#xa;</xsl:text>
	             <xsl:for-each select="oai_dc:dc/*[text() and not (self::dc:identifier)]">
	                 <xsl:copy-of select="."/><xsl:text>&#xa;</xsl:text>
	             </xsl:for-each>
	         </xsl:element><xsl:text>&#xa;</xsl:text>
	     </xsl:template>
	
	     <xsl:template match="/">
	         <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
	         	xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
	         	xmlns:dc="http://purl.org/dc/elements/1.1/"
	         	xmlns:xsd="http://www.w3.org/2001/XMLSchema#"><xsl:text>&#xa;</xsl:text>
	         
	              <xsl:element name="rdf:Description">
	                  <xsl:attribute name="rdf:about">
	                      <xsl:text>'''+escape(url)+'''</xsl:text>
	                  </xsl:attribute><xsl:text>&#xa;</xsl:text>
			          <xsl:for-each select="//oai_dc:dc">
	                      <xsl:element name="dc:references">
                              <xsl:attribute name="rdf:resource">
				                  <xsl:value-of select="./dc:identifier"/>
                              </xsl:attribute>
	                      </xsl:element><xsl:text>&#xa;</xsl:text>
	                  </xsl:for-each>
	                  <xsl:element name="xsd:dateTime">'''+escape(getTimestamp())+'''</xsl:element><xsl:text>&#xa;</xsl:text>
	              </xsl:element><xsl:text>&#xa;</xsl:text>
	
	              <xsl:apply-templates />
	         </rdf:RDF>
	     </xsl:template>

	     <xsl:template match="text()|@*">
	     </xsl:template>
</xsl:stylesheet>'''


def get_xslt_tree(url):
    xslt_root = etree.XML(createStylesheet(url))
    return etree.XSLT(xslt_root)

def parse_string(url, s):
    #bugfix
    s = s.replace("http://www.openarchives.org/OAI/2.0/", "", 1)

    f = StringIO(s)
    d = etree.parse(f)
    
    result = get_xslt_tree(url)(d)
    if result:
        return str(result)
    else:
        return result



if __name__ == "__main__":
    #f = open("first_record_input.xml")
    #f = open("entscholar_List_Records_min.xml")
    #f = open("entscholar_List_Records.xml")
  
    f = open("/tmp/a")

    s = f.read()
    f.close()

    out = parse_string("test", s)
    print len(out), out
