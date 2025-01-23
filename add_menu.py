import streamlit as st
import pymysql
from dotenv import load_dotenv
import os
import time
import base64
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

# .env 파일 로드
load_dotenv()

# 기준 좌표 (위도, 경도)
CURRENT_LOCATION = (37.5707485, 126.8798744)

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


st.set_page_config(  # 항상 제일 먼저
    page_title="FISAFOODIE",
    page_icon="🍽",
    layout="wide"
)


def set_bg_hack(main_bg):  # background
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
sex_ = st.radio("", ["남", "여"], label_visibility="hidden", horizontal=True)

st.divider()

st.markdown('<div class="custom-text">🚩 수강 중인 트랙을 선택해주세요! </div>', unsafe_allow_html=True)
class_ = st.selectbox("", ["ai_엔지니어링", "클라우드 서비스", "클라우드 엔지니어링"])
st.divider()

st.markdown('<div class="custom-text">🏡 방문한 식당은 어디세요? </div>', unsafe_allow_html=True)
restaurant_name_ = st.text_input("", key="restaurant_name")
st.divider()

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
accessibility_ = st.feedback(key="accessibility", options="stars")

st.divider()

# 사진 업로드
st.markdown('<div class="custom-text">📸 식사 후 사진을 업로드 해주세요! </div>', unsafe_allow_html=True)
uploaded_image = st.file_uploader("이미지 파일을 업로드 해주세요", type=["png", "jpg", "jpeg"])

# 이미지를 바이너리로 저장할 함수
def image_to_binary(img):
    return img.read()

# 업로드된 이미지가 있으면 바이너리로 변환, 없으면 None을 저장
if uploaded_image is not None:
    image_data = image_to_binary(uploaded_image)
else:
    image_data = None  # 이미지가 없으면 None으로 설정

# '맛 평점'이 비어있으면 기본값(1)을 설정
taste_item = taste_ if taste_ else 1  # 기본값을 1로 설정 (원하는 값으로 변경 가능)

st.divider()
# 근처 식당을 찾는 함수
# OSM(OpenStreetMap) 기반 식당 검색 (디버깅 포함)
def find_nearest_restaurant(query):
    geolocator = Nominatim(user_agent="streamlit-app")
    location_results = geolocator.geocode(query, exactly_one=False, addressdetails=True)

    if not location_results:
        return None, "No results found"

    # 결과와 거리 계산
    filtered_results = []
    for location in location_results:
        coords = (location.latitude, location.longitude)
        distance = geodesic(CURRENT_LOCATION, coords).km
        st.write(f"DEBUG: 검색된 결과: {location.address}, 거리: {distance:.2f}km")
        if distance <= 3:  # 3km 이내
            filtered_results.append((location, distance))

    # 거리순 정렬
    filtered_results.sort(key=lambda x: x[1])

    if len(filtered_results) == 0:
        return None, "No results within 3km"
    elif len(filtered_results) == 1:
        return filtered_results[0][0].address, "Single result found"
    else:
        return filtered_results[0][0].address, "Multiple results, closest selected"


if st.button("등록"):
    try:
        # MySQL 연결
        connection = connect_db()
        cursor = connection.cursor()

        if restaurant_name_:
            # 1. 초기 검색
            address, status = find_nearest_restaurant(restaurant_name_)
            st.write(f"DEBUG: 초기 검색 결과 - Address: {address}, Status: {status}")

            # 2. 초기 검색 결과 처리
            if status == "No results found" or status == "No results within 3km":
                st.warning("검색 결과가 없습니다. '상암'을 추가하여 다시 검색합니다.")

                # "상암" 추가 후 재검색
                updated_search_query = f"{restaurant_name_} 상암"
                address, status = find_nearest_restaurant(updated_search_query)
                st.write(f"DEBUG: '상암' 추가 후 검색 결과 - Address: {address}, Status: {status}")

                # 재검색 결과 처리
                if status == "No results found":
                    st.error("'상암'을 추가했음에도 검색 결과가 없습니다. 다른 키워드로 다시 시도하세요.")
                elif status == "No results within 3km":
                    st.error("3km 내에 식당이 없습니다. 지역 정보를 더 구체적으로 입력해 보세요.")
                else:
                    # 최종 검색된 주소를 restaurant_name_에 반영
                    restaurant_name_ = address
                    st.success(f"검색 성공! 선택된 식당: {address}")
            else:
                # 검색된 결과가 있을 경우, 그대로 restaurant_name_에 반영
                restaurant_name_ = address
                st.success(f"검색 성공! 선택된 식당: {address}")
        else:
            st.warning("식당 이름을 입력해주세요.")

        # 여기서 restaurant_name_가 올바르게 업데이트 되었는지 확인
        st.write(f"DB에 저장될 식당 이름: {restaurant_name_}")

        # 입력 데이터 준비
        sex_item = sex_
        class_item = class_
        restaurant_name = restaurant_name_  # 최종적으로 업데이트된 식당 이름 사용
        menu_item = menu_
        price_item = price_  # 가격대 선택값
        picture_item = image_data  # 이미지 바이너리 데이터 (이미지가 없으면 None)
        flavor_item = taste_item  # 맛 평점
        accessibility_item = accessibility_  # 접근성 평점
        date_item = date_  # 선택한 날짜
        phone_item = phone_num  # 전화번호

        # 쿼리 작성
        insert_query = f"""
        INSERT INTO {table_name} (sex, class, restaurant_name, menu, cost, flavor, picture, accessibility, date, phone_num)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # 데이터 삽입
        cursor.execute(insert_query, (
            sex_item, class_item, restaurant_name, menu_item, price_item,
            flavor_item, picture_item, accessibility_item, date_item, phone_item
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
