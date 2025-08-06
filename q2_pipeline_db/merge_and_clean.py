import os
import pandas as pd
from data_processor import DataProcessor

def load_and_clean():
    # หาตำแหน่งโฟลเดอร์หลัก (data-engineer-poc)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, 'data')

    # กำหนด path ไปยังไฟล์ต่าง ๆ อย่างชัดเจน
    sources = [
        os.path.join(DATA_DIR, 'scopus_selected.csv'),
        os.path.join(DATA_DIR, 'tci_selected.csv'),
        os.path.join(DATA_DIR, 'wos_selected.csv')
    ]

    combined_df = pd.DataFrame()

    for source in sources:
        print(f"กำลังอ่านไฟล์: {source}")
        try:
            df = pd.read_csv(source)
        except FileNotFoundError:
            print(f"ไม่พบไฟล์: {source}")
            continue

        processor = DataProcessor(df)
        processor.standardize_columns()
        processor.handle_missing_values()
        processor.deduplicate()

        cleaned_df = processor.get_dataframe()
        combined_df = pd.concat([combined_df, cleaned_df], ignore_index=True)

    # ถ้าไม่มีข้อมูลเลยให้หยุดและแจ้งเตือน
    if combined_df.empty:
        print("ไม่มีข้อมูลถูกโหลด ตรวจสอบไฟล์ในโฟลเดอร์ 'data/'")
        return

    expected_columns = ['ARTICLE_NAME', 'AUTHOR', 'OUTPUT_YEAR', 'JOURNAL', 'VOLUME', 'ISSUE',
                        'PAGE_RANGE', 'SOURCE']
    combined_df = combined_df[expected_columns]
    combined_df.drop_duplicates(inplace=True)
    combined_df.reset_index(drop=True, inplace=True)

    # สร้างโฟลเดอร์ data (เผื่อไม่มี)
    os.makedirs(DATA_DIR, exist_ok=True)

    # เขียนไฟล์
    output_path = os.path.join(DATA_DIR, 'combined_cleaned_data.csv')
    try:
        combined_df.to_csv(output_path, index=False)
        print(f'เขียนไฟล์สำเร็จ: {output_path}')
    except Exception as e:
        print(f'เขียนไฟล์ไม่สำเร็จ: {e}')

# เรียกฟังก์ชันเมื่อรันไฟล์โดยตรง
if __name__ == "__main__":
    load_and_clean()
