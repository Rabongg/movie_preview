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
    load_dotenv()
    try:
        movie_list = []
        
        web_driver = WebDriverManager()
        
        cgv = CGV(Theater.CGV, CGV_URL, CGV_CLASS_TAG)
        movie_list.extend(cgv.get_movie_info(web_driver))
        
        mega = MEGA_BOX(Theater.MEGABOX, MEGA_BOX_URL, MEGA_BOX_CLASS_TAG)
        movie_list.extend(mega.get_movie_info(web_driver))

        lotte = LOTTE_CINEMA(Theater.LOTTE, LOTTE_CINEMA_URL, LOTTE_CLASS_TAG)
        movie_list.extend(lotte.get_movie_info(web_driver))
        
        topic = os.getenv('TOPIC')
        redis_publisher = RedisPublisher(topic)
        
        redis_publisher.publish_message(json.dumps(movie_list, default=lambda obj: obj.model_dump()))
    
    except Exception:
        logging.error('ERROR!!!!!!!!')
        raise Exception
    finally:
        web_driver.quit_driver()

if __name__ == "__main__":
    main()
