import streamlit as st
import pymysql
import os
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
from datetime import datetime, timedelta
import base64
# .env 파일 로드
load_dotenv()
# MySQL 연결 정보 로드
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
    page_icon="🍽"
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


set_bg_hack(r"bg1.png")

# 페이지 제목
st.markdown(
    """
    <style>
        .title {
            text-align: center;
            font-size: 50px;
        }
        .blue {
            color: blue;
        }
    </style>
    <div class='title'>🍚 <span class='blue'>우리</span>만의 정보 🍚</div>
    """, 
    unsafe_allow_html=True
)

st.divider()
# MySQL 연결 및 데이터 로드
def load_data():
    connection = connect_db()
    query = "SELECT * FROM restaurant_reviews;"
    df = pd.read_sql(query, connection)
    connection.close()
    return df

# SQL 테이블을 데이터프레임으로 담기
df = load_data()
# 가격대 문자열을 해당 구간의 최고값으로 변환하는 함수
def get_avg_price_from_range(price_range_str):
    price_map = {
        '5000원 미만': 5000,
        '5000원 ~ 8000원미만': 8000,
        '8000원 ~ 11000원미만': 11000,
        '11000원 ~ 14000원 미만': 14000,
        '14000원 이상': 17000
    }
    return price_map.get(price_range_str, None)

# 'cost'열에 적용해서 자료형 변환'문자열' -> '숫자형'
df['cost'] = df['cost'].apply(get_avg_price_from_range)

# 그래프 제목 추가 함수
def add_title(fig, title):
    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            xanchor='center',
            font=dict(size=20)
        )
    )

# 가게 맛 Rank 그래프
def plot_taste_rank(df):
    # 'restaurant_name'으로 그룹화 -> 'flavor'의 평균 계산 -> 내림차순 정렬 -> 10개만 슬라이싱
    df_taste_rank = df.groupby('restaurant_name')['flavor'].mean().sort_values(ascending=False).reset_index()[:10]
    # 'restaurant_name'에서 공백 기준으로 줄바꿈 -> '상호명 줄바꾸기'
    df_taste_rank['restaurant_name_줄바꿈'] = df_taste_rank['restaurant_name'].apply(lambda name: "<br>".join(name.split(" ")))
    # 순위 컬럼 추가 (문자열로 변환)
    df_taste_rank['rank'] = (df_taste_rank.index + 1).astype(str)
    # 막대그래프 그리기(순위를 색상 기준으로 설정)
    fig = px.bar(df_taste_rank,
                x='restaurant_name_줄바꿈',
                y='flavor',
                color='rank',  # 순위를 기준으로 색상 설정
                color_discrete_sequence=px.colors.qualitative.Set3,
                labels={'restaurant_name_줄바꿈': '가게', 'flavor': '맛점수'})
    # 범례 숨기기
    fig.update_layout(showlegend=False)
    fig.update_yaxes(tickangle=0, range=[0, 5])
    add_title(fig, "Top 10! 맛있는 집 Rank 👑")
    return fig

# 금주의 가게 Rank 그래프
def plot_this_week_rank(df, start_of_week, end_of_week):
    # 'datetime' 자료형으로 변환
    df['date'] = pd.to_datetime(df['date'])
    this_week_df = df[(df['date'] >= start_of_week) & (df['date'] <= end_of_week)]
    this_week_df = this_week_df.groupby('restaurant_name')['flavor'].mean().sort_values(ascending=False).reset_index()[:3]
    this_week_df['rank'] = range(1, len(this_week_df) + 1)
    this_week_df['rank'] = this_week_df['rank'].astype(str)
    this_week_df['restaurant_name_줄바꿈'] = this_week_df['restaurant_name'].apply(lambda name: "<br>".join(name.split(" ")))
    fig = px.bar(this_week_df,
                x='restaurant_name_줄바꿈',
                y='flavor',
                color='rank',  # 순위를 기준으로 색상 설정
                color_discrete_sequence=px.colors.qualitative.Set3,
                labels={'restaurant_name_줄바꿈': '가게', 'flavor': '맛점수'})
    # 범례 숨기기
    fig.update_layout(showlegend=False)
    fig.update_xaxes(tickangle=0)
    fig.update_yaxes(tickangle=0, range=[0, 5])
    add_title(fig, f"해당 주차 Rank Top3 👑")
    return fig

# 선택한 가게의 누적 평균 맛 점수 선 그래프
def plot_cumulative_avg(df, selected_restaurant):
    selected_df = df[df['restaurant_name'] == selected_restaurant]
    selected_df = selected_df.sort_values('date')
    selected_df['누적평균'] = selected_df['flavor'].expanding().mean()
    fig = px.line(selected_df, x='date', y='누적평균', title=f"{selected_restaurant}의 일자별 맛점수 변화", labels={'date': '날짜', '누적평균': '맛점수'})
    fig.update_xaxes(tickformat='%Y-%m-%d', dtick='D1')
    fig.update_yaxes(range=[0, 5])
    fig.update_layout(title=dict(x=0.5, font=dict(size=18)))
    return fig
