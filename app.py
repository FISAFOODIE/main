import streamlit as st

query_app = st.Page("query_app.py", title="Query Your Data")
create_table_app = st.Page("create_table_app.py", title="Create Table with CSV file")

pg = st.navigation([query_app, create_table_app])

pg.run()