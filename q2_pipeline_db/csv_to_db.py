import pandas as pd
import psycopg2
import os

from psycopg2.extras import execute_values

def upload_csv_to_postgres(csv_path, conn_params, table_name='articles'):
    # โหลด CSV
    df = pd.read_csv(csv_path)
    
    # ตรวจสอบคอลัมน์ว่าตรงกับตาราง articles หรือยัง
    print("Columns in CSV:", df.columns.tolist())
    
    # สร้าง connection
    conn = psycopg2.connect(**conn_params)
    cur = conn.cursor()
    
    # เตรียม query insert
    cols = list(df.columns)
    query = f"INSERT INTO {table_name} ({', '.join(cols)}) VALUES %s"
    
    # แปลง dataframe เป็น list of tuples
    values = [tuple(x) for x in df.to_numpy()]
    
    try:
        execute_values(cur, query, values)
        conn.commit()
        print(f"Inserted {len(df)} rows into {table_name} successfully.")
    except Exception as e:
        print("Error inserting data:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    # ที่อยู่ไฟล์ CSV ที่ต้องการอัปโหลด
    base_dir = os.path.dirname(os.path.abspath(__file__))  # โฟลเดอร์ที่ไฟล์ csv_to_db.py อยู่
    csv_path = os.path.join(base_dir, 'data', 'combined_data.csv')
    
    # กำหนดพารามิเตอร์เชื่อมต่อ DB
    conn_params = {
        'host': 'localhost',
        'port': 5432,
        'dbname': 'research_db',
        'user': 'AreedaTJ',
        'password': 'AreedaTJ'
    }
    
    # เรียกฟังก์ชันโหลดข้อมูล
    upload_csv_to_postgres(csv_path, conn_params)
