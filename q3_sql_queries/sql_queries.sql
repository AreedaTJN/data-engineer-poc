-- 1. แสดงจำนวนผลงานวิจัยทั้งหมดในแต่ละปี โดยเรียงจากปีล่าสุดไปหาเก่าสุด
SELECT output_year, COUNT(article_name) AS total_articles
FROM articles
GROUP BY output_year
ORDER BY output_year DESC;

-- 2. ค้นหารายชื่อผู้แต่ง 10 อันดับแรกที่มีจำนวนผลงานตีพิมพ์มากที่สุด
SELECT
TRIM(name) AS author,
COUNT(*) AS total_publications
FROM (
  SELECT unnest(string_to_array(author, ';')) AS name
  FROM articles
  WHERE author IS NOT NULL
) AS authors_expanded
GROUP BY author
ORDER BY total_publications DESC
LIMIT 10;

-- 3. แสดงรายชื่อผลงานวิจัยที่มาจากแหล่งข้อมูล 'scopus' และตีพิมพ์หลังปี 2022
SELECT a.article_name, a.author, a.output_year, a.journal, s.source_name
FROM articles a
JOIN sources s ON a.source_id = s.source_id
WHERE s.source_name ILIKE 'scopus'
AND a.output_year > 2022;

-- 4. ค้นหารายชื่อวารสารที่ตีพิมพ์มากที่สุด 5 อันดับแรก
SELECT journal, COUNT(*) AS article_count
FROM articles
GROUP BY journal
ORDER BY article_count DESC
LIMIT 5;

-- 5. ค้นหารายชื่อผู้แต่งที่เคยมีผลงานตีพิพม์ในวารสารที่มาจากทั้ง 3 ฐานข้อมูล
WITH authors_expanded AS (
  SELECT 
    TRIM(unnest(string_to_array(author, ';'))) AS author_name,
    s.source_name
  FROM articles a
  JOIN sources s ON a.source_id = s.source_id
  WHERE author IS NOT NULL
),
author_source_count AS (
  SELECT 
    author_name,
    source_name,
    COUNT(*) AS num_articles
  FROM authors_expanded
  GROUP BY author_name, source_name
),
pivoted_counts AS (
  SELECT
    author_name,
    COALESCE(SUM(CASE WHEN source_name ILIKE 'scopus' THEN num_articles ELSE 0 END), 0) AS scopus_count,
    COALESCE(SUM(CASE WHEN source_name ILIKE 'wos' THEN num_articles ELSE 0 END), 0) AS wos_count,
    COALESCE(SUM(CASE WHEN source_name ILIKE 'tci' THEN num_articles ELSE 0 END), 0) AS tci_count
  FROM author_source_count
  GROUP BY author_name
),
scored_authors AS (
  SELECT *,
         (scopus_count * 1.5 + wos_count * 1.25 + tci_count * 1.0) AS total_score
  FROM pivoted_counts
)
SELECT *
FROM scored_authors
WHERE scopus_count > 0 AND wos_count > 0 AND tci_count > 0  -- ต้องมีครบ 3 ฐาน
ORDER BY total_score DESC;


GRANT USAGE ON SCHEMA public TO "AreedaTJ";
GRANT SELECT ON ALL TABLES IN SCHEMA public TO "AreedaTJ";
















