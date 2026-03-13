import streamlit as st

st.set_page_config(page_title="DATAFLUX", layout="centered")

# Title
st.markdown("<h1 style='text-align:center;'>DATAFLUX</h1>", unsafe_allow_html=True)

# Subtitle
st.markdown("<h3 style='text-align:center;'>Extract Insights From Data</h3>", unsafe_allow_html=True)

st.write("")

# Buttons
col1, col2 = st.columns(2)

with col1:
    voice = st.button("🎤 Voice to SQL")

with col2:
    upload = st.button("📂 Upload Dataset")
    
# Voice to SQL section
if voice:
    st.subheader("🎤 Voice to SQL")

    query = st.text_area("Editable Query Box")

    if st.button("Generate SQL"):
        st.code("SELECT * FROM dataset LIMIT 10;")

    st.subheader("Query Tools")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.button("Explanation")

    with col2:
        st.button("Optimization")

    with col3:
        st.button("Sub Representation")
        
        # Upload Dataset section
if upload:
    st.subheader("📂 Upload Dataset")

    file = st.file_uploader("Upload CSV File", type=["csv"])

    if file is not None:
        import pandas as pd

        df = pd.read_csv(file)

        st.success("Dataset uploaded successfully")

        st.dataframe(df.head())