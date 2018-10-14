from bs4 import BeautifulSoup
import requests
import csv
import time


class SimpleCrawler:

    url_is_visited = 1
    url_not_visited = 0

    def __init__(self, filename, depth, main_url):
        self.filename = filename
        self.depth = depth
        self.dict_url = {main_url:{'frequency':1, 'visited':0,'layer':1}}
        self.main_url = main_url


    def append_to_urls(self, page_urls,layer):

        for key,value in page_urls.items():
            if key in self.dict_url:
                self.dict_url[key]['frequency'] += value
            else:
                self.dict_url[key] = {'frequency': value, 'visited':0, 'layer' :layer}



    def mark_url_as_visited (self, url):

        if url in self.dict_url:
           self.dict_url[url]['visited'] = 1

    def get_not_visited_urls(self,layer):

        d = dict((k, v) for k, v in self.dict_url.items() if v['visited'] == 0 and v['layer'] <= layer)

        return d


    def get_page_urls(self, url, layer):

        source = requests.get(url).text
        soup = BeautifulSoup(source, 'lxml')

        _dict_frequency = {}

        all_a_tags_in_html = soup.find_all('a', href=True)

        for a_tag in all_a_tags_in_html:
            if str(a_tag['href']).startswith(self.main_url):

                url = a_tag['href']

                if url in  _dict_frequency: # increment frequency
                    _dict_frequency[url] += 1
                else:
                    if (layer<self.depth):
                        _dict_frequency[url] = 1

        return _dict_frequency



    def buil_url_list(self ):

        for layer in range(1, self.depth+1):

            non_visited_urls  = self.get_not_visited_urls(layer )
            print("traversing layer ..... " + str(layer))
            print('non visited Urls: '  + str(len(non_visited_urls)))

            for url in non_visited_urls:

                    #get page urls in a temp dictionary
                    page_urls  = self.get_page_urls(url, layer)

                    #add to global list of urls, with values=  0 if url does not exist
                    self.append_to_urls(page_urls,layer+1)

                    # mark url l as visited in a global list
                    self.mark_url_as_visited(url)



        return self.dict_url


    def save_to_csv(self, csvfile):

        with open(csvfile, mode='w') as urlfile:
            f_writer = csv.writer(urlfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for url, value in self.dict_url.items():

                f_writer.writerow([url, value['frequency']])


print("Starting...")

if __name__ == "__main__":
    print("Starting...")

    start = time.time()
    main_url = "http://coreyms.com/"

    f = SimpleCrawler('urls.csv', 3, main_url)
    lst = f.buil_url_list()
    f.save_to_csv("urls.csv")

    print('Entire job took:', time.time() - start)
