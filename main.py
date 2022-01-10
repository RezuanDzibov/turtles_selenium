import csv
from typing import Optional

from selenium import webdriver
from selenium.webdriver.common.by import By


class CSVMixin:
    headers = list()
    
    def __init__(self, csv_filename: str = None) -> None:
        csv_filename = self.get_csv_filename(csv_filename=csv_filename)
        self.csvfile = open(csv_filename, 'w', newline='', encoding='utf-8')
        self.writer = csv.DictWriter(self.csvfile, fieldnames=self.headers)
        self.writer.writeheader()
        
    def write_to_csv(self, row: dict):
        self.writer.writerow(row)
        
    def get_csv_filename(self, csv_filename: Optional[str]) -> str:
        """[summary]
            Check if csv_filename was provided.
            
        Args:
            csv_filename (Optional[str]): 
        Returns:
            str: csv_filename
        """
        if csv_filename:
            if csv_filename.endswith('.csv'):
                return csv_filename
            else:
                return f'{csv_filename}.csv'
        else:
            return 'turtle_families.csv'
        
    def __del__(self):
        self.csvfile.close()


class MainCrawler(CSVMixin):
    headers = ['turtle_family_name', 'turtle_family_description']
    
    def __init__(self, csv_filename: str = None) -> None:
        self._url = 'https://www.scrapethissite.com/pages/frames/'
        self._driver = webdriver.Chrome()
        super().__init__(csv_filename=csv_filename)
        
    def scrap(self) -> None:
        self._driver.get(self._url)
        self._switch_to_frame()
        turtle_family_cards = self._driver.find_elements(By.CLASS_NAME, 'turtle-family-card')
        turtle_family_links = [author.find_element(By.CLASS_NAME, 'btn').get_attribute('href') for author in turtle_family_cards]
        for turtle_family_link in turtle_family_links:
            turtle_family_info = self._scrap_turtle_family_page(turtle_family_link=turtle_family_link)
            self.write_to_csv(row=turtle_family_info)
                
    def _switch_to_frame(self) -> None :
        self._driver.switch_to.frame(self._driver.find_element(By.TAG_NAME, 'iframe'))
        
    def _scrap_turtle_family_page(self, turtle_family_link) -> dict:
        self._driver.get(turtle_family_link)
        turtle_family_dict = dict()
        turtle_family_dict['turtle_family_name'] = self._driver.find_element(By.CLASS_NAME, 'family-name').text
        turtle_family_dict['turtle_family_description'] = self._driver.find_element(By.CLASS_NAME, 'lead').text
        return turtle_family_dict  

    def __del__(self):
        self._driver.close()
        super().__del__()