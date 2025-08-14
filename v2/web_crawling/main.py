from common.constant import CGV_URL, MEGA_BOX_URL, LOTTE_CINEMA_URL, CGV_CLASS_TAG, MEGA_BOX_CLASS_TAG, LOTTE_CLASS_TAG
from logic.cgv import CGV
from logic.mega_box import MEGA_BOX
from logic.lotte_cinema import LOTTE_CINEMA
from common.theater_enum import Theater
from utils.web_driver_manager import WebDriverManager
from dotenv import load_dotenv
import os
import logging
import json

from logic.redis_publisher import RedisPublisher

def main():
    # env 파일 load 하기 위해서
    load_dotenv()
    
    # log 레벨 설정
    logging.basicConfig(level=logging.INFO, encoding="utf-8")  # UTF-8 설정
    
    try:
        movie_list = []
        
        web_driver = WebDriverManager()
        
        cgv = CGV(Theater.CGV, CGV_URL, CGV_CLASS_TAG)
        movie_list.extend(cgv.get_movie_info())
        
        mega = MEGA_BOX(Theater.MEGABOX, MEGA_BOX_URL, MEGA_BOX_CLASS_TAG)
        movie_list.extend(mega.get_movie_info(web_driver))

        lotte = LOTTE_CINEMA(Theater.LOTTE, LOTTE_CINEMA_URL, LOTTE_CLASS_TAG)
        movie_list.extend(lotte.get_movie_info(web_driver))
        
        topic = os.getenv('TOPIC')
        redis_publisher = RedisPublisher(topic)
        
        redis_publisher.publish_message(json.dumps(movie_list, default=lambda obj: obj.model_dump(), ensure_ascii=False))
    
    except Exception:
        logging.exception('ERROR!!!!!!!!')
        raise Exception
    finally:
        web_driver.quit_driver()

if __name__ == "__main__":
    main()
