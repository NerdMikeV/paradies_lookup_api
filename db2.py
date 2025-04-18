import pyodbc

# Connect to your Azure SQL database
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=paradies-poc.database.windows.net;"
    "DATABASE=Paradies PoC;"
    "UID=adminuser;"
    "PWD=Mlv105524;"
    "TrustServerCertificate=yes;"
)
cursor = conn.cursor()

# Backroom SKUs list (same for both platforms for now)
backroom_skus = [
    '1114', '1004946', '1074422', '1015996', '1083856', '1007879',
    '1017906', '1032127', '1031971', '1066331', '1000507', '1043340',
    '1023935', '1077993', '1057538', '1009299', '1093186', '1076482',
    '1026637', '1074732', '1072178', '1120282'
]

# Insert into TYS
for sku in backroom_skus:
    cursor.execute("IF NOT EXISTS (SELECT 1 FROM [TYS Backroom SKUs] WHERE SKU = ?) INSERT INTO [TYS Backroom SKUs] (SKU) VALUES (?)", sku, sku)

# Insert into SAV
for sku in backroom_skus:
    cursor.execute("IF NOT EXISTS (SELECT 1 FROM [SAV Backroom SKUs] WHERE SKU = ?) INSERT INTO [SAV Backroom SKUs] (SKU) VALUES (?)", sku, sku)

conn.commit()
cursor.close()
conn.close()

print("✅ Backroom SKU data inserted successfully.")

