from selenium.webdriver.common.by import By
import logging
from logic.movie import Movie

class LOTTE_CINEMA(Movie):
    def get_movie_title_and_date(self, movie_info) -> tuple[str, str]:
        movie_img = movie_info.find_element(By.TAG_NAME, 'img')
        movie_title = movie_img.get_attribute('alt')
        movie_date = movie_info.find_element(By.CLASS_NAME, 'itm_date').text
        logging.debug(f"Movie Title: {movie_title}")
        logging.debug(f"Movie Date: {movie_date}")
        logging.debug('-' * 40)
        
        return movie_title, movie_date