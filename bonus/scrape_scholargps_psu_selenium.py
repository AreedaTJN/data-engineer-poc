from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time, csv, json

def find_next_page_button(driver):
    buttons = driver.find_elements(By.CSS_SELECTOR, "a.pagination_button_number")
    for btn in buttons:
        try:
            icon = btn.find_element(By.CSS_SELECTOR, "i.fas.fa-chevron-right")
            # ถ้าเจอ icon ลูกศรขวา แสดงว่านี่คือปุ่ม next
            return btn
        except NoSuchElementException:
            continue
    return None

BASE_URL = "https://scholargps.com/search.php?q=profile&affiliation_ac=70466324193403&source=affiliation&type=global&global_search_type=scholar&page="

options = Options()
# options.add_argument("--headless=new")  # ถ้าอยากรันแบบไม่แสดงหน้าต่างเบราว์เซอร์ให้เปิดบรรทัดนี้
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

profile_links = set()
page = 1

while True:
    url = BASE_URL + str(page)
    print(f"[INFO] เปิดหน้าผลลัพธ์หน้า {page}...")
    driver.get(url)

    try:
        # รอให้ลิงก์โปรไฟล์โหลดมา
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href*='/scholars/']")))
    except:
        print("[INFO] โหลดข้อมูลหน้าไม่สำเร็จหรือหมดหน้าแล้ว")
        break

    links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/scholars/']")
    current_page_links = set()
    for link in links:
        href = link.get_attribute("href")
        if href and "/scholars/" in href:
            current_page_links.add(href.split("?")[0])

    if not current_page_links:
        print("[INFO] ไม่มีโปรไฟล์ในหน้านี้, จบการค้นหา")
        break

    # ถ้าหน้านี้ไม่เพิ่มลิงก์ใหม่เลย แสดงว่าอาจหมดข้อมูล
    if current_page_links.issubset(profile_links):
        print("[INFO] ไม่มีโปรไฟล์ใหม่ในหน้านี้, สิ้นสุดการค้นหา")
        break

    profile_links.update(current_page_links)
    print(f"[INFO] เจอโปรไฟล์ {len(current_page_links)} รายในหน้านี้, รวมทั้งหมด {len(profile_links)} ราย")

    # แก้ไขตรงนี้ เช็คปุ่ม next โดยหา icon ลูกศรขวา
    next_btn = find_next_page_button(driver)
    if next_btn:
        print("[INFO] พบปุ่มหน้าถัดไป กำลังคลิกเพื่อโหลดหน้าใหม่...")
        next_btn.click()
        time.sleep(3)  # รอโหลดหน้าใหม่
        page += 1
    else:
        print("[INFO] ไม่พบปุ่มหน้าถัดไป, สิ้นสุดการค้นหา")
        break

print(f"[INFO] รวมโปรไฟล์ทั้งหมด {len(profile_links)} ราย กำลังดึงข้อมูลรายละเอียด...")

profiles = []
for i, url in enumerate(sorted(profile_links), 1):
    print(f"[{i}/{len(profile_links)}] เข้าโปรไฟล์: {url}")
    driver.get(url)
    time.sleep(1.5)

    try:
        name = driver.find_element(By.TAG_NAME, "h1").text.strip()
    except:
        name = None

    try:
        email_elem = driver.find_element(By.CSS_SELECTOR, "a[href^='mailto:']")
        email = email_elem.get_attribute("href").split(":", 1)[1]
    except:
        email = None

    profiles.append({
        "name": name,
        "email": email,
        "url": url
    })

driver.quit()

with open("scholargps_psu_scholars_allpages.json", "w", encoding="utf-8") as jf:
    json.dump(profiles, jf, ensure_ascii=False, indent=2)

with open("scholargps_psu_scholars_allpages.csv", "w", newline="", encoding="utf-8") as cf:
    writer = csv.DictWriter(cf, fieldnames=["name", "email", "url"])
    writer.writeheader()
    writer.writerows(profiles)

print("[INFO] เสร็จสิ้น! บันทึกข้อมูลครบทุกโปรไฟล์แล้ว")
