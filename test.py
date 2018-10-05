import pauk

f = pauk.SimpleCrawler('urls.csv', 2, 'http://coreyms.com/')

lst = f.buil_url_list()

f.save_To_Csv("urls.csv")