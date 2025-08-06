import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

RESULT_URL = "https://search.tci-thailand.org/php/search/advance_search.php"
DETAIL_URL = "https://search.tci-thailand.org/php/search/author_info.php"

def fetch_psu_papers(max_page=5, page_size=10):
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://search.tci-thailand.org/advance_search.html'
    }
    session = requests.Session()
    papers = []

    for cur_page in range(1, max_page+1):
        payload = {
            'keyword[]': 'มหาวิทยาลัยสงขลานครินทร์',
            'criteria[]': 'title',
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

        article_ids = data.get('article_ids', [])
        for aid in article_ids:
            detail_params = {'article_id': aid}
            detail_resp = session.get(DETAIL_URL, params=detail_params, headers=headers)
            try:
                author_data = detail_resp.json()
                authors = ', '.join([a.get('name_loc', '') for a in author_data])
            except Exception as e:
                print(f"Error parsing author info for article {aid}: {e}")
                authors = ''
            # title, year, journal ยังต้องดึงจาก endpoint อื่น (หรือจาก response แรกถ้ามี)
            papers.append({
                'title': '',      # ต้องเติม logic ดึง title
                'authors': authors,
                'year': '',       # ต้องเติม logic ดึง year
                'journal': ''     # ต้องเติม logic ดึง journal
            })
            time.sleep(0.5)

    return papers

if __name__ == "__main__":
    papers = fetch_psu_papers(max_page=5, page_size=10)  # ดึง 5 หน้า หน้า 10 รายการ
    df = pd.DataFrame(papers)
    df.to_csv('psu_papers.csv', index=False, encoding='utf-8-sig')
    print(f"ดึงข้อมูลสำเร็จ {len(df)} รายการ")