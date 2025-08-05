from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def scrape_tci_from_advance(university_name="มหาวิทยาลัยสงขลานครินทร์", output_file="tci_psu_results.csv"):
    options = Options()
    # options.add_argument("--headless")  # เปิดหน้าจอไว้ดูก่อน
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    # 1. เปิดหน้าค้นหาขั้นสูง
    driver.get("https://search.tci-thailand.org/advance_search.html")

    # 2. กรอกชื่อมหาวิทยาลัยในช่อง "หน่วยงาน"
    # รอให้ input โหลด
    wait.until(EC.presence_of_element_located((By.NAME, "keyword[]")))
    search_input = driver.find_element(By.NAME, "keyword[]")

    # กรอกชื่อมหาวิทยาลัย
    search_input.clear()
    search_input.send_keys(university_name)

    # กดปุ่มค้นหา
    wait.until(EC.element_to_be_clickable((By.ID, "searchBtn")))
    search_button = driver.find_element(By.ID, "searchBtn")
    search_button.click()

    # 4. รอผลลัพธ์
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.result")))
    time.sleep(2)  # ให้โหลดข้อมูลให้เสร็จสมบูรณ์

    results = []
    article_divs = driver.find_elements(By.CSS_SELECTOR, "div.result")

    for div in article_divs:
        title = div.find_element(By.CLASS_NAME, "title").text.strip() if div.find_elements(By.CLASS_NAME, "title") else ""
        journal = div.find_element(By.CLASS_NAME, "journal").text.strip() if div.find_elements(By.CLASS_NAME, "journal") else ""
        year = div.find_element(By.CLASS_NAME, "year").text.strip() if div.find_elements(By.CLASS_NAME, "year") else ""

        results.append({
            "title": title,
            "journal": journal,
            "year": year
        })

    print(f"✅ พบ {len(results)} บทความจาก {university_name}")

    driver.quit()

    # 5. บันทึกไฟล์ CSV
    df = pd.DataFrame(results)
    df.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"📁 บันทึกไฟล์เรียบร้อยที่ {output_file}")

if __name__ == "__main__":
    scrape_tci_from_advance()
