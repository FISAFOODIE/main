import streamlit as st
import requests
import pandas as pd
import mysql.connector
import time
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경 변수로 MySQL 연결 정보 가져오기
host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
port = int(os.getenv('DB_PORT', 3306))  # 기본 포트는 3306
database_name = os.getenv('DB_NAME')

# 사용자 정의 User-Agent 헤더 추가
headers = {
    "User-Agent": "YourAppName/1.0 (your-email@example.com)"  # 사용자 이름과 이메일을 넣으세요
}

# MySQL 연결 함수
def get_mysql_connection():
    try:
        print("MySQL 연결 중...")
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            port=port,
            database=database_name
        )
        print("MySQL 연결 성공!")
        return conn
    except mysql.connector.Error as e:
        print(f"데이터베이스 연결 실패: {e}")
        return None

# MySQL DB에서 가게 이름 가져오기
def get_restaurant_names():
    print("가게 이름 가져오는 중...")
    conn = get_mysql_connection()
    if conn is None:
        print("MySQL 연결 실패!")
        return []

    cursor = conn.cursor()

    try:
        # 실제 존재하는 테이블과 컬럼 이름을 확인 후 쿼리 작성
        cursor.execute("SELECT restaurant_name FROM restaurant_reviews")
        restaurants = cursor.fetchall()
        print(f"가게 이름 가져오기 완료: {len(restaurants)}개")
        conn.close()
        return restaurants
    except mysql.connector.Error as e:
        print(f"SQL 실행 오류: {e}")
        conn.close()
        return []

# 가게 이름으로 위치를 찾기 위한 Nominatim API 호출
def get_location_from_name(restaurant_name):
    print(f"'{restaurant_name}' 위치 찾는 중...")
    url = f"https://nominatim.openstreetmap.org/search?q={restaurant_name}&format=json&addressdetails=1&limit=1"

    try:
        # Nominatim API 호출
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # JSON 형식으로 응답을 파싱
            data = response.json()
            if data:
                latitude = float(data[0]['lat'])
                longitude = float(data[0]['lon'])
                print(f"'{restaurant_name}' 위치 찾기 완료!")
                return latitude, longitude
            else:
                print(f"'{restaurant_name}' 위치 정보 없음.")
                return None, None
        else:
            print(f"'{restaurant_name}' API 요청 실패: {response.status_code}")
            return None, None
    except Exception as e:
        print(f"API 호출 중 오류 발생: {e}")
        return None, None


# Main
restaurant_data = []

# MySQL에서 가게 이름 가져오기
restaurants = get_restaurant_names()

if not restaurants:
    print("가게 이름을 가져오는 데 실패했습니다.")
else:
    for restaurant in restaurants:
        store_name = restaurant[0]

        # 각 가게 이름으로 위도, 경도를 찾기 위한 API 호출
        latitude, longitude = get_location_from_name(store_name)

        if latitude and longitude:
            # 유효한 위도, 경도가 있는 경우
            restaurant_data.append({
                "name": store_name,
                "latitude": latitude,
                "longitude": longitude
            })
        else:
            print(f"가게 '{store_name}'의 위치를 찾을 수 없습니다.")

        # 요청 간 지연을 추가하여 과도한 요청을 방지
        time.sleep(1)

# DataFrame 생성
df = pd.DataFrame(restaurant_data)

# 지도에 마커 표시
if not df.empty:
    print("지도에 가게 마커 표시 중...")
    st.map(df[['latitude', 'longitude']])
else:
    print("가게 정보를 지도에 표시할 수 없습니다.")
