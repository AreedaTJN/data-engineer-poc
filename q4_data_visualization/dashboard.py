import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
from sqlalchemy import create_engine

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
selected_years = st.sidebar.multiselect("Select publication years", years, default=[])
selected_sources = st.sidebar.multiselect("Select sources", sources, default=[])

# ==== MAIN QUERY ====
@st.cache_data
def load_data(years, sources):
    query = """
        SELECT a.article_name, a.author, a.output_year, a.journal, s.source_name
        FROM articles a
        JOIN sources s ON a.source_id = s.source_id
    """
    params = []
    conditions = []

    if years:
        placeholders_year = ','.join(['%s'] * len(years))
        conditions.append(f"a.output_year IN ({placeholders_year})")
        params.extend(years)

    if sources:
        placeholders_source = ','.join(['%s'] * len(sources))
        conditions.append(f"s.source_name IN ({placeholders_source})")
        params.extend(sources)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY a.output_year DESC"

    conn = get_psycopg2_conn()
    try:
        df = pd.read_sql(query, conn, params=params)
    finally:
        conn.close()
    return df

df = load_data(selected_years, selected_sources)

# ==== HEADER ====
st.title("PSU Research Dashboard")
st.markdown("Dashboard showing research publications from PostgreSQL database")

# ==== SECTION 1: Yearly trend chart (Bar Chart) ====
st.subheader("Yearly Research Publication Trend")

yearly = df.groupby('output_year').size().reset_index(name='count')
yearly['output_year'] = yearly['output_year'].astype(int).astype(str)  # Convert to string for clean x-axis
yearly = yearly.sort_values('output_year', ascending=False)

fig = px.bar(
    yearly,
    x='output_year',
    y='count',
    title="Number of Publications per Year",
    labels={"output_year": "Publication Year", "count": "Number of Publications"},
    template="plotly_white",
    text='count'
)

# เพิ่มขนาด font text บนบาร์
fig.update_traces(
    marker_color='#1f77b4',
    textposition='outside',
    textfont_size=14  # เพิ่มขนาด font ของตัวเลขบนบาร์
)

# layout
fig.update_layout(
    title_font=dict(size=20, family='Arial', color='white'),
    xaxis=dict(tickangle=0, color='white'),
    yaxis=dict(
        showgrid=True,
        zeroline=False,
        color='white',
        range=[0, yearly['count'].max() * 1.3]  # ขยายสูงสุดแกน y 30% จาก max count
    ),
    hovermode="x unified",
    plot_bgcolor='#111111',
    paper_bgcolor='#111111',
    margin=dict(l=0, r=0, t=100, b=0)  # ขยาย margin top เพิ่มพื้นที่ให้ title และ text บนบาร์
)

st.plotly_chart(fig, use_container_width=True)

# ==== SECTION 2: Top authors ====
st.subheader("Top authors by number of publications")

authors = df['author'].dropna().str.split(';').explode().str.strip()
top_authors = authors.value_counts().reset_index()
top_authors.columns = ['author', 'num_articles']

st.dataframe(top_authors.head(10), use_container_width=True)

# ==== SECTION 3: All publications ====
st.subheader("List of research publications")
st.dataframe(df, use_container_width=True)
