import streamlit as st
import pymysql
import os
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
from datetime import datetime, timedelta

# .env 파일 로드
load_dotenv()

# MySQL 연결 정보 로드
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

st.set_page_config(page_title="FISAFOODIE", page_icon=":각얼음:")

# 페이지 제목
st.title("대시보드 (미완성)")
st.divider()

# MySQL 연결 및 데이터 로드
def load_data():
    connection = connect_db()
    query = "SELECT * FROM restaurant_reviews;"
    df = pd.read_sql(query, connection)
    connection.close()
    return df


df = load_data()

# 가격대 문자열을 평균값으로 변환하는 함수
def get_avg_price_from_range(price_range_str):
    price_map = {
        '0~5,000 이하': 5000,
        '5,000원 초과 8,000원 이하': 6500,
        '8,000원 초과 10,000원 이하': 9000,
        '10,000원 초과 15,000원 이하': 12500,
        '15,000원 초과': 15000
    }
    return price_map.get(price_range_str, None)

df['cost'] = df['cost'].apply(get_avg_price_from_range)

# 그래프 제목 추가
def add_title(fig, title):
    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            xanchor='center',
            font=dict(size=20)
        )
    )

# 가게 Rank 그래프
def plot_taste_rank(df):
    df_taste_rank = df.groupby('restaurant_name')['flavor'].mean().sort_values(ascending=False).reset_index()[:10]
    df_taste_rank['restaurant_name_줄바꿈'] = df_taste_rank['restaurant_name'].apply(lambda name: "<br>".join(name.split(" ")))

    fig = px.bar(df_taste_rank, x='restaurant_name_줄바꿈', y='flavor', labels={'restaurant_name_줄바꿈': '가게', 'flavor': '맛점수'})
    add_title(fig, "Top 10! 맛있는 집 rank 👑")
    return fig

# 금주의 가게 Rank 그래프
def plot_this_week_rank(df):
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())  # 이번 주 월요일
    end_of_week = start_of_week + timedelta(days=6)  # 이번 주 일요일

    start_of_week_str = start_of_week.strftime('%m월 %d일')
    end_of_week_str = end_of_week.strftime('%m월 %d일')

    df['date'] = pd.to_datetime(df['date'])
    this_week_df = df[(df['date'] >= start_of_week) & (df['date'] <= end_of_week)]
    this_week_df = this_week_df.groupby('restaurant_name')['flavor'].mean().sort_values(ascending=False).reset_index()[:3]
    this_week_df['rank'] = range(1, len(this_week_df) + 1)
    this_week_df['restaurant_name_줄바꿈'] = this_week_df['restaurant_name'].apply(lambda name: "<br>".join(name.split(" ")))

    fig = px.bar(this_week_df, x='restaurant_name_줄바꿈', y='flavor', labels={'restaurant_name_줄바꿈': '가게', 'flavor': '맛점수'})
    fig.update_xaxes(tickangle=0)
    fig.update_yaxes(tickangle=0)
    add_title(fig, f"이번주 rank Top3 👑<br>({start_of_week_str} ~ {end_of_week_str})")
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

    fig = px.bar(menu_avg, x='menu', y='flavor', hover_data={'class' : False, 'flavor': False, 'cost': True}, labels={'menu': '메뉴명', 'flavor': '맛점수', 'cost': '가격대'}, title=f"{selected_restaurant} 메뉴별 평균 맛점수", color='class', barmode="group")
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
                value=f"{selected_df['flavor'].mean():.1f}",
                delta=f"{selected_df['flavor'].mean() - df['flavor'].mean():.1f}"
                )   

    # 메트릭2: 평균 가격대
    met2.metric(label="평균가격대",
                value=f"{selected_df['cost'].mean():.0f}원",
                delta=f"{selected_df['cost'].mean() - df['cost'].mean():.1f}원")

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
col1, col2 = st.columns([2, 2])

with col1:
    st.plotly_chart(plot_taste_rank(df), use_container_width=True)

with col2:
    st.plotly_chart(plot_this_week_rank(df), use_container_width=True)

# 가게명 선택 및 관련 통계 출력
rest = st.selectbox('보고싶은 가게명을 선택하세요', df['restaurant_name'].unique())
display_metrics(df, rest)
st.plotly_chart(plot_cumulative_avg(df, rest), use_container_width=True)
st.plotly_chart(plot_menu_avg(df, rest), use_container_width=True)

# track별 파이 차트 출력
plot_track_favorites(df)