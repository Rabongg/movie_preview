from selenium.webdriver.common.by import By
from db.database import get_data
from utils.utils import data_list_to_set
from utils.web_driver_manager import WebDriverManager

class Movie:
    def __init__(self, type: str, url: str, class_tag: str) -> None:
        self.type = type
        self.url = url
        self.class_tag = class_tag

    def get_movie_info(self, web_driver: WebDriverManager) -> list:
        try:
            web_driver.start_driver(self.url)
            
            movie_list = web_driver.get_element_by_class_name(self.class_tag)
            movie_info_list = movie_list.find_elements(By.TAG_NAME, 'li')
            
            insert_data_list = []
            
            data_set = data_list_to_set(get_data(self.type))
            
            for movie_info in movie_info_list:
                movie_title, movie_date = self.get_movie_title_and_date(movie_info=movie_info)
                
                if movie_title not in data_set:
                    insert_data_list.append((movie_title, movie_date, self.type))

            return insert_data_list

        except Exception:
            print('=========ERROR==========')
            raise Exception
            
    def get_movie_title_and_date(self, movie_info) -> tuple[str, str]:
        pass