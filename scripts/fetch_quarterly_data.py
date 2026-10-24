import os
import requests
import pandas as pd

quarters = {
    '2023_q1': 'https://data.chhs.ca.gov/dataset/22026f7b-198a-4708-b1ab-a4aa14885c6e/resource/a5939522-e62a-49ef-aa1f-ff9d2d98f494/download/2023_q1.xlsx',
    '2023_q2': 'https://data.chhs.ca.gov/dataset/22026f7b-198a-4708-b1ab-a4aa14885c6e/resource/3790c896-1fcd-4ae6-85ec-4a1920d790b2/download/2023_q2.xlsx',
    '2023_q3': 'https://data.chhs.ca.gov/dataset/22026f7b-198a-4708-b1ab-a4aa14885c6e/resource/edf7157e-eebd-4a99-aef4-fdb2a738ac91/download/2023_q3.xlsx',
    '2023_q4': 'https://data.chhs.ca.gov/dataset/22026f7b-198a-4708-b1ab-a4aa14885c6e/resource/04ba86ad-b379-4dc0-ada6-282025eae2bd/download/2023_q4.xlsx',
    '2024_q1': 'https://data.chhs.ca.gov/dataset/22026f7b-198a-4708-b1ab-a4aa14885c6e/resource/82c67289-d5be-46a2-929a-e05f34fb3cb5/download/2024_q1.xlsx'
}

raw_dir = os.path.join("data", "raw")
os.makedirs(raw_dir, exist_ok=True)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

quarter_dfs = []

for q_name, url in quarters.items():
    file_path = os.path.join(raw_dir, f"{q_name}.xlsx")
    if not os.path.exists(file_path):
        print(f"Downloading {q_name} from {url}...")
        r = requests.get(url, headers=headers, timeout=60)
        if r.status_code == 200:
            with open(file_path, "wb") as f:
                f.write(r.content)
            print(f"Saved {file_path} ({len(r.content)} bytes)")
        else:
            print(f"Failed to download {q_name}: status {r.status_code}")
            continue
    else:
        print(f"{file_path} already exists.")

    # Read and inspect
    df_q = pd.read_excel(file_path)
    df_q.columns = [str(c).strip().upper() for c in df_q.columns]
    print(f"{q_name}: shape={df_q.shape}, unique facilities={df_q['FAC_NO'].nunique() if 'FAC_NO' in df_q else 'N/A'}")
    df_q['QUARTER_SOURCE'] = q_name
    quarter_dfs.append(df_q)

# Concatenate all quarterly observations into a master quarterly dataframe
if quarter_dfs:
    combined_df = pd.concat(quarter_dfs, ignore_index=True)
    combined_path = os.path.join(raw_dir, "combined_quarterly_raw.csv")
    combined_df.to_csv(combined_path, index=False)
    print(f"\nSuccessfully combined quarterly data: total rows={len(combined_df)}, total columns={combined_df.shape[1]}")
    print(f"Unique facilities overall: {combined_df['FAC_NO'].nunique()}")
    print(f"Saved to {combined_path}")
