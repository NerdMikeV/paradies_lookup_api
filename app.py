from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)

# SQL connection setup
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=paradies-poc.database.windows.net;"
    "DATABASE=Paradies PoC;"
    "UID=adminuser;"
    "PWD=Mlv105524;"
    "TrustServerCertificate=yes;"
)

@app.route("/")
def home():
    return "✅ Flask API is running!"

@app.route("/api/lookup", methods=["POST"])
def lookup_product():
    data = request.get_json()
    platform = data.get("platform", "").upper()
    upc = data.get("upc")
    sap = data.get("sap")

    if not platform or platform not in ["ATL", "SAV", "TYS"]:
        return jsonify({"error": "Invalid or missing platform"}), 400

    if not upc and not sap:
        return jsonify({"error": "Please provide a UPC or SAP Material Number"}), 400

    # Table mapping
    table_map = {
        "ATL": {
            "mara": "[sales atl 64 weeks_working_v3_mara_material_master]",
            "abc": "[sales atl 64 weeks_working_v3_a_b_c_analysis]"
        },
        "SAV": {
            "mara": "[sales sav 64 weeks_working_v3_mara_material_master]",
            "abc": "[sales sav 64 weeks_working_v3_a_b_c_analysis]",
            "backroom": "[SAV Backroom SKUs]"
        },
        "TYS": {
            "mara": "[sales tys 64 weeks_working_v3 (2)_mara_material_master]",
            "abc": "[sales tys 64 weeks_working_v3 (2)_a_b_c_analysis]",
            "backroom": "[TYS Backroom SKUs]"
        }
    }

    conn_cursor = conn.cursor()
    mara_table = table_map[platform]["mara"]
    abc_table = table_map[platform]["abc"]

    try:
        # If UPC provided, get SAP from MARA table
        if upc:
            query = f"""
                SELECT TOP 1 [Matl]
                FROM {mara_table}
                WHERE [EAN/UPC] = ?
            """
            conn_cursor.execute(query, upc)
            row = conn_cursor.fetchone()
            if not row:
                return jsonify({"error": "UPC not found"}), 404
            sap = row[0]

        # Use SAP to get full product info
        query = f"""
            SELECT TOP 1 
                abc.[SKU] AS sap,
                abc.[Item Name] AS description,
                abc.[A-B-C] AS velocity,
                mara.[EAN/UPC] AS upc
            FROM {abc_table} abc
            LEFT JOIN {mara_table} mara
                ON abc.[SKU] = mara.[Matl]
            WHERE abc.[SKU] = ?
        """
        conn_cursor.execute(query, sap)
        row = conn_cursor.fetchone()
        if not row:
            return jsonify({"error": "SAP not found"}), 404

        columns = [col[0] for col in conn_cursor.description]
        result = dict(zip(columns, row))

        # Add backroom field if platform is SAV or TYS
        if platform in ["SAV", "TYS"]:
            backroom_table = table_map[platform]["backroom"]
            conn_cursor.execute(f"SELECT 1 FROM {backroom_table} WHERE SKU = ?", sap)
            result["backroom_allowed"] = bool(conn_cursor.fetchone())

        return jsonify(result)

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": "Server error", "details": str(e)}), 500

# 👇 Render uses port 8080 and needs production WSGI server
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"🚀 Starting Flask server on http://0.0.0.0:{port}")
    app.run(debug=True, host="0.0.0.0", port=port)







