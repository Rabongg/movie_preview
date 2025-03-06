from selenium.webdriver.common.by import By
from logic.movie import Movie
import logging
    
class MEGA_BOX(Movie):
    def get_movie_title_and_date(self, movie_info) -> tuple[str, str]:
        movie_title = movie_info.find_element(By.CLASS_NAME, 'tit').text
        movie_date = movie_info.find_element(By.CLASS_NAME, 'date').text
        logging.debug(f"Movie Title: {movie_title}")
        logging.debug(f"Movie Date: {movie_date}")
        logging.debug('-' * 40)
        
        return movie_title, movie_date