import requests
from bs4 import BeautifulSoup
import csv

SEARCH_URL = "https://search.tci-thailand.org/advance_search.html"
RESULT_URL = "https://search.tci-thailand.org/result_search.html"

def search_tci_by_institution(institution, max_pages=1):
    results = []
    for page in range(1, max_pages + 1):
        payload = {
            'search_type': 'advance',
            'inst': institution,
            'page': page
        }
        response = requests.post(RESULT_URL, data=payload)
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('div', class_='article-list')
        for article in articles:
            title = article.find('a', class_='article-title').text.strip() if article.find('a', class_='article-title') else ''
            authors = article.find('div', class_='article-author').text.strip() if article.find('div', class_='article-author') else ''
            journal = article.find('div', class_='article-journal').text.strip() if article.find('div', class_='article-journal') else ''
            year = article.find('div', class_='article-year').text.strip() if article.find('div', class_='article-year') else ''
            results.append({
                'title': title,
                'authors': authors,
                'journal': journal,
                'year': year
            })
    return results

if __name__ == "__main__":
    institution = "มหาวิทยาลัยสงขลานครินทร์"
    data = search_tci_by_institution(institution, max_pages=2)  # ปรับจำนวนหน้าได้ตามต้องการ

    # เขียนผลลัพธ์ลงไฟล์ CSV
    with open('tci_results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'authors', 'journal', 'year']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            writer.writerow(item)

    print("บันทึกข้อมูลลงไฟล์ tci_results.csv แล้ว")