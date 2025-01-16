import streamlit as st
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


# MySQL 연결 설정
def connect_db():
    return pymysql.connect(
        host=host,
        user=user,
        password=password,
        port=port,
        database=database_name
    )


# 한 페이지당 출력할 데이터 수
PAGE_SIZE = 10

st.set_page_config(
    page_title="FISAFOODIE",
    page_icon="🧊"
)

# 제목
st.title(":knife_fork_plate: :rainbow[점메츄] - 메뉴 관리:knife_fork_plate:")
st.divider()

# 데이터베이스 설정
table_name = "restaurant_reviews"  # 실제 테이블 이름으로 변경


# 데이터베이스에서 정보 조회 (LIMIT 및 OFFSET을 이용하여 페이지마다 다른 데이터 로드)
def fetch_db_data(offset=0, limit=PAGE_SIZE):
    try:
        connection = connect_db()
        cursor = connection.cursor()

        # 쿼리 작성 (LIMIT과 OFFSET을 사용하여 페이지네이션 처리)
        select_query = f"SELECT * FROM {table_name} LIMIT %s OFFSET %s"
        cursor.execute(select_query, (limit, offset))
        rows = cursor.fetchall()

        return rows
    except Exception as e:
        st.error(f"오류 발생: {e}")
        return []
    finally:
        connection.close()


# 데이터베이스에서 총 데이터 개수 조회 (전체 페이지 수 계산을 위한 용도)
def fetch_total_data_count():
    try:
        connection = connect_db()
        cursor = connection.cursor()

        # 총 데이터 개수 조회
        count_query = f"SELECT COUNT(*) FROM {table_name}"
        cursor.execute(count_query)
        total_count = cursor.fetchone()[0]

        return total_count
    except Exception as e:
        st.error(f"오류 발생: {e}")
        return 0
    finally:
        connection.close()


# 총 데이터 개수
total_count = fetch_total_data_count()

# 전체 페이지 수 계산
total_pages = (total_count // PAGE_SIZE) + (1 if total_count % PAGE_SIZE > 0 else 0)

# 페이지 탭 생성 (페이지 번호에 해당하는 탭 생성)
tabs = [f"{i + 1}" for i in range(total_pages)]

# 탭을 사용하여 페이지 선택
tab_selections = st.tabs(tabs)

# 각 탭에 해당하는 데이터 불러오기
for tab_index, tab in enumerate(tab_selections):
    with tab:
        # 현재 탭에 해당하는 페이지 번호 계산
        offset = tab_index * PAGE_SIZE
        rows = fetch_db_data(offset)

        # DB에서 정보를 가져와서 출력
        if rows:
            for i, row in enumerate(rows):
                # 텍스트와 이미지를 나란히 배치하기 위해 st.columns 사용
                col1, col2 = st.columns([3, 1])  # 첫 번째 열은 텍스트, 두 번째 열은 이미지

                with col1:  # 텍스트 출력
                    st.write(f"트랙: {row[2]}")
                    st.write(f"식당 이름: {row[3]}")
                    st.write(f"메뉴: {row[4]}")
                    st.write(f"가격대: {row[6]}")
                    st.write(f"맛 평점: {row[7]}")
                    st.write(f"접근성 평점: {row[8]}")
                    st.write(f"식사 날짜: {row[9].strftime('%Y년%m월%d일')}")

                with col2:  # 이미지 출력
                    if row[5]:  # 이미지가 바이너리 데이터로 저장되어 있는 경우
                        try:
                            st.image(row[5], width=300)  # 이미지 크기 고정 (width 150px)
                        except Exception as e:
                            st.error(f"이미지 표시 오류: {e}")

                st.divider()
        else:
            st.warning("현재 데이터베이스에 저장된 메뉴 정보가 없습니다.")
