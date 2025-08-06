import sys
import os
import pandas as pd

# เพิ่ม path ของโฟลเดอร์ q2_pipeline_db เข้าไป
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from processors.data_processor import DataProcessor

# โหลดข้อมูล
df = pd.read_csv("q2_pipeline_db/data/scopus_selected.csv")

# ใช้งาน class
processor = DataProcessor(df)
processor.standardize_columns()
processor.handle_missing_values()
processor.deduplicate()

print(processor.get_dataframe().head())
