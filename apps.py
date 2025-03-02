import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="File Convert", layout="wide")
st.title("File Convert & Cleaner")
st.write("Upload CSV or Excel files, clean data, and convert formats.")

files = st.file_uploader("Upload CSV or Excel Files.", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split(".")[-1]
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)

        st.subheader(f"{file.name} - Preview")
        st.dataframe(df.head())

        if st.checkbox(f"Remove Duplicates - {file.name}"):
            df = df.drop_duplicates()
            st.success("Removed Duplicates")
            st.dataframe(df.head())

        if st.checkbox(f"Fill Missing Values - {file.name}"):
            df.fillna(df.select_dtypes(include=["number"]).mean(), inplace=True)
            st.success("Missing Values Filled With Mean")
            st.dataframe(df.head())

        selected_columns = st.multiselect(f"Select Columns - {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]
        st.dataframe(df.head())

        if st.checkbox(f"Show Chart - {file.name}") and not df.select_dtypes(include=["number"]).empty:
            st.bar_chart(df.select_dtypes(include=["number"]).iloc[:, :2])

        format_choise = st.radio(f"Convert {file.name} to:", ["csv", "Excel"], key=file.name)

        # ✅
        output = BytesIO()
        if format_choise == "csv":
            df.to_csv(output, index=False)
            mime = "text/csv"
            new_name = ".".join(file.name.split(".")[:-1]) + ".csv"  
        else:
            df.to_excel(output, index=False, engine='openpyxl')
            mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            new_name = ".".join(file.name.split(".")[:-1]) + ".xlsx"  

        output.seek(0)  
        st.download_button(label=f"Download {new_name}", data=output, file_name=new_name, mime=mime)
        st.success("Processing Complete")
