import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from urllib.parse import quote_plus

# Connection string
params = quote_plus(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=paradies-poc.database.windows.net;"
    "DATABASE=Paradies PoC;"
    "UID=adminuser;"
    "PWD=Mlv105524;"
    "TrustServerCertificate=yes;"
)
conn_str = f"mssql+pyodbc:///?odbc_connect={params}"
engine = create_engine(conn_str)

# File and sheet to retry
file_path = r"C:\Users\micha\Documents\Paradies Database Creation\SALES ATL 64 weeks_Working_v3.xlsx"
sheet_name = "2032, 2033, 2034"
table_name = "sales atl 64 weeks_working_v3_2032_2033_2034"

# Reload sheet and upload
df = pd.read_excel(file_path, sheet_name=sheet_name)

with engine.connect() as conn:
    print(f"🚀 Re-uploading {sheet_name} → {table_name}")
    df.to_sql(table_name, con=conn, if_exists="replace", index=False)
    print(f"✅ Successfully re-uploaded {len(df)} rows to {table_name}")
