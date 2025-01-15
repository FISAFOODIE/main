import streamlit as st
# open_csv = st.Page("open_csv.py", title="Open Your csv file")
add_menu = st.Page("add_menu.py", title="Query Your Data")
create_table_app = st.Page("create_table_app.py", title="Create Table with CSV file")
pg = st.navigation([add_menu, create_table_app])
pg.run()

