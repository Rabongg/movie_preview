from selenium.webdriver.common.by import By
from common.constant import MEGA_BOX_URL, MEGA_BOX_CLASS_TAG
from common.theater_enum import Theater
from logic.movie import Movie
    
class MEGA_BOX(Movie):
    def get_movie_title_and_date(self, movie_info) -> tuple[str, str]:
        movie_title = movie_info.find_element(By.CLASS_NAME, 'tit').text
        movie_date = movie_info.find_element(By.CLASS_NAME, 'date').text
        print(f"Movie Title: {movie_title}")
        print(f"Movie Date: {movie_date}")
        print('-' * 40)
        
        return movie_title, movie_date