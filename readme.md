#spider


#libraries to import:
from bs4 import BeautifulSoup
import requests
import csv

#code sample:
f = p.SimpleCrawler('urls.csv', 2, 'http://coreyms.com/')
lst = f.buil_url_list()
f.save_to_csv("urls.csv")