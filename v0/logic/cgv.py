from selenium.webdriver.common.by import By
import logging
from logic.movie import Movie

class CGV(Movie):
    def get_movie_title_and_date(self, movie_info) -> tuple[str, str]:
        movie_title = movie_info.find_element(By.CLASS_NAME, 'searchingEventName').text
        movie_date = movie_info.find_element(By.TAG_NAME, 'span').text
        logging.info(f"Movie Title: {movie_title}")
        logging.info(f"Movie Date: {movie_date}")
        logging.info('-' * 40)
        
        return movie_title, movie_date