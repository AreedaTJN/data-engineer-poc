import pandas as pd
from typing import List

class DataProcessor:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def standardize_columns(self):
        mapping = {
            'TITLE': 'ARTICLE_NAME',
            'ARTICLE_TITLE': 'ARTICLE_NAME',
        }
        self.df.rename(columns=mapping, inplace=True)

    def handle_missing_values(self):
        self.df.fillna('ไม่ระบุ', inplace=True)

    def deduplicate(self):
        self.df.drop_duplicates(inplace=True)

    def process(self) -> pd.DataFrame:
        self.standardize_columns()
        self.handle_missing_values()
        self.deduplicate()
        return self.df

    @staticmethod
    def combine(dfs: List[pd.DataFrame]) -> pd.DataFrame:
        """
        รวม DataFrame หลายอันแล้วลบข้อมูลซ้ำที่เกิดจากการรวม
        """
        combined_df = pd.concat(dfs, ignore_index=True)
        combined_df.drop_duplicates(inplace=True)
        return combined_df