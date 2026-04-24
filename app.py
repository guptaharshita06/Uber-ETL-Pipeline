import streamlit as st
import pandas as pd
from src.sql_analysis import run_sql_queries
from src.cleaning import clean_data
from src.utils import get_basic_info

st.set_page_config(page_title="Data Cleaning App", layout="wide")

st.title("📊 Data Cleaning & Analysis App")

# ================= SIDEBAR =================
st.sidebar.header("⚙️ Cleaning Options")

remove_duplicates = st.sidebar.checkbox("Remove Duplicates", True)
handle_missing = st.sidebar.checkbox("Handle Missing Values", True)

fill_method = st.sidebar.selectbox(
    "Missing Value Strategy",
    ["mean", "median", "zero", "drop"]
)

# ================= SESSION STATE =================
if "cleaned_df" not in st.session_state:
    st.session_state.cleaned_df = None

if "total" not in st.session_state:
    st.session_state.total = None

if "avg_values" not in st.session_state:
    st.session_state.avg_values = None

# ================= FILE UPLOAD =================
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("📊 Raw Data Info")
    st.write(get_basic_info(df))

    st.subheader("🔍 Missing Values (Raw Data)")
    st.write(df.isnull().sum())

    st.subheader("📄 Raw Data Preview")
    st.dataframe(df.head())

    # ================= CLEAN BUTTON =================
    if st.button("Clean Data"):
        with st.spinner("Cleaning data..."):

            cleaned_df = clean_data(
                df,
                remove_duplicates,
                handle_missing,
                fill_method
            )

            st.session_state.cleaned_df = cleaned_df

            # ================= SQL =================
            total, avg_values = run_sql_queries(cleaned_df)

            st.session_state.total = total
            st.session_state.avg_values = avg_values

            st.success("✅ Data cleaned successfully!")

# ================= SHOW RESULT =================
if st.session_state.cleaned_df is not None:

    cleaned_df = st.session_state.cleaned_df

    st.subheader("✅ Cleaned Data Output")
    st.write("Shape:", cleaned_df.shape)

    if cleaned_df.empty:
        st.error("❌ Cleaned data is empty!")
    else:
        st.dataframe(cleaned_df.head())

        # ================= VISUALIZATION =================
        st.subheader("📊 Data Visualization")

        numeric_cols = cleaned_df.select_dtypes(include='number').columns

        if len(numeric_cols) > 0:
            selected_col = st.selectbox("Select column for graph", numeric_cols)

            chart_type = st.radio("Select chart type", ["Line", "Bar"])

            if chart_type == "Line":
                st.line_chart(cleaned_df[selected_col])
            else:
                st.bar_chart(cleaned_df[selected_col])
        else:
            st.warning("⚠️ No numeric columns found for visualization")

        # ================= SQL ANALYSIS =================
        st.subheader("📊 SQL Analysis Results")

        st.write("Total Rows:", st.session_state.total)

        st.write("Average Values (Numeric Columns):")
        st.write(st.session_state.avg_values)

        # ================= DOWNLOAD =================
        file_name = "cleaned_data.csv"
        csv = cleaned_df.to_csv(index=False).encode('utf-8')

        st.download_button(
            label="📥 Download Cleaned CSV",
            data=csv,
            file_name=file_name,
            mime="text/csv"
        )