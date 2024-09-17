from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from constant import cgv_url

# Chrome 웹 드라이버 설정
chrome_options = Options()
chrome_options.add_argument('--headless')  # 브라우저 창을 표시하지 않음
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# CGV 이벤트/시사회 URL 설정
driver.get(cgv_url)

# 페이지가 완전히 로드될 때까지 대기
time.sleep(5)  # 필요에 따라 대기 시간 조절

# 시사회 정보 추출
movie_list = driver.find_element(By.CLASS_NAME ,'searchingEventResult_list')  # 'event-class'는 실제 클래스명으로 변경

movie_info = movie_list.find_elements(By.TAG_NAME, 'li')

for movie in movie_info:
    movie_title = movie.find_element(By.CLASS_NAME, 'searchingEventName').text
    movie_date = movie.find_element(By.TAG_NAME, 'span').text
    print(f"Movie Title: {movie_title}")
    print(f"Movie Date: {movie_date}")
    print('-' * 40)

driver.quit()