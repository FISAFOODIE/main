import streamlit as st
import db_util as db

st.title("점메츄 - 메뉴 관리")

# 데이터베이스 설정
db_name = "dummy_database"
table_name = "dummy_table"
default_csv_file = "dummydata.csv"

# 초기 데이터 로드
try:
    # 항상 dummydata.csv를 데이터베이스에 로드
    db.create_table_with_csv(default_csv_file, db_name, table_name)
    st.success(f"Database '{db_name}.db' has been initialized with '{default_csv_file}'.")
except Exception as e:
    st.error(f"Error initializing data: {e}")

st.divider()

# 새로운 메뉴 추가 섹션
st.subheader("오늘 점심으로 무엇을 드셨나요?")

sex_ = st.radio("성별을 입력해주세요", ["남", "여"])
class_ = st.radio("트랙을 입력해주세요", ["ai_엔지니어링", "클라우드 서비스", "클라우드 엔지니어링"])
restaurant_name_ = st.text_input("방문한 식당을 입력해주세요")
menu_ = st.text_input("메뉴명을 입력해주세요 (여러가지 메뉴를 드셨다면 ','으로 구분 ex) 짜장면, 탕수육)")
photo_ = st.file_uploader("사진 파일을 업로드해주세요")
price_ = st.radio("가격대를 입력해주세요", ["5000원 미만", "5000원 ~ 8000원미만", "8000원 ~ 11000원미만", "11000원 ~ 14000원 미만", "14000원 이상"])
st.text("음식은 어떠셨나요?")
taste_ = st.feedback(key="taste", options="stars")
st.text("식당 위치는 어떠셨나요? (거리, 횡단보도 건넌 횟수, 엘레베이터 여부)")
accessibility_ = st.feedback(key="accessibility",options="stars")

if st.button("Add Menu Item"):
    try:
        # 새로운 메뉴 항목 추가
        query = f"""
        INSERT INTO {table_name} (menu, price) VALUES ('{menu_item}', {menu_price});
        """
        db.execute_query(db_name, query)
        st.success(f"'{menu_item}' has been added to the menu.")
    except Exception as e:
        st.error(f"Error adding menu item: {e}")
