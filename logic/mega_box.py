from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from common.constant import mega_box_url
from common.theater_enum import Theater
from db.database import insert_data

# Chrome 웹 드라이버 설정
chrome_options = Options()
chrome_options.add_argument('--headless')  # 브라우저 창을 표시하지 않음
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# 메가 박스 이벤트/시사회 URL 설정
driver.get(mega_box_url)

# 페이지가 완전히 로드될 때까지 대기
time.sleep(5)  # 필요에 따라 대기 시간 조절

# 시사회 정보 추출
movie_list = driver.find_element(By.CLASS_NAME ,'event-list')

movie_info = movie_list.find_elements(By.TAG_NAME, 'li')

insert_data_list = []

for movie in movie_info:
    movie_title = movie.find_element(By.CLASS_NAME, 'tit').text
    movie_date = movie.find_element(By.CLASS_NAME, 'date').text
    print(f"Movie Title: {movie_title}")
    print(f"Movie Date: {movie_date}")
    print('-' * 40)
    insert_data_list.append((movie_title, movie_date, Theater.MEGABOX.name))

driver.quit()

insert_data(insert_data_list)