import streamlit as st
import pymysql
from dotenv import load_dotenv
import os
import time
import base64

# .env 파일 로드
load_dotenv()
# .env 파일에서 MySQL 연결 정보 가져오기
host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
port = int(os.getenv('DB_PORT', 3306))
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

st.set_page_config( # 항상 제일 먼저
    page_title="FISAFOODIE",
    page_icon="🍽",
    layout="wide"
)


def set_bg_hack(main_bg): # background
    # Extract file extension (e.g., png, jpg)
    main_bg_ext = main_bg.split('.')[-1]
    
    # Read and encode the image
    with open(main_bg, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
        
    # Apply background via custom CSS
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url(data:image/{main_bg_ext};base64,{encoded_string});
            background-size: 100% 100%;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


set_bg_hack(r"bg.png")

# CSS 파일 읽어오는 코드
with open("./default.css") as f:
    css = f.read()

# CSS 적용 코드
st.markdown(f'<style> {css} </style>',
    unsafe_allow_html=True,
)

# 제목
st.markdown("<div class='title'>🍴 점메츄 프로젝트 🍴</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>FISA 아카데미 학생들을 위한 맛집 찾기 페이지</div>", unsafe_allow_html=True)
st.divider()


# 데이터베이스 설정
table_name = "restaurant_reviews"  # 실제 테이블 이름으로 변경

# 초기 데이터 로드 (여기서는 이미 데이터베이스가 존재한다고 가정)

# 새로운 메뉴 추가 섹션
st.subheader("오늘 :rainbow[점심]으로 무엇을 드셨는지 알려주세요 !")
st.divider()

st.markdown('<div class="custom-text">❤ 폰 번호 뒷자리를 알려주시면 각 반에 1명씩 추첨하여 매머드 깊티를 드려요 ❤</div>', unsafe_allow_html=True)
phone_num = st.text_input("")
st.divider()

st.markdown('<div class="custom-text">👦👩 성별을 선택해주세요! </div>', unsafe_allow_html=True)
sex_ = st.radio("", ["남", "여"], horizontal = True)
st.divider()

st.markdown('<div class="custom-text">🚩 수강 중인 트랙을 선택해주세요! </div>', unsafe_allow_html=True)
class_ = st.selectbox("", ["ai_엔지니어링", "클라우드 서비스", "클라우드 엔지니어링"])
st.divider()

st.markdown('<div class="custom-text">🏡 방문한 식당은 어디세요? </div>', unsafe_allow_html=True)
restaurant_name_ = st.text_input("", key="restaurant_name")
st.divider()

# st.write('') # 줄 띄우기
# if st.button('눈 그만') == False: # 창에 눈 날리기
#     st.snow()

# if st.button('풍선 그만') == False: # 창에 풍선 날리기
#     st.balloons()

st.markdown('<div class="custom-text">🍔 어떤 메뉴를 드셨나요? </div>', unsafe_allow_html=True)
menu_ = st.text_input("(여러가지 메뉴를 드셨다면 ','으로 구분 ex) 짜장면, 탕수육)")

st.divider()
st.markdown('<div class="custom-text">💰 가격은 얼마였나요? </div>', unsafe_allow_html=True)
price_ = st.radio("", ["5000원 미만", "5000원 ~ 8000원미만", "8000원 ~ 11000원미만", "11000원 ~ 14000원 미만", "14000원 이상"])

st.divider()
st.markdown('<div class="custom-text">📆 식사하신 날짜는 언제인가요? </div>', unsafe_allow_html=True)
date_ = st.date_input("", format="YYYY-MM-DD")

st.divider()
st.markdown('<div class="custom-text">🍜 음식은 어떠셨나요? </div>', unsafe_allow_html=True)
taste_ = st.feedback(key="taste", options="stars")

st.divider()
st.markdown('<div class="custom-text">🚶 식당 접근성은 어땠나요? (거리, 횡단보도 건넌 횟수, 엘리베이터 여부)</div>', unsafe_allow_html=True)
accessibility_ = st.feedback(key="accessibility",options="stars")

st.divider()

if st.button("등록"):
    try:
        # MySQL 연결
        connection = connect_db()
        cursor = connection.cursor()

        # 입력 데이터 준비
        sex_item = sex_
        class_item = class_
        restaurant_name_item = restaurant_name_
        menu_item = menu_
        price_item = price_  # 가격대 선택값
        taste_item = taste_  # 별점
        accessibility_item = accessibility_  # 별점
        date_item = date_  # 선택한 날짜
        phone_item = phone_num  # 전화번호

        # 쿼리 작성
        insert_query = f"""
        INSERT INTO {table_name} (sex, class, restaurant_name, menu, cost, flavor, accessibility, date, phone_num)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # 데이터 삽입
        cursor.execute(insert_query, (
            sex_item, class_item, restaurant_name_item, menu_item, price_item,
            taste_item, accessibility_item, date_item, phone_item
        ))

        # 커밋 및 성공 메시지
        connection.commit()
        st.success("등록 성공! 새로고침 후 등록해주세요.")

    except Exception as e:
        # 오류 발생 시 롤백
        connection.rollback()
        st.error(f"오류 발생: {e}")

    finally:
        # 연결 종료
        connection.close()