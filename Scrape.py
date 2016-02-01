import multiprocessing
import requests
import bs4

class Scraper:

    def __init__(self, root_url=None,page_url=None):

        self.root_url = root_url
        self.page_url = page_url
        
    def __call__(self):

        ad_links = self.get_ad_links(self.root_url+self.page_url)
        for ad_url in ad_links:
            print(ad_url)
        
        soup = self.get_soup(self.root_url+self.page_url)
        for i in range(10):

            next_page = self.get_next_page_url(soup)
            soup = self.get_soup(next_page)

            ad_links = self.get_ad_links(next_page)
            for ad_url in ad_links:
                print(ad_url)


    def get_soup(self, next_url=None):

        response = requests.get(next_url)
        soup = bs4.BeautifulSoup(response.text,"lxml")
        return soup 
       
    def get_next_page_url(self,soup):

        next_page = self.root_url+soup.find(rel="next")['href']
        return next_page
    
    def get_ad_links(self,url):
       
        ad_links = []
        soup = self.get_soup(url)
        ads = soup.select('div.flex-unit')

        for content in ads:
            try:
                paid_ad = content.select('div.unoverflowify')[0].select('div.r-margin')[0].select('span.fleft')[0].get_text()
            except:
                continue
            if paid_ad == 'Betalt plassering':
                print('Skipped paid ad')
                continue
            else:
                ad_links.append(self.root_url+content.select('a.userhistory')[0]['href'])

        return ad_links

    #def scrape_ad(self, url):

if __name__=='__main__':

    root_url = 'http://m.finn.no'
    page_url = '/bap/forsale/search.html?search_type=SEARCH_ID_BAP_ALL&sort=1'
    
    finn = Scraper(root_url,page_url)
    finn()

