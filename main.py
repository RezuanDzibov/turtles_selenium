from selenium import webdriver
from selenium.webdriver.common.by import By


class MainCrawler:
    def __init__(self) -> None:
        self.driver = webdriver.Chrome()
        
    def scrap(self) -> None:
        self.driver.get('https://www.scrapethissite.com/pages/frames/')
        self.switch_to_frame()
        turtle_card = self.driver.find_elements(By.CLASS_NAME, 'turtle-family-card')
    
    def switch_to_frame(self) -> None :
        self.driver.switch_to.frame(self.driver.find_element(By.TAG_NAME, 'iframe'))
                           
    def __del__(self):
        self.driver.close()


if __name__ == '__main__':
    crawler = MainCrawler()
    crawler.scrap()