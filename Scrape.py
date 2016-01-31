import multiprocessing
import requests
import bs4

class Scraper:

    def __init__(self, root_url=None,page_url=None):

        self.root_url = root_url
        self.page_url = page_url
        

    def get_soup(self, next_url=None):

        response = requests.get(next_url)
        self.soup = bs4.BeautifulSoup(response.text,"lxml")
        
       
    def get_next_page_url(self):
        next_pages = [] 
        
        pages = self.soup.select('span.hidelt768')

        for links in pages: 
            for link in links:
                try:
                    next_pages.append(self.root_url+link['href'])
                    print(link['href'])
                except:
                    continue

        return next_pages
    
    def scrape_page(self,first_page=None):
       
        ad_links = []
        self.get_soup(first_page)
        ads = self.soup.select('div.flex-unit')
        for content in ads:
            try:
                paid_ad = content.select('div.unoverflowify')[0].select('div.r-margin')[0].select('span.fleft')[0].get_text()
            except:
                continue
            if paid_ad == 'Betalt plassering':
                print('Skipped paid ad')
                continue
            else:
                ad_links.append(content.select('a.userhistory')[0]['href'])
        
        for links in ad_links:
            print(self.root_url+links)


if __name__=='__main__':

    root_url = 'http://m.finn.no'
    page_url = '/bap/forsale/search.html?search_type=SEARCH_ID_BAP_ALL&sort=1'
    
    finn = Scraper(root_url,page_url)
    finn.scrape_page(root_url+page_url)

