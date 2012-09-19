# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from urllib2 import urlopen
# $ sudo apt-get install libxml libxml-dev libxslt-dev
# $ sudo easy_install lxml
from lxml import etree#, html
from lxml.cssselect import CSSSelector #sudo pip install cssselect
from pprint import pprint
import csv
category_list_url = "http://www.regulations.doe.gov/certification-data/Category.html"
category_list_flob = urlopen(category_list_url) #flob = file-like object
parser = etree.HTMLParser(encoding='utf-8')
category_list_tree = etree.parse(category_list_flob, parser)

# <codecell>

css = "table#report a"
product_selector = CSSSelector(css)
anchors = product_selector(category_list_tree)
base_url = "http://www.regulations.doe.gov"
product_page_urls = {}
for anchor in anchors:
    product_page_urls[anchor.text] = base_url + anchor.get('href')

# <codecell>

#pprint(product_page_urls)

# <codecell>

def get_subproduct_info(product_page_url):
    product_flob = urlopen(product_page_url)
    product_tree = etree.parse(product_flob, parser)
    '''return a dictionary of urls for subproduct csv files.'''
    subproduct_rows_css = ('table#report tbody tr')
    subproduct_rows_selector = CSSSelector(subproduct_rows_css)
    subproduct_rows = subproduct_rows_selector(product_tree)
    
    csv_path_dict = {}
    for row in subproduct_rows:
        subproduct_name =  row[0][0].text
        try:
            subproduct_csv_path = base_url + row[1][0].get('href')
            csv_path_dict[subproduct_name] = subproduct_csv_path
        except(IndexError):
           continue
    return csv_path_dict

# <codecell>

def open_csv_and_get_headers(url_to_csv):
    reader = csv.reader(urlopen(url_to_csv,'rU')) # a reader object
    header_row = reader.next() #the rest of the reader object is left to rot

    list_of_headers = []
    for attribute in range(len(header_row)):
        list_of_headers.append(header_row[attribute])
    list_of_headers.pop() # pop the appended newline off the end of the list
    return list_of_headers

# <codecell>

for product in product_page_urls.keys():
    subproducts = get_subproduct_info(product_page_urls[product])
    for subproduct in subproducts.keys():
        headers = open_csv_and_get_headers(subproducts[subproduct])
        for attribute in headers:
            print(product+'\t'+ subproduct + attribute)

# <codecell>


