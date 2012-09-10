import urllib2
# $ sudo apt-get install libxml libxml-dev libxslt-dev
# $ sudo easy_install lxml
from lxml import etree
doe_database_url = "http://www.regulations.doe.gov/certification-data/Category.html"
doe_database_text = urllib2.urlopen(doe_database_url)
html_source = doe_database_text.read()
doe_database_text.close()
