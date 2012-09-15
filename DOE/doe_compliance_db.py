import urllib2
# $ sudo apt-get install libxml libxml-dev libxslt-dev
# $ sudo easy_install lxml
from lxml import etree
from lxml.cssselect import CSSSelector #sudo pip install cssselect
doe_database_url = "http://www.regulations.doe.gov/certification-data/Category.html"
flob = urllib2.urlopen(doe_database_url)
html_source = flob.read()
flob.close()

html = etree.HTML(html_source)
css = "td>a"
selector = CSSSelector(css)
anchors = selector(html)
for anchor in anchors:
	print etree.tostring(anchor)
#rows = html.find(".//table[@id='report']//tr[4]")
#print etree.tostring(rows)
#categories = []
