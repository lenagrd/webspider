import pauk2 as p

f = p.SimpleCrawler('urls.csv', 2, 'http://coreyms.com/')
lst = f.buil_url_list()
f.save_to_csv("urls.csv")