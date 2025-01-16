import pymysql
from dotenv import load_dotenv
import os
import csv

# .env 파일 로드
load_dotenv()

# .env 파일에서 MySQL 연결 정보 가져오기
host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
port = int(os.getenv('DB_PORT', 3306))  # 기본 포트는 3306
database_name = os.getenv('DB_NAME')

# CSV 파일 경로
csv_file_path = '../data/basic_data.csv'  # 실제 CSV 파일 경로

# MySQL 서버에 연결
connection = pymysql.connect(
    host=host,
    user=user,
    password=password,
    port=port,
    database=database_name
)

try:
    # 커서 생성
    cursor = connection.cursor()

    # CSV 파일을 UTF-8 인코딩으로 읽어서 데이터 삽입
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # 첫 번째 줄은 헤더이므로 건너뜁니다.

        # CSV 파일의 각 행에 대해 삽입 처리
        for row in csv_reader:
            # 쿼리문 작성 (restaurant_reviews 테이블의 컬럼에 맞게 작성)
            insert_query = """
            INSERT INTO restaurant_reviews (sex, class, restaurant_name, menu, picture, cost, flavor, accessibility)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            # CSV 파일에서 가져온 행(row) 데이터를 실행
            cursor.execute(insert_query, (
                row[0],  # sex
                row[1],  # class
                row[2],  # restaurant_name
                row[3],  # menu
                None,     # photo는 실제 파일 경로로 처리하거나 None으로 삽입
                row[5],   # price
                int(row[6]),   # taste
                int(row[7])    # accessibility
            ))

    # 커밋 및 성공 메시지
    connection.commit()
    print(f"'{csv_file_path}' 데이터가 'restaurant_reviews' 테이블에 성공적으로 삽입되었습니다.")

except Exception as e:
    print(f"오류 발생: {e}")
    connection.rollback()

finally:
    # 연결 종료
    connection.close()
