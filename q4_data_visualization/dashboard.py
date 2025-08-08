import streamlit as st
import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
import matplotlib.pyplot as plt

# ==== DATABASE CONNECTION ====
DB_USER = 'AreedaTJ'
DB_PASS = 'AreedaTJ'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'research_db'

engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

def get_psycopg2_conn():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )

# ==== LOAD FILTER OPTIONS ====
@st.cache_data
def load_filter_data():
    conn = get_psycopg2_conn()
    try:
        years_df = pd.read_sql("SELECT DISTINCT output_year FROM articles ORDER BY output_year DESC", conn)
        sources_df = pd.read_sql("SELECT DISTINCT source_name FROM sources ORDER BY source_name", conn)
    finally:
        conn.close()
    return years_df['output_year'].tolist(), sources_df['source_name'].tolist()

years, sources = load_filter_data()

# ==== SIDEBAR FILTER ====
st.sidebar.header("🔍 Filters")
selected_years = st.sidebar.multiselect("เลือกปีที่ตีพิมพ์", years, default=years)
selected_sources = st.sidebar.multiselect("เลือกแหล่งข้อมูล", sources, default=sources)

# ==== MAIN QUERY ====
@st.cache_data
def load_data(years, sources):
    placeholders_year = ','.join(['%s'] * len(years))
    placeholders_source = ','.join(['%s'] * len(sources))
    query = f"""
        SELECT a.article_name, a.author, a.output_year, a.journal, s.source_name
        FROM articles a
        JOIN sources s ON a.source_id = s.source_id
        WHERE a.output_year IN ({placeholders_year})
        AND s.source_name IN ({placeholders_source})
    """
    params = years + sources
    conn = get_psycopg2_conn()
    try:
        df = pd.read_sql(query, conn, params=params)
    finally:
        conn.close()
    return df

df = load_data(selected_years, selected_sources)

# ==== HEADER ====
st.title("PSU Research Dashboard")
st.markdown("แดชบอร์ดแสดงข้อมูลผลงานวิจัยจากฐานข้อมูล PostgreSQL")

# ==== SECTION 1: กราฟแนวโน้มรายปี ====
st.subheader("แนวโน้มผลงานวิจัยรายปี")

yearly = df.groupby('output_year').size().reset_index(name='count')
fig, ax = plt.subplots()
ax.plot(yearly['output_year'], yearly['count'], marker='o')
ax.set_xlabel("ปีที่ตีพิมพ์")
ax.set_ylabel("จำนวนผลงาน")
ax.set_title("จำนวนผลงานวิจัยรายปี")
st.pyplot(fig)

# ==== SECTION 2: ตารางผู้แต่งผลงานสูงสุด ====
st.subheader("ผู้แต่งที่มีผลงานมากที่สุด")

authors = df['author'].dropna().str.split(';').explode().str.strip()
top_authors = authors.value_counts().reset_index()
top_authors.columns = ['author', 'num_articles']

st.dataframe(top_authors.head(10), use_container_width=True)

# ==== SECTION 3: ตารางผลงานทั้งหมด ====
st.subheader("รายการผลงานวิจัย")
st.dataframe(df, use_container_width=True)