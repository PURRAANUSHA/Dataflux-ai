from transformers import pipeline
import speech_recognition as sr
import streamlit as st
import pandas as pd

from backend.sql_generator import generate_sql
from backend.query_tools import explain_query
def generate_sql_query(user_query):

    if "top" in user_query.lower():
        return "SELECT * FROM dataset ORDER BY value DESC LIMIT 5;"

    elif "average" in user_query.lower():
        return "SELECT AVG(value) FROM dataset;"

    elif "count" in user_query.lower():
        return "SELECT COUNT(*) FROM dataset;"

    else:
        return "SELECT * FROM dataset;"
def generate_sql_query(user_query):

    if "top" in user_query.lower():
        return "SELECT * FROM dataset ORDER BY value DESC LIMIT 5;"

    elif "average" in user_query.lower():
        return "SELECT AVG(value) FROM dataset;"

    elif "count" in user_query.lower():
        return "SELECT COUNT(*) FROM dataset;"

    else:
        return "SELECT * FROM dataset;"
def voice_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak now")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        return text
    except:
        return "Could not understand audio"

# Page configuration
st.set_page_config(page_title="DATAFLUX", layout="centered")

# Initialize page state
if "page" not in st.session_state:
    st.session_state.page = "home"


# ---------------- HOME PAGE ----------------

if st.session_state.page == "home":

    st.title("DATAFLUX")
    st.subheader("Extract Insights From Data")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎤 Voice to SQL"):
            st.session_state.page = "voice"

    with col2:
        if st.button("📂 Upload Dataset"):
            st.session_state.page = "upload"


# ---------------- VOICE TO SQL PAGE ----------------

if st.session_state.page == "voice":

    st.title("🎤 Voice to SQL")

    st.write("Speak or type your query")

    if st.button("Start Voice Input 🎤"):
        spoken_text = voice_to_text()
        st.session_state.query = spoken_text

    query = st.text_area(
        "Editable Query Box",
        value=st.session_state.get("query", "")
    )

    if st.button("Generate SQL"):

        sql_query = "SELECT * FROM dataset LIMIT 10;"

        st.code(sql_query, language="sql")

        st.subheader("Query Tools")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Explanation"):
                st.write("This query retrieves the first rows from the dataset.")

        with col2:
            if st.button("Optimization"):
                st.write("Indexes and filters can improve performance.")

        with col3:
            if st.button("Sub Representation"):
                st.write("Step1: Select data → Step2: Limit results")

    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"

# ---------------- UPLOAD DATASET PAGE ----------------

if st.session_state.page == "upload":

    st.title("📂 Upload Dataset")

    file = st.file_uploader("Upload Dataset", type=["csv","xls","xlsx"])

    if file is not None:

        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        st.success("Dataset uploaded successfully")

        # Dataset preview
        st.subheader("Dataset Preview")
        st.dataframe(df.head())

        # -----------------------------
        # Data Preprocessing
        # -----------------------------
        st.subheader("🧹 Automatic Data Preprocessing")

        duplicates = df.duplicated().sum()
        missing = df.isnull().sum().sum()

        df = df.drop_duplicates()
        df = df.fillna(df.mean(numeric_only=True))

        st.write("Duplicates removed:", duplicates)
        st.write("Missing values handled:", missing)

        # -----------------------------
        # Data Quality Report
        # -----------------------------
        st.subheader("📊 Data Quality Report")

        col1, col2, col3 = st.columns(3)

        col1.metric("Rows", df.shape[0])
        col2.metric("Columns", df.shape[1])
        col3.metric("Missing Values", missing)

        # -----------------------------
        # Outlier Detection
        # -----------------------------
        st.subheader("⚠️ Outlier Detection")

        numeric_df = df.select_dtypes("number")

        if not numeric_df.empty:

            Q1 = numeric_df.quantile(0.25)
            Q3 = numeric_df.quantile(0.75)

            IQR = Q3 - Q1

            outliers = ((numeric_df < (Q1 - 1.5 * IQR)) |
                        (numeric_df > (Q3 + 1.5 * IQR))).sum()

            st.write("Outliers detected per column:")
            st.write(outliers)

        # -----------------------------
        # Visualization
        # -----------------------------
        st.subheader("📊 Visualization")

        chart = st.selectbox(
            "Select Chart Type",
            ["Bar Chart","Line Chart","Area Chart"]
        )

        if chart == "Bar Chart":
            st.bar_chart(numeric_df)

        if chart == "Line Chart":
            st.line_chart(numeric_df)

        if chart == "Area Chart":
            st.area_chart(numeric_df)

        # -----------------------------
        # AI Insights
        # -----------------------------
        st.subheader("🤖 AI Insights")

        if not numeric_df.empty:

            st.write("Highest values:")
            st.write(numeric_df.max())

            st.write("Average values:")
            st.write(numeric_df.mean())

            st.write("Minimum values:")
            st.write(numeric_df.min())

    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"