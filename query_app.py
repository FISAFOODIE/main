import streamlit as st
import pandas as pd

import db_util as db


st.title("Query Your Data")
################

st.subheader("Database and Tables")

# show tables
db_name = st.selectbox(label="Select a database", options=db.get_database_names())
tbl_names = db.get_table_names(db_name)
df_tbl = pd.DataFrame(tbl_names, columns=["Table Name"])
st.write("", df_tbl)

################
st.divider()
################

st.subheader("Query and Result")

# query editor
default_table_name = tbl_names[0]
query = st.text_area(
    label="Enter your SQL query here",
    value=f"SELECT * FROM {default_table_name} LIMIT 10;",
)


# run query and show result
def run_query(db_name, query):
    result = db.execute_query(db_name, query)
    return pd.DataFrame(result)


run_button = st.button("Run query")
st.text("Query result:")
if run_button:
    df_result = run_query(db_name, query)
    st.write(df_result)
    st.download_button(
        label="Download CSV",
        data=df_result.to_csv(index=False),
        file_name="query_result.csv",
        mime="text/csv",
    )