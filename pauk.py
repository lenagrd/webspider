from bs4 import BeautifulSoup
import requests
#from urllib.parse import urlparse


class SimpleCrawlerOld:

    url_is_visited = 1
    url_not_visited = 0

    def __init__(self, filename, depth, main_url):
        self.filename = filename
        self.depth = depth
        self.list_url = []
        self.main_url = main_url
        self.list_url.append([main_url, 1, self.url_not_visited, 1])


    def mark_url_as_visited (self, url_element):
        for l in  [elem for elem in self.list_url if elem[0] == url_element[0]]:
            l[2] = self.url_is_visited

    def crawl_and_scrape_url(self, url_element, layer):

        source = requests.get(url_element[0]).text
        #print(" Page: " +  url_element[0])
        soup = BeautifulSoup(source, 'lxml')

        all_a_tags_in_html = soup.find_all('a', href=True)


        for a_tag in all_a_tags_in_html:
            if str(a_tag['href']).startswith(self.main_url):

                # existing_url = [a,b,c,d]. a = url, b = frequency, c = IsVisited, d = depth
                existing_url = [x for x in self.list_url if x[0] == a_tag['href']]

                if existing_url: # increment frequency
                    existing_url[0][1] += 1
                else:  #create new  url if  url within the requested depth
                    if (layer<self.depth):
                        self.list_url.append([a_tag['href'], 1, self.url_not_visited,  layer +1])


    def buil_url_list(self ):

        #print (self.list_url)

        for layer in range(1, self.depth+1):
            print("traversing layer ..... " + str(layer))
            for elem in self.list_url :
                if elem[3] == layer and elem[2] != self.url_is_visited:
                    self.crawl_and_scrape_url(elem, layer)
                    # mark url l as visited
                    self.mark_url_as_visited(elem)

        return self.list_url

    def save_To_Csv(self, csvfile):
        csv = open(csvfile, "w")

        columnTitleRow = "url, frequency, level\n"
        csv.write(columnTitleRow)

        for a, b, c, d in self.list_url:
            url = a
            frequency = b
            layer = c
            row = url + "," + str(frequency) + "," +  str(layer)  + "\n"
            csv.write(row)




#
f = SimpleCrawlerOld('urls.csv',2, 'http://coreyms.com/')

lst = f.buil_url_list()

f.save_To_Csv("urls.csv")


