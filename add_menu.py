import streamlit as st
import pymysql
from dotenv import load_dotenv
import os
import time

# .env 파일 로드
load_dotenv()

# .env 파일에서 MySQL 연결 정보 가져오기
host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
port = int(os.getenv('DB_PORT', 3306))  # 기본 포트는 3306
database_name = os.getenv('DB_NAME')


# MySQL 연결 설정
def connect_db():
    return pymysql.connect(
        host=host,
        user=user,
        password=password,
        port=port,
        database=database_name
    )

st.set_page_config(
    page_title="FISAFOODIE",
    page_icon="🧊"
)

# 제목
st.title(":knife_fork_plate: :rainbow[점메츄] - 메뉴 관리:knife_fork_plate:")
st.divider()

# 데이터베이스 설정
table_name = "restaurant_reviews"  # 실제 테이블 이름으로 변경

# 초기 데이터 로드 (여기서는 이미 데이터베이스가 존재한다고 가정)
st.divider()

# 새로운 메뉴 추가 섹션
st.subheader("오늘 :rainbow[점심]으로 무엇을 드셨나요?")
st.write('')

sex_ = st.radio("성별을 선택해주세요", ["남", "여"])
st.divider()

class_ = st.selectbox("트랙을 선택해주세요", ["ai_엔지니어링", "클라우드 서비스", "클라우드 엔지니어링"])
st.divider()

restaurant_name_ = st.text_input("방문한 식당을 입력해주세요")
st.divider()

menu_ = st.text_input("메뉴명을 입력해주세요 (여러가지 메뉴를 드셨다면 ','으로 구분 ex) 짜장면, 탕수육)")
st.divider()

photo_ = st.file_uploader("사진 파일을 업로드해주세요", type=["jpg", "jpeg", "png"])  # 확장자 제한
st.divider()

price_ = st.radio("가격대를 입력해주세요", ["5000원 미만", "5000원 ~ 8000원미만", "8000원 ~ 11000원미만", "11000원 ~ 14000원 미만", "14000원 이상"])
st.divider()

st.text("음식은 어떠셨나요?")
taste_ = st.feedback(key="taste", options="stars")
st.divider()

st.text("식당 위치는 어떠셨나요? (거리, 횡단보도 건넌 횟수, 엘레베이터 여부)")
accessibility_ = st.feedback(key="accessibility", options="stars")

st.divider()

# 데이터 삽입 버튼
if st.button("Add Menu Item"):
    try:
        # MySQL 연결
        connection = connect_db()
        cursor = connection.cursor()

        # 입력 데이터 준비
        menu_item = menu_
        price_item = price_
        sex_item = sex_
        class_item = class_
        restaurant_name_item = restaurant_name_
        taste_item = taste_
        accessibility_item = accessibility_

        # 사진이 업로드된 경우 BLOB으로 처리
        if photo_ is not None:
            # 사진을 바이너리로 읽기
            photo_binary = photo_.read()
            # 바이너리 데이터가 제대로 들어갔는지 확인 (디버깅용)
            st.write(f"파일 크기: {len(photo_binary)} bytes")  # 바이너리 크기 출력
        else:
            photo_binary = None  # 사진이 없을 경우 None 처리

        # 쿼리 작성
        insert_query = f"""
        INSERT INTO {table_name} (sex, class, restaurant_name, menu, picture, cost, flavor, accessibility)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        # 데이터 삽입
        cursor.execute(insert_query, (
            sex_item, class_item, restaurant_name_item, menu_item, photo_binary, price_item, taste_item, accessibility_item
        ))

        # 커밋 및 성공 메시지
        connection.commit()
        st.success(f"'{menu_item}'가 성공적으로 추가되었습니다.")

    except Exception as e:
        # 오류 발생 시 롤백
        connection.rollback()
        st.error(f"오류 발생: {e}")

    finally:
        # 연결 종료
        connection.close()
