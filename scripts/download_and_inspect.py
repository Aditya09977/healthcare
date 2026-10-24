import requests
import openpyxl
import pandas as pd
import os

url = "https://data.chhs.ca.gov/dataset/22026f7b-198a-4708-b1ab-a4aa14885c6e/resource/82c67289-d5be-46a2-929a-e05f34fb3cb5/download/2024_q1.xlsx"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

out_dir = os.path.join("data", "raw")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "2024_q1.xlsx")

print("Downloading 2024_q1.xlsx...")
r = requests.get(url, headers=headers, timeout=60)
if r.status_code == 200:
    with open(out_path, "wb") as f:
        f.write(r.content)
    print(f"Downloaded successfully: {len(r.content)} bytes.")
    
    # Inspect Excel sheets
    excel_file = pd.ExcelFile(out_path)
    print("Sheet names:", excel_file.sheet_names)
    
    # Read the first sheet
    for sheet in excel_file.sheet_names:
        df = pd.read_excel(out_path, sheet_name=sheet, nrows=5)
        print(f"\n--- Sheet '{sheet}' ---")
        print("Shape preview:", df.shape)
        print("Columns (first 30):", list(df.columns[:30]))
else:
    print(f"Failed with status: {r.status_code}")
