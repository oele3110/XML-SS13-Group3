XML-SS13-Group3
===============

XML SS2013 Group3 Project

Link zur Veranstaltungsseite:

http://blog.ag-nbi.de/2013/03/20/vorlesung-xml-technologien-3/

Projektaufgabe:

Das Paradigma des klassischen Web Browsers greift bei einem Hypertext Web, nicht aber bei einem Web of Data, bei dem Rohdaten angesprochen werden oder Metadaten im Quelltext des Hypertextes eingebettet sind. Ebenso stammt der klassische Web Browser noch aus der Zeit, wo man von einem Menschen vor einem Computerarbeitsplatz ausging. Die vielfältigen Endgeräte der heutigen Zeit machen Schwächen des heutigen Browserkonzepts nicht zuletzt an Problemen der Synchronisation von Lesezeichen spürbar. Es ist sicher auch die Frage zulässig, ob ein Browser heutzutage überhaupt noch ein reiner Client sein muss oder ob er nicht auch gleichzeitig ein Server sein kann, der durch Nutzerinteraktion gewonnene Informationen wieder im Web zur Verfügung stellt (z.B. Verlaufsinformationen).

Ziel der Projektaufgabe ist es, dass Sie einen Web Data Brwoser prototypisch implementieren und dabei die Technologien der Vorlesung einsetzen. Der Web Data Browser soll das visuelle Browsen von Web Daten und Web Seiten erlauben. Das bedeutet, dass es egal ist, was ich als Ziel URL eingebe (Web Dokument, URI einer Linked Data Resource, URI eines OAI-Repositories), es wird immer eine visuelle Repräsentation gerendert und es gibt eine einheitliche History als RDF Graph.

Funktionale Anforderungen auf einen Blick:

- intern arbeitet der Browser mit dem RDF Datenmodell
- die Funktionalität muss an mindestens einer XML-Datenquelle gezeigt werden (one of http://www.openarchives.org/Register/BrowseSites) wobei aus dem XML per XSLT (wie hier http://simile.mit.edu/wiki/OAI-PMH_RDFizer) RDF zur internen Repräsentation erzeugt werden soll
- die Funktionalität muss an mindestens einer JSON Datenquelle gezeigt werden (z.B. http://www.europeana.eu/ oder https://dev.twitter.com/); JSON -> RDF
- die Funktionalität muss an mindestens einer Linked Data Quelle gezeigt werden (z.B. http://dbpedia.org)
- die Funktionalität muss an mindestens einer Seite mit eingebetteten Microdata gezeigt werden (z.B. http://stackoverflow.com oder http://bestbuy.com); Microdata -> RDF
- die Visualisierung soll automatisch in Abhängigkeit des Datentyps ausgewählt werden sofern das möglich ist (Beispiel: Karte für Geodaten), wenn nicht möglich Fallback-Visualisierung der Daten
- die Visualisierung basiert auf erweiterbaren Templates, die HTML erzeugen (XSLT für Templates wäre nice to have)
- der Browser erzeugt eine History, die alle gesammelten Daten als RDF Graph zur Verfügung stellt, dieser RDF Graph soll via SPARQL anfragbar sein
- es soll mindestens eine interessante Beispielquery geben, die diese History abfragt (Beispiele: Habe ich Seiten mit dem gleichen Tag besucht? Habe ich Produkte des selben Anbieters angesehen?)
