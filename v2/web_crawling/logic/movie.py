from selenium.webdriver.common.by import By
from utils.web_driver_manager import WebDriverManager
import logging

from dto.movie_info_dto import MovieInfoDto

class Movie:
    def __init__(self, type: str, url: str, class_tag: str) -> None:
        self.type = type
        self.url = url
        self.class_tag = class_tag

    def get_movie_info(self, web_driver: WebDriverManager) -> list[MovieInfoDto]:
        try:
            web_driver.start_driver(self.url)
            
            movie_list = web_driver.get_element_by_class_name(self.class_tag)
            movie_info_list = movie_list.find_elements(By.TAG_NAME, 'li')
            
            insert_data_list = []
            
            
            for movie_info in movie_info_list:
                movie_title, movie_date = self.get_movie_title_and_date(movie_info=movie_info)
                
                insert_data_list.append(MovieInfoDto(movie_title=movie_title, movie_date=movie_date, theater=self.type))

            return insert_data_list

        except Exception:
            logging.error('=========ERROR==========')
            raise Exception
    
    # 상속받은 class에서 구현할 method
    def get_movie_title_and_date(self, movie_info) -> tuple[str, str]:
        pass