import pandas as pd

class DataProcessor:
    def __init__(self, df: pd.DataFrame):
        # เก็บสำเนาของ DataFrame ที่รับเข้ามา
        self.df = df.copy()

    def standardize_columns(self):
        """
        เปลี่ยนชื่อคอลัมน์ TITLE, ARTICLE_TITLE → ARTICLE_NAME
        เพื่อให้ทุกแหล่งข้อมูลใช้ชื่อเดียวกัน
        """
        mapping = {
            'TITLE': 'ARTICLE_NAME',
            'ARTICLE_TITLE': 'ARTICLE_NAME',
        }
        self.df.rename(columns=mapping, inplace=True)

    def handle_missing_values(self):
        """
        เติมค่า missing (NaN) ด้วยคำว่า 'ไม่ระบุ'
        """
        self.df.fillna("ไม่ระบุ", inplace=True)

    def deduplicate(self):
        """
        ลบข้อมูลที่ซ้ำกันใน DataFrame
        """
        self.df.drop_duplicates(inplace=True)

    def get_dataframe(self) -> pd.DataFrame:
        """
        ส่งคืน DataFrame ที่ถูกจัดการแล้ว
        """
        return self.df
