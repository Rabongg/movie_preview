from selenium.webdriver.common.by import By
from common.constant import CGV_URL, CGV_CLASS_TAG
from common.theater_enum import Theater
from logic.movie import Movie

class CGV(Movie):
    def get_movie_title_and_date(self, movie_info) -> tuple[str, str]:
        movie_title = movie_info.find_element(By.CLASS_NAME, 'searchingEventName').text
        movie_date = movie_info.find_element(By.TAG_NAME, 'span').text
        print(f"Movie Title: {movie_title}")
        print(f"Movie Date: {movie_date}")
        print('-' * 40)
        
        return movie_title, movie_date

movie = CGV(Theater.CGV.name, CGV_URL, CGV_CLASS_TAG)

movie.get_movie_info()