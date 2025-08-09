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

-- ตรวจสอบสิทธิ์ user
SELECT grantee, privilege_type
FROM information_schema.role_table_grants
WHERE table_catalog = 'research_db';

-- หรือเช็คสิทธิ์การเชื่อมต่อ
SELECT rolname, rolcanlogin FROM pg_roles;

GRANT CONNECT ON DATABASE research_db TO "AreedaTJ";

SELECT rolname, rolcanlogin FROM pg_roles WHERE rolname = 'AreedaTJ';

ALTER ROLE "AreedaTJ" WITH LOGIN;

SELECT rolname, rolcanlogin FROM pg_roles WHERE rolname = 'AreedaTJ';

GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE articles TO "AreedaTJ";

GRANT USAGE, SELECT ON SEQUENCE articles_article_id_seq TO "AreedaTJ";

-- คำสั่งรวม
-- GRANT CONNECT ON DATABASE research_db TO "AreedaTJ";
-- GRANT USAGE ON SCHEMA public TO "AreedaTJ";
-- GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE articles TO "AreedaTJ";
-- GRANT USAGE, SELECT ON SEQUENCE articles_article_id_seq TO "AreedaTJ";
