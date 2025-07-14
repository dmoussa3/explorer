import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
st.set_page_config(page_title="Data Analysis", layout="wide")
st.title("Data Analysis Dashboard 📊")

#0 Analysis Type Selection
st.header("Select Analysis Type 🗂️")
analysis_type = st.radio("Select the type of analysis", ("CSV File", "Excel File"))

#1 File Upload
if analysis_type == "CSV File":
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
elif analysis_type == "Excel File":
    uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.header("Data Preview 🔍")
    st.dataframe(df)

    #2 Show basic statistics
    if st.checkbox("Show Statistics summary"):
        st.write("Summary 📈")
        st.write(df.describe())

    #3 Filtering
    st.header("Filter Options ⚙️")

    filtered_col = st.selectbox("Select column(s) to filter", df.columns)
    if df[filtered_col].dtype == 'object':
        unique_val = df[filtered_col].unique()
        selected_val = st.selectbox("Select value to filter", unique_val)
        filtered_df = df[df[filtered_col] == selected_val]
    else:
        min, max = float(df[filtered_col].min()), float(df[filtered_col].max())
        range = st.slider("Select range", min_value=min, max_value=max, value=(min, max))
        filtered_df = df[df[filtered_col].between(*range)]

    st.write("Filtered Data 📊")
    st.write(f"Filtered rows: {len(filtered_df)}")
    st.dataframe(filtered_df)

    #4 Plotting
    st.subheader("Plot Columns 📊")

    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    if numeric_cols:
        col_to_plot = st.selectbox("Select a numeric column to plot", numeric_cols)
        fig, ax = plt.subplots()
        filtered_df[col_to_plot].hist(bins=30, ax=ax)
        st.pyplot(fig)
    else:
        st.warning("No numeric columns to plot.")

    #5 Download filtered data
    st.header("Download Filtered Data 📥")
    download_option = st.radio("Select download format", ("CSV", "Excel"))
    if download_option == "CSV":
        st.download_button("Download Filtered Data into CSV", filtered_df.to_csv(index=False), "filtered.csv", "text/csv")
    elif download_option == "Excel":
        # Convert DataFrame to Excel
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            filtered_df.to_excel(writer, index=False, sheet_name='Filtered Data')
        excel_buffer.seek(0)

        st.download_button("Download Filtered Data into Excel", excel_buffer, "filtered.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.info("Please upload a file to begin.")