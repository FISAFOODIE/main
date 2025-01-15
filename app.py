import streamlit as st
# open_csv = st.Page("open_csv.py", title="Open Your csv file")
add_menu = st.Page("add_menu.py", title="점심 메뉴 등록")
dashboard = st.Page("dashboard.py", title="통계 대시보드")
pg = st.navigation([add_menu, dashboard])
pg.run()