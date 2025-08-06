-- สร้างตารางสำหรับแหล่งที่มาของบทความ (Scopus, TCI, WOS)
CREATE TABLE IF NOT EXISTS sources (
    source_id SERIAL PRIMARY KEY,
    source_name VARCHAR(50) UNIQUE NOT NULL
);

-- สร้างตารางสำหรับข้อมูลบทความ
CREATE TABLE IF NOT EXISTS articles (
    article_id SERIAL PRIMARY KEY,
    article_name TEXT NOT NULL,
    author TEXT NOT NULL,
    output_year INTEGER NOT NULL,
    journal TEXT NOT NULL,
    volume TEXT,
    issue TEXT,
    page_range TEXT,
    doc_type TEXT,
    source_id INTEGER REFERENCES sources(source_id)
);
