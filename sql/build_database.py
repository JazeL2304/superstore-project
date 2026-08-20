import sqlite3
import pandas as pd
import os

def build_database():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, "..", "data", "Sample_-_Superstore.csv")
    db_path = os.path.join(current_dir, "superstore.db")
    
    print(f"Reading CSV from: {csv_path}")
    try:
        df = pd.read_csv(csv_path, encoding='windows-1252')
    except Exception:
        df = pd.read_csv(csv_path, encoding='latin1')
        
    # Standardize column names (replace spaces and hyphens with underscores)
    df.columns = [col.replace(' ', '_').replace('-', '_') for col in df.columns]
    
    # Convert dates to ISO YYYY-MM-DD
    df['Order_Date'] = pd.to_datetime(df['Order_Date'], format='%m/%d/%Y', errors='coerce').dt.strftime('%Y-%m-%d')
    df['Ship_Date'] = pd.to_datetime(df['Ship_Date'], format='%m/%d/%Y', errors='coerce').dt.strftime('%Y-%m-%d')
    
    print(f"Sample data after date conversion:\n{df[['Order_ID', 'Order_Date', 'Ship_Date', 'Sub_Category', 'Sales', 'Profit']].head(3)}")
    
    conn = sqlite3.connect(db_path)
    df.to_sql('superstore', conn, if_exists='replace', index=False)
    conn.close()
    
    print(f"Database successfully created at: {db_path} with {len(df)} records.")

if __name__ == "__main__":
    build_database()
