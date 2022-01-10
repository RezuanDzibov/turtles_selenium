from selenium import webdriver



class MainCrawler:
    def __init__(self) -> None:
        self.driver = webdriver.Chrome()
        
    def scrap(self) -> None:
        self.driver.get('https://www.scrapethissite.com/pages/frames/')    
        
    def __del__(self):
        self.driver.close()