import pandas as pd
import glob
import os
import time
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from urllib.parse import quote_plus

# --- CONNECTION SETUP ---
params = quote_plus(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=paradies-poc.database.windows.net;"
    "DATABASE=Paradies PoC;"
    "UID=adminuser;"
    "PWD=Mlv105524;"
    "TrustServerCertificate=yes;"
)

conn_str = f"mssql+pyodbc:///?odbc_connect={params}"

# --- BUILD ENGINE WITH RETRIES ---
retries = 5
delay = 20
engine = None

for attempt in range(retries):
    try:
        engine = create_engine(conn_str)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT GETDATE()"))
            print("✅ Connected! SQL Server time:", result.fetchone()[0])
            break
    except OperationalError as e:
        print(f"⏳ Attempt {attempt + 1} failed: {e}")
        print(f"🔁 Waiting {delay} seconds before retry...")
        time.sleep(delay)
else:
    print("❌ Could not connect to SQL after multiple attempts.")
    exit()

# --- PATH TO YOUR FILES ---
folder_path = r'C:\Users\micha\Documents\Paradies Database Creation'
excel_files = glob.glob(os.path.join(folder_path, "*.xlsx"))

# --- LOOP THROUGH FILES + SHEETS ---
for file in excel_files:
    print(f"\n📂 Processing file: {os.path.basename(file)}")
    all_sheets = pd.read_excel(file, sheet_name=None)

    for sheet_name, df in all_sheets.items():
        if df.empty:
            print(f"   ⚠️ Skipping empty sheet: {sheet_name}")
            continue

        # Generate clean SQL table name
        base_name = os.path.splitext(os.path.basename(file))[0]
        clean_sheet = sheet_name.lower().replace(' ', '_').replace('-', '_').replace(',', '')
        table_name = f"{base_name}_{clean_sheet}".lower()[:100]  # Trim if needed

        print(f"   → Uploading sheet: {sheet_name} → table: {table_name}")

        try:
            df.to_sql(table_name, con=engine, if_exists='replace', index=False)
            print(f"      ✅ Uploaded {len(df)} rows to {table_name}")
        except Exception as e:
            print(f"      ❌ Error uploading {table_name}: {e}")

