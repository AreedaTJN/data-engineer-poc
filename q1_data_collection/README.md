# 1.1 OpenAlex Scraper
สคริปต์นี้ใช้สำหรับดึงผลงานวิจัยทั้งหมดที่เกี่ยวข้องกับสถาบัน Prince of Songkla University จาก OpenAlex API และบันทึกข้อมูลลงไฟล์ CSV
## วิธีใช้งาน
1. ติดตั้งไลบรารีที่จำเป็น  
   ```
   pip install requests pandas
   ```
2. รันสคริปต์  
   ```
   python openalex_scraper.py ซึ่งอยู่ในโฟลเดอร์ q1_data_collection
   ```
3. ผลลัพธ์จะถูกบันทึกเป็นไฟล์ CSV ลงในโฟลเดอร์ data `data/openalex(PSU)_results_all.csv`
## รายละเอียดข้อมูลที่ดึง
- รหัสผลงาน (`id`)
- ชื่อเรื่อง (`title`)
- DOI
- ปีที่เผยแพร่ (`publication_year`)
- ประเภทผลงาน (`type`)
- จำนวนการอ้างอิง (`cited_by_count`)
- รายชื่อผู้แต่ง (`authors`)
- วารสารหรือแหล่งตีพิมพ์ (`host_venue`)
- สำนักพิมพ์ (`publisher`)
- สาขาวิชา (`concepts`)
## หมายเหตุ
- สามารถปรับจำนวนข้อมูลต่อหน้าได้ด้วย `per_page` (สูงสุด 200)
- สคริปต์จะดึงข้อมูลทุกหน้าโดยอัตโนมัติจนกว่าจะครบ

# 1.2