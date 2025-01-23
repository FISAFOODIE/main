import streamlit as st
import requests
import pymysql
import time
import os
import json
from dotenv import load_dotenv
import folium
from folium.plugins import MarkerCluster
from streamlit.components.v1 import html

load_dotenv()

host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
port = int(os.getenv('DB_PORT', 3306))
database_name = os.getenv('DB_NAME')

# 환경 변수 값 확인
# st.write(f"호스트: {host}, 사용자: {user}, 포트: {port}, DB: {database_name}")

headers = {
    "User-Agent": "YourAppName/1.0 (your-email@example.com)"
}

def get_mysql_connection():
    try:
        print("MySQL 연결 시도 중...")
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            port=port,
            database=database_name
        )
        print("MySQL 연결 성공!")
        return conn
    except pymysql.MySQLError as e:
        print(f"데이터베이스 연결 실패: {e}")
        return None

st.title(":knife_fork_plate: :rainbow[방문 식당 위치 보기] :knife_fork_plate:")

st.write("수강생들이 많이 먹은 가게 위치를 찾아보아요!")
st.divider()

def get_restaurant_names():
    print("가게 이름 가져오는 중...")
    conn = get_mysql_connection()
    if conn is None:
        return []

    cursor = conn.cursor()

    try:
        cursor.execute("SELECT restaurant_name FROM restaurant_reviews")
        restaurants = cursor.fetchall()
        print(f"가게 이름 가져오기 완료: {len(restaurants)}개")
        result = []
        for restaurant in restaurants:
            print(f"원본 가게 이름: '{restaurant[0]}'")  # 원본 가게 이름 출력
            result.append(restaurant[0])  # 원본 이름 그대로 사용

        conn.close()
        return result
    except pymysql.MySQLError as e:
        print(f"SQL 실행 오류: {e}")
        conn.close()
        return []

def get_location_from_name(name):
    print(f"'{name}' 위치 찾는 중...")
    url = f"https://nominatim.openstreetmap.org/search?q={name}&format=json&addressdetails=1&limit=1"

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if data:
                latitude = float(data[0]['lat'])
                longitude = float(data[0]['lon'])
                print(f"'{name}' 위치 찾기 완료!")
                return latitude, longitude
            else:
                return None, None
        else:
            return None, None
    except Exception as e:
        print(f"API 호출 중 오류 발생: {e}")
        return None, None

def load_mapped_restaurants():
    try:
        with open("mapping_data.json", "r") as f:
            mapped_restaurants = json.load(f)
        return mapped_restaurants
    except FileNotFoundError:
        return {}

def save_mapped_restaurants(mapped_restaurants):
    with open("mapping_data.json", "w") as f:
        json.dump(mapped_restaurants, f)

restaurant_data = []
mapped_restaurants = load_mapped_restaurants()

restaurants = get_restaurant_names()

# 가게 이름이 없으면 종료
if not restaurants:
    print("가게 이름을 가져오는 데 실패했습니다.")
    st.write("가게 이름을 가져오는 데 실패했습니다.")
else:
    # 위치를 새로 찾은 가게 데이터
    new_restaurant_data = []

    for store_name in restaurants:
        # 이미 처리된 가게라면 건너뛰기
        if store_name in mapped_restaurants:
            print(f"가게 '{store_name}'은 이미 매핑되었습니다.")
            continue

        # 각 가게 이름으로 위도, 경도를 찾기 위한 API 호출
        latitude, longitude = get_location_from_name(store_name)

        if latitude and longitude:
            # 유효한 위도, 경도가 있는 경우
            new_restaurant_data.append({
                "name": store_name,
                "latitude": latitude,
                "longitude": longitude
            })
            # 해당 가게 이름을 매핑된 목록에 추가
            mapped_restaurants[store_name] = {"latitude": latitude, "longitude": longitude}
        else:
            # 위치를 찾지 못하면 그냥 건너뛰고 계속 진행
            continue

        # 요청 간 지연을 추가하여 과도한 요청을 방지
        time.sleep(1)

    # 매핑된 데이터를 파일에 저장
    save_mapped_restaurants(mapped_restaurants)

    # Folium 지도를 생성
    if mapped_restaurants:  # 기본 매핑된 가게들
        print("기존 매핑된 가게들 지도에 표시 중...")
        # 지도 중심을 첫 번째 가게의 위치로 설정 (기존 데이터로 설정)
        first_location = list(mapped_restaurants.values())[0]  # 첫 번째 가게
        folium_map = folium.Map(location=[first_location['latitude'], first_location['longitude']], zoom_start=12)

        # MarkerCluster를 사용하여 마커를 그룹화
        marker_cluster = MarkerCluster().add_to(folium_map)

        # 기본 매핑된 가게 마커 추가
        for store_name, location in mapped_restaurants.items():
            # 가게 이름에서 첫 번째 쉼표 전까지 추출
            display_name = store_name.split(',')[0]  # 쉼표 앞부분만 사용
            folium.Marker(
                location=[location['latitude'], location['longitude']],
                popup=display_name,  # 마커 클릭 시 가게 이름만 표시
                icon=folium.Icon(icon="cloud")
            ).add_to(marker_cluster)

        # 새로 추가된 가게들 마커 추가
        if new_restaurant_data:
            print("새로 찾은 가게들 지도에 표시 중...")
            for restaurant in new_restaurant_data:
                display_name = restaurant['name'].split(',')[0]  # 쉼표 앞부분만 사용
                folium.Marker(
                    location=[restaurant['latitude'], restaurant['longitude']],
                    popup=display_name,  # 마커 클릭 시 가게 이름만 표시
                    icon=folium.Icon(icon="cloud", color="green")
                ).add_to(marker_cluster)

        # folium 지도 HTML로 변환 후 Streamlit에 표시
        folium_map_html = folium_map._repr_html_()
        html(folium_map_html, height=600)
    else:
        print("위치 정보를 찾지 못한 가게들은 지도에 표시되지 않습니다.")
        st.write("위치 정보를 찾지 못한 가게들은 지도에 표시되지 않습니다.")
