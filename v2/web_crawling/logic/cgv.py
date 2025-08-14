from selenium.webdriver.common.by import By
import logging
from logic.movie import Movie
from dto.movie_info_dto import MovieInfoDto
import requests

class CGV(Movie):
    def get_movie_info(self) -> list[MovieInfoDto]:
        insert_data_list = []
        try:
            response = requests.get(self.url)
            data = response.json()
            movie_info_list = data.get('data', {'list':[]}).get('list', [])
            
            for movie_info in movie_info_list:
                movie_title = movie_info.get('evntNm', 'Unknown Title')
                start_date = movie_info.get('evntStartDt', 'Unknown Start Date').split()[0]
                end_date = movie_info.get('evntEndDt', 'Unknown End Date').split()[0]
                movie_date = f"{start_date} ~ {end_date}"
                logging.debug(f"Movie Title: {movie_title}")
                logging.debug(f"Movie Date: {movie_date}")
                logging.debug('-' * 40)
                insert_data_list.append(MovieInfoDto(movie_title=movie_title, movie_date=movie_date, theater=self.type))
            return insert_data_list
        except requests.RequestException as e:
            logging.error(f"Request error: {e}")
            return []
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return []