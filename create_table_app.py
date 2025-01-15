import logging

import streamlit as st
import pandas as pd

import db_util as db

# APP_ROOT = "apps/sqlite_streamlit"

logging.basicConfig(
    filename=f"logs/create_table_app.log",
    format="%(asctime)s - [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

################
st.title("Create Table with CSV file")
################

st.subheader("Upload CSV file")
uploaded_file = st.file_uploader(label="Select a file", type=["csv"])
# st.write("CSV file preview:")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df.head(10))

################
st.divider()
################

st.subheader("Create Table")
db_name = st.text_input(label="Enter the target database")
tbl_name = st.text_input(label="Enter a table name")

if st.button("Create table"):
    logger.info(
        f"Creating table {db_name}.{tbl_name} with data from {uploaded_file.name}"
    )
    logger.info(f"Uploaded file head: {df.head(3)}")

    # save temp csv file
    tmp_file_path = f"data/tmp_{db_name}.{tbl_name}.csv"
    logger.info(f"Temp file path: {tmp_file_path}")
    df.to_csv(tmp_file_path, index=False)

    # create table
    db.create_table_with_csv(tmp_file_path, db_name, tbl_name)
    st.success(
        f"Table {db_name}.{tbl_name} created with data from {uploaded_file.name}"
    )