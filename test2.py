import requests
import pandas as pd
import time

# URLs
RESULT_URL = "https://search.tci-thailand.org/php/search/advance_search.php"
DETAIL_URL = "https://search.tci-thailand.org/php/search/author_info.php"

def fetch_psu_articles(max_page=5, page_size=10, output_file="psu_articles.csv"):
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://search.tci-thailand.org/advance_search.html'
    }
    session = requests.Session()
    all_articles = []

    for cur_page in range(1, max_page + 1):
        payload = {
            'keyword[]': 'มหาวิทยาลัยสงขลานครินทร์',
            'criteria[]': 'affiliation',  # ✅ สำคัญ! ต้องเป็น affiliation
            'perform_advance_search': 'true',
            'cur_page': cur_page,
            'page_size': page_size,
            'year_filter': [],
            'country_filter': '',
            'get_all_article_id': 'true',
            'year_num': 10
        }

        response = session.post(RESULT_URL, data=payload, headers=headers)
        print(f"Page {cur_page} Status code:", response.status_code)
        if response.status_code != 200:
            print("Error:", response.text[:200])
            continue

        try:
            data = response.json()
        except Exception as e:
            print("JSON decode error:", e)
            continue

        records = data.get("records", [])
        article_ids = data.get("article_ids", [])

        for i, record in enumerate(records):
            article_id = article_ids[i]
            # ดึง author เพิ่มเติมจาก author_info.php
            try:
                detail_resp = session.get(DETAIL_URL, params={'article_id': article_id}, headers=headers)
                author_data = detail_resp.json()
                authors = ', '.join([a.get('name_loc', '') for a in author_data])
            except Exception as e:
                print(f"Error parsing author info for article {article_id}: {e}")
                authors = ""

            all_articles.append({
                'title': record.get('article_title_loc', ''),
                'journal': record.get('journal_title_loc', ''),
                'year': record.get('article_year', ''),
                'authors': authors
            })

            time.sleep(0.5)

    # บันทึกไฟล์
    df = pd.DataFrame(all_articles)
    df.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"\n✅ ดึงข้อมูลสำเร็จ {len(df)} รายการ บันทึกไว้ใน {output_file}")

if __name__ == "__main__":
    fetch_psu_articles(max_page=5, page_size=10)
