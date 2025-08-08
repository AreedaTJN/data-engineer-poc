import os
import pandas as pd
import sys

# เพิ่ม path ของ processors ให้ import class_data_processor ได้ (หากยังไม่ได้เพิ่ม)
current_dir = os.path.dirname(__file__)
processors_path = os.path.abspath(current_dir)
if processors_path not in sys.path:
    sys.path.append(processors_path)

from class_data_processor import DataProcessor

def main():
    # โหลดไฟล์ csv ด้วย path ที่สัมพันธ์กับตำแหน่งไฟล์นี้
    base_data_path = os.path.abspath(os.path.join(current_dir, '../data'))
    
    tci_df = pd.read_csv(os.path.join(base_data_path, 'tci_selected.csv'))
    scopus_df = pd.read_csv(os.path.join(base_data_path, 'scopus_selected.csv'))
    wos_df = pd.read_csv(os.path.join(base_data_path, 'wos_selected.csv'), encoding='utf-8')

    tci_clean = DataProcessor(tci_df).process()
    scopus_clean = DataProcessor(scopus_df).process()
    wos_clean = DataProcessor(wos_df).process()

    combined = DataProcessor.combine([tci_clean, scopus_clean, wos_clean])

    # สร้าง mapping แปลงชื่อแหล่งเป็นเลข
    source_mapping = {
        'tci': 1,
        'scopus': 2,
        'wos': 3
    }

    # แปลงค่าคอลัมน์ SOURCE ให้เป็นตัวเลข
    combined['source_id'] = combined['SOURCE'].map(source_mapping)

    # ถ้าไม่ต้องการคอลัมน์ 'SOURCE' เดิมก็ลบออก
    combined.drop(columns=['SOURCE'], inplace=True)

    # เปลี่ยนชื่อคอลัมน์ทั้งหมดเป็นตัวพิมพ์เล็ก
    combined.columns = combined.columns.str.lower()

    # สร้างโฟลเดอร์ output ถ้ายังไม่มี
    output_dir = base_data_path
    os.makedirs(output_dir, exist_ok=True)

    combined.to_csv(os.path.join(output_dir, 'combined_data.csv'), index=False)
    print(f"Combined data saved to {os.path.join(output_dir, 'combined_data.csv')}")

if __name__ == '__main__':
    main()
