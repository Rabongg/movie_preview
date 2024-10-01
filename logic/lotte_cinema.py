from selenium.webdriver.common.by import By
from common.constant import LOTTE_CINEMA_URL, LOTTE_CLASS_TAG
from common.theater_enum import Theater
from logic.movie import Movie

class LOTTE_CINEMA(Movie):
    def get_movie_title_and_date(self, movie_info) -> tuple[str, str]:
        movie_img = movie_info.find_element(By.TAG_NAME, 'img')
        movie_title = movie_img.get_attribute('alt')
        movie_date = movie_info.find_element(By.CLASS_NAME, 'itm_date').text
        print(f"Movie Title: {movie_title}")
        print(f"Movie Date: {movie_date}")
        print('-' * 40)
        
        return movie_title, movie_date

movie = LOTTE_CINEMA(Theater.LOTTE.name, LOTTE_CINEMA_URL, LOTTE_CLASS_TAG)

movie.get_movie_info()