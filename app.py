import streamlit as st
# open_csv = st.Page("open_csv.py", title="Open Your csv file")
add_menu = st.Page("add_menu.py", title="점심 메뉴 등록")
dashboard = st.Page("dashboard.py", title="우리 파헤쳐보기")
pg = st.navigation([add_menu, dashboard])
pg.run()