# 선택한 가게의 메뉴별 평점 막대 그래프
def plot_menu_avg(df, selected_restaurant):
    selected_df = df[df['restaurant_name'] == selected_restaurant]
    menu_avg = selected_df.groupby(['menu', 'class']).agg({'flavor': 'mean', 'cost': 'first'}).reset_index()
    fig = px.bar(menu_avg,
                x='menu',
                y='flavor',
                hover_data={'class' : False, 'flavor': False, 'cost': True},
                labels={'menu': '메뉴명', 'flavor': '맛점수', 'cost': '가격대'},
                title=f"{selected_restaurant} 메뉴별 평균 맛점수",
                color='class',
                barmode="group")
    fig.update_yaxes(range=[0, 5])
    return fig

# 상위 3개 식당을 track별로 파이 차트로 그리기
def plot_track_favorites(df):
    track_restaurant_counts = df.groupby(['class', 'restaurant_name']).size().reset_index(name='count')
    columns = st.columns(3)
    for i, (track, group) in enumerate(track_restaurant_counts.groupby('class')):
        if i >= 3:
            break
        most_visited_restaurants = group.nlargest(5, 'count')
        fig = px.pie(most_visited_restaurants, names='restaurant_name', values='count', hover_data={'count': True}, labels={'restaurant_name': '식당명', 'count': '방문 횟수'}, color_discrete_sequence=px.colors.qualitative.Set3, title=f"{track}반이!<br>좋아하는 식당")
        fig.update_layout(title_font_size=14, legend_font_size=9)
        fig.update_traces(marker=dict(line=dict(color='black', width=1)))
        
        columns[i].plotly_chart(fig, use_container_width=True)

# 메트릭스 표시
def display_metrics(df, selected_restaurant):
    selected_df = df[df['restaurant_name'] == selected_restaurant]
    # 메트릭1: 맛점수
    met1, met2, met3 = st.columns([1, 1, 2])
    met1.metric(label="맛점수",
                value=f"{selected_df['flavor'].mean():.1f}점",
                delta=f"{selected_df['flavor'].mean() - df['flavor'].mean():.1f}점"
                )
    # 메트릭2: 평균 가격대
    met2.metric(label="평균가격대",
                value=f"{selected_df['cost'].mean():,.0f}원",
                delta=f"{selected_df['cost'].mean() - df['cost'].mean():,.0f}원")
    # 메트릭3: 가장 많이 가는 class
    most_frequent_class = selected_df['class'].mode()[0]  # 가장 많이 간 class
    match most_frequent_class:
        case 'ai_엔지니어링':
            most_frequent_class = 'AI_엔지니어링'
        case '클라우드 엔지니어링':
            most_frequent_class = '클라_엔지니어링'
        case '클라우드 서비스':
            most_frequent_class = '클라_서비스'
    met3.metric(label="가게 점령반", value=f'{most_frequent_class}')

# 그래프 출력
col1, col2 = st.columns([2, 2], vertical_alignment="bottom")
with col1:
    # 전체 리뷰 수와 리뷰된 가게 수 계산
    total_reviews = len(df)
    unique_restaurants = df["restaurant_name"].nunique()
    st.header("요약📋")
    # 새로운 데이터프레임 생성
    overview_df = pd.DataFrame(
        {
            "리뷰 수": [total_reviews],
            "가게 수": [unique_restaurants],
        }
    )

    st.markdown(overview_df.to_html(index=False, escape=False), unsafe_allow_html=True)
    st.plotly_chart(plot_taste_rank(df), use_container_width=True)
    

with col2:
    # 날짜 입력 받기
    selected_date = st.date_input("랭킹을 보고 싶은 주차를 선택하세요:", value=pd.Timestamp.today())
    selected_date = pd.Timestamp(selected_date)  # datetime.date -> pd.Timestamp 변환
    # 선택한 날짜를 기준으로 주간 계산
    start_of_week = selected_date - pd.Timedelta(days=selected_date.weekday())
    end_of_week = start_of_week + pd.Timedelta(days=6)
    st.write(f"선택한 기간: {start_of_week.strftime('%Y년 %m월 %d일')} ~ {end_of_week.strftime('%Y년 %m월 %d일')}")
    st.plotly_chart(plot_this_week_rank(df, start_of_week, end_of_week), use_container_width=True)
st.write("")
st.write("")
st.write("")
st.write("")
# 메트릭1: 맛점수
met1_1, met2_1 = st.columns([1, 1])
met1_1.metric(label = ':+1::-1: 전체 가게 맛점수 평균', value = f"{df['flavor'].mean():.1f}점")
met2_1.metric(label = '💸 전체 가게 가격대 평균', value = f"{df['cost'].mean():,.0f}원")
st.write("")
st.write("")
st.write("")
st.write("")

with st.container(border=True):
    # 가게명 선택 및 관련 통계 출력
    rest = st.selectbox('보고싶은 가게명을 선택하세요', df['restaurant_name'].unique())
    display_metrics(df, rest)
    st.plotly_chart(plot_cumulative_avg(df, rest), use_container_width=True)
    st.plotly_chart(plot_menu_avg(df, rest), use_container_width=True)
st.write("")
st.write("")
st.write("")
st.write("")
# track별 파이 차트 출력
plot_track_favorites(df)