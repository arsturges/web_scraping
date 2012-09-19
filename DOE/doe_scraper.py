from urllib2 import urlopen
from lxml import etree # $ sudo apt-get install libxml libxml-dev libxslt-dev; sudo easy_install lxml
from lxml.cssselect import CSSSelector #sudo pip install cssselect
from pprint import pprint
import csv

category_list_url = "http://www.regulations.doe.gov/certification-data/Category.html"
category_list_flob = urlopen(category_list_url) # flob = file-like object
parser = etree.HTMLParser(encoding='utf-8') # html parser, otherwise it defaults to an xml parser
category_list_tree = etree.parse(category_list_flob, parser)


css = "table#report a" # anchor tags inside a table with id='report'
product_selector = CSSSelector(css)
anchors = product_selector(category_list_tree)
base_url = "http://www.regulations.doe.gov"
product_page_urls = {}
for anchor in anchors:
    product_page_urls[anchor.text] = base_url + anchor.get('href') # must prepend base_url to hrefs


def get_subproduct_info(product_page_url):
    '''return a dictionary of urls for subproduct csv files.
		csv_path_dict['subproduct name'] = "url_to_the_csv_file"'''
    product_flob = urlopen(product_page_url)
    product_tree = etree.parse(product_flob, parser)
    subproduct_rows_css = ('table#report tbody tr') # tr inside tbody inside table with id='report'
    subproduct_rows_selector = CSSSelector(subproduct_rows_css)
    subproduct_rows = subproduct_rows_selector(product_tree)
    
    csv_path_dict = {}
    for row in subproduct_rows:
        subproduct_name =  row[0][0].text
        try:
            subproduct_csv_path = base_url + row[1][0].get('href')
            csv_path_dict[subproduct_name] = subproduct_csv_path
        except(IndexError):
           continue # pass over subproducts that have no csv files
    return csv_path_dict


def open_csv_and_get_headers(url_to_csv):
	'''take a url to a csv file, open that file, read the headers, 
	and return those headers as a list.'''
	reader = csv.reader(urlopen(url_to_csv,'rU')) # a reader object
	header_row = reader.next() #the rest of the reader object is left to rot

	list_of_headers = []
	for attribute in range(len(header_row)):
		list_of_headers.append(header_row[attribute])
	list_of_headers.pop() # pop the appended newline off the end of the list
	return list_of_headers



with open('attributes.csv', 'wb') as csvfile:
	writer = csv.writer(csvfile)
	for product in product_page_urls.keys():
		subproducts = get_subproduct_info(product_page_urls[product])
		for subproduct in subproducts.keys():
			headers = open_csv_and_get_headers(subproducts[subproduct])
			for attribute in headers:
				#pass#print(product+ '\t' + subproduct + attribute)
				writer.writerow([product, subproduct, attribute])
