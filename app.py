import pymysql
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# .env 파일에서 MySQL 연결 정보 가져오기
host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
port = int(os.getenv('DB_PORT', 3306))  # 기본 포트는 3306
database_name = os.getenv('DB_NAME')

# CSV 파일 경로
csv_file_path = './data/basic_data.csv'

# MySQL 서버에 연결
connection = pymysql.connect(
    host=host,
    user=user,
    password=password,
    port=port,
    database=database_name,
    local_infile=True  # LOCAL INFILE을 사용하려면 이 옵션을 True로 설정
)

try:
    # 커서 생성
    cursor = connection.cursor()

    # LOAD DATA LOCAL INFILE 명령어로 CSV 파일을 MySQL로 로드
    load_data_query = f"""
    LOAD DATA LOCAL INFILE '{csv_file_path}'
    INTO TABLE basic_data
    FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
    IGNORE 1 LINES;
    """
    cursor.execute(load_data_query)
    connection.commit()
    print(f"'{csv_file_path}' 데이터가 'basic_data' 테이블에 성공적으로 삽입되었습니다.")

except Exception as e:
    print(f"오류 발생: {e}")
    connection.rollback()

finally:
    # 연결 종료
    connection.close()
