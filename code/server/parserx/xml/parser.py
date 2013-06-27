from lxml import etree
from StringIO import StringIO

XSLT_STYLESHEET = '''\
<xsl:stylesheet version="1.0"
     xmlns="http://www.openarchives.org/OAI/2.0/"
     xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
     xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
     xmlns:dc="http://purl.org/dc/elements/1.1/">

     <xsl:template match="ListRecords/*">
         <xsl:copy-of select="." />
     </xsl:template>


    <xsl:template match="text()|@*">
    </xsl:template>

</xsl:stylesheet>'''


def get_xslt_tree():
    xslt_root = etree.XML(XSLT_STYLESHEET)
    return etree.XSLT(xslt_root)

def parse_string(s):
    f = StringIO(s)
    d = etree.parse(f)
    
    result = get_xslt_tree()(d)
    if result:
        return str(result)
    else:
        return result


if __name__ == "__main__":
    f = open("entscholar_List_Records_min.xml")
    #f = open("entscholar_List_Records.xml")
    s = f.read()
    f.close()

    s = s.replace("http://www.openarchives.org/OAI/2.0/", "", 1)

    out = parse_string(s)
    print len(out), out
