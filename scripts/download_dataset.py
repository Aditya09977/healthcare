"""
Dataset Acquisition Script
Official Source: Hospital Quarterly Financial & Utilization Report – Complete Data Set
HealthData.gov / California Department of Public Health (HCAI / CHHS)
Dataset URL: https://healthdata.gov/State/Hospital-Quarterly-Financial-Utilization-Report-Co/8j3z-qxvr
"""

import os
import json
import requests
import pandas as pd
from datetime import datetime

# CKAN Datastore Resource IDs for 2023 - 2024 Quarters
QUARTERS = {
    '2024Q4': {'id': 'b7875112-01b2-4f96-82a5-ea1682863b89', 'label': '2024 Q4 (12/31/2024)'},
    '2024Q3': {'id': '670a04a0-4503-40cc-955a-c1ba829ab460', 'label': '2024 Q3 (09/30/2024)'},
    '2024Q2': {'id': 'f5fc3b16-5bc8-4b22-98de-c836bf2cd687', 'label': '2024 Q2 (06/30/2024)'},
    '2024Q1': {'id': '82c67289-d5be-46a2-929a-e05f34fb3cb5', 'label': '2024 Q1 (03/31/2024)'},
    '2023Q4': {'id': '04ba86ad-b379-4dc0-ada6-282025eae2bd', 'label': '2023 Q4 (12/31/2023)'},
    '2023Q3': {'id': 'edf7157e-eebd-4a99-aef4-fdb2a738ac91', 'label': '2023 Q3 (09/30/2023)'},
    '2023Q2': {'id': '3790c896-1fcd-4ae6-85ec-4a1920d790b2', 'label': '2023 Q2 (06/30/2023)'},
    '2023Q1': {'id': 'a5939522-e62a-49ef-aa1f-ff9d2d98f494', 'label': '2023 Q1 (03/31/2023)'}
}

BASE_API_URL = "https://data.chhs.ca.gov/api/action/datastore_search"

def download_data():
    raw_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
    os.makedirs(raw_dir, exist_ok=True)
    
    all_dfs = []
    metadata_log = {
        'source_url': 'https://healthdata.gov/State/Hospital-Quarterly-Financial-Utilization-Report-Co/8j3z-qxvr',
        'api_endpoint': BASE_API_URL,
        'download_timestamp': datetime.now().isoformat(),
        'quarters': {}
    }
    
    print("=" * 70)
    print("Initiating Hospital Quarterly Financial & Utilization Report Acquisition")
    print("Source: California Health and Human Services (CHHS) / HealthData.gov")
    print("=" * 70)
    
    for qtr_key, qtr_info in QUARTERS.items():
        res_id = qtr_info['id']
        url = f"{BASE_API_URL}?resource_id={res_id}&limit=1000"
        print(f"Fetching {qtr_key} ({qtr_info['label']})...", end=" ", flush=True)
        try:
            resp = requests.get(url, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                if data.get('success'):
                    records = data['result']['records']
                    df_qtr = pd.DataFrame(records)
                    df_qtr['REPORTING_QUARTER'] = qtr_key
                    all_dfs.append(df_qtr)
                    count = len(records)
                    print(f"Success! {count} hospital records retrieved.")
                    metadata_log['quarters'][qtr_key] = {
                        'resource_id': res_id,
                        'record_count': count,
                        'columns': list(df_qtr.columns)
                    }
                else:
                    print(f"API Error: {data.get('error')}")
            else:
                print(f"HTTP Error {resp.status_code}")
        except Exception as e:
            print(f"Exception during request: {e}")
            
    if all_dfs:
        combined_df = pd.concat(all_dfs, ignore_index=True)
        output_csv = os.path.join(raw_dir, 'hospital_quarterly_data.csv')
        combined_df.to_csv(output_csv, index=False)
        print("-" * 70)
        print(f"Combined Dataset Saved: {output_csv}")
        print(f"Total Hospital-Quarter Observations: {len(combined_df)}")
        print(f"Unique Facilities: {combined_df['FAC_NO'].nunique()}")
        print(f"Total Columns: {len(combined_df.columns)}")
        
        meta_path = os.path.join(raw_dir, 'dataset_metadata.json')
        metadata_log['total_records'] = len(combined_df)
        metadata_log['unique_facilities'] = int(combined_df['FAC_NO'].nunique())
        metadata_log['total_features'] = len(combined_df.columns)
        with open(meta_path, 'w') as f:
            json.dump(metadata_log, f, indent=2)
        print(f"Metadata written to: {meta_path}")
        print("=" * 70)
        return combined_df
    else:
        raise RuntimeError("Failed to download any quarterly dataset from CHHS/HealthData.gov.")

if __name__ == '__main__':
    download_data()
