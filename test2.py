from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def test_chrome():
    options = Options()
    options.add_argument("--headless")  # ไม่เปิดหน้าต่าง
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # ไม่ต้องระบุ path เพราะอยู่ใน PATH แล้ว
    driver = webdriver.Chrome(options=options)

    driver.get("https://www.google.com")
    print("✅ Page title:", driver.title)

    driver.quit()

if __name__ == "__main__":
    test_chrome()
