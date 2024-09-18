import pymysql
from common.constant import HOST, PORT, USER, PASSWORD, DATABASE
from common.theater_enum import Theater

def db_connect():
  conn = pymysql.connect(host=HOST, port=PORT, user=USER, passwd=PASSWORD, database=DATABASE, cursorclass=pymysql.cursors.DictCursor)

  cur = conn.cursor()
  
  return cur, conn


def insert_data(movie_info: list):
  cursor, connection = db_connect()
  
  print(movie_info)
  try:
    sql = 'insert into movie_curtain_call_info (title, period, theater, created_dt) values (%s, %s, %s, now())'
    
    cursor.executemany(sql, movie_info)
    connection.commit()
  
  except Exception as e:
    print('========== ERROR ==========')
    print(e)
    
  finally:
    cursor.close()
    connection.close()
    
def get_data(theater: str) -> list[dict]:
  cursor, connection = db_connect()
  try:
    sql = 'select * from movie_curtain_call_info where theater = %s'
    
    cursor.execute(sql, (theater))
    result = cursor.fetchall()
    
    return result
  
  except Exception as e:
    print('========== ERROR ==========')
    print(e)
  finally:
    cursor.close()
    connection.close()
    
# insert_data()
get_data(theater=Theater.CGV.name)