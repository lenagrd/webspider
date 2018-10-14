# this library provides Parallel versions of the map function
from multiprocessing import Pool

# Dummy is an exact clone of the multiprocessing module. The only difference is that,
# whereas multiprocessing works with processes,
# the dummy module uses threads (which come with all the usual Python limitations)
from multiprocessing.dummy import Pool as ThreadPool

import requests
from bs4 import BeautifulSoup
import csv
import time


# This line creates a bunch of available workers,
# starts them up so that they’re ready to do some work,
# and stores all of them in variable so that they’re easily accessed.
# This sets the number of workers in the pool.
# If you leave it blank, it will default to the number of Cores in your machine

class SimpleCrawlerMulti:

    url_is_visited = 1
    url_not_visited = 0

    def __init__(self, filename, depth, main_url):
        self.filename = filename
        self.depth = depth
        self.dict_url = {main_url: {'frequency': 1, 'visited': 0, 'layer': 1}}
        self.main_url = main_url

    def get_page_urls(self, url,layer):

        source = requests.get(url).text
        soup = BeautifulSoup(source, 'lxml')

        _dict_frequency = {}

        #print('inside get_page_urls  with the level ' + str(layer) + ' and url=' + url)

        all_a_tags_in_html = soup.find_all('a', href=True)

        for a_tag in all_a_tags_in_html:
            if str(a_tag['href']).startswith(self.main_url):

                url = a_tag['href']

                if url in _dict_frequency:  # increment frequency
                    _dict_frequency[url] += 1
                else:
                    if (layer < self.depth):
                        _dict_frequency[url] = 1

        # add to global list of urls, with values=  0 if url does not exist
        self.append_to_urls(_dict_frequency, layer + 1)

        # mark url l as visited in a global list
        self.mark_url_as_visited(url)

        #return _dict_frequency


    def append_to_urls(self, page_urls, layer):

        for key, value in page_urls.items():
            if key in self.dict_url:
                self.dict_url[key]['frequency'] += value
            else:
                self.dict_url[key] = {'frequency': value, 'visited': 0, 'layer': layer}


    def mark_url_as_visited(self, url):

        if url in self.dict_url:
            self.dict_url[url]['visited'] = 1


    def get_not_visited_urls(self, layer):

        d = dict((k, v) for k, v in self.dict_url.items() if v['visited'] == 0 and v['layer'] <= layer)

        return d


    def save_to_csv(self, csvfile):

        with open(csvfile, mode='w') as urlfile:
            f_writer = csv.writer(urlfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for url, value in self.dict_url.items():

                f_writer.writerow([url, value['frequency']])


    def buil_url_list(self):

        for layer in range(1, self.depth + 1):

            non_visited_urls = self.get_not_visited_urls(layer)
            print("traversing layer ..... " + str(layer))
            print('non visited Urls: ' + str(len(non_visited_urls)))

            if len(non_visited_urls)>=2:

                # param_layer = [layer] * len(non_visited_urls)
                # params = zip(list(non_visited_urls.keys()), param_layer)
                # print('number of parameter pairs that go into map function: ' + str(len(list(params))))

                number_of_workers = 15
                pool = ThreadPool(number_of_workers)

                results = pool.map(lambda p: self.get_page_urls(p, layer), list(non_visited_urls.keys()))
                #results = pool.map(self.get_page_urls, params)

                pool.close()
                pool.join()

            if len(non_visited_urls) == 1:
                # dictionary has only one element. get this element through converting to list first
                single_non_visited_url = list(non_visited_urls.keys())[0]

                self.get_page_urls(single_non_visited_url, layer)

        return self.dict_url





if __name__ == "__main__":
    print("Starting...")
    main_url = "http://coreyms.com/"
    start = time.time()

    f = SimpleCrawlerMulti('urls.csv', 3, main_url)
    lst = f.buil_url_list()
    f.save_to_csv("urls.csv")

    print('Entire job took:', time.time() - start)



