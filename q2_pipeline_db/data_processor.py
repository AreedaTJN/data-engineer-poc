import pandas as pd

class DataProcessor:
    def __init__(self, df):
        self.df = df.copy()

    def standardize_columns(self):
        mapping = {
            'TITLE': 'ARTICLE_NAME',
            'ARTICLE_TITLE': 'ARTICLE_NAME',
        }
        self.df.rename(columns=mapping, inplace=True)
        
    def handle_missing_values(self):
        self.df.fillna("ไม่ระบุ", inplace=True)

    def deduplicate(self):
        self.df.drop_duplicates(inplace=True)
        
    def get_dataframe(self):
        return self.df
            