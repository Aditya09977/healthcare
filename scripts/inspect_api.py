import requests
import json

urls_to_try = [
    "https://healthdata.gov/resource/8j3z-qxvr.json?$limit=5",
    "https://healthdata.gov/api/views/8j3z-qxvr/rows.csv?accessType=DOWNLOAD",
    "https://data.ca.gov/api/3/action/package_search?q=Hospital+Quarterly+Financial"
]

print("--- Testing Socrata JSON API ---")
try:
    r = requests.get("https://healthdata.gov/resource/8j3z-qxvr.json", params={"$limit": 5}, timeout=20)
    print("Status:", r.status_code)
    if r.status_code == 200:
        data = r.json()
        print(f"Retrieved {len(data)} records.")
        if data:
            print("Columns:", list(data[0].keys()))
            print("First record sample:", json.dumps(data[0], indent=2))
    else:
        print("Error text:", r.text[:400])
except Exception as e:
    print("Exception:", e)

print("\n--- Testing Metadata Endpoint ---")
try:
    r_meta = requests.get("https://healthdata.gov/api/views/8j3z-qxvr.json", timeout=20)
    print("Meta Status:", r_meta.status_code)
    if r_meta.status_code == 200:
        meta = r_meta.json()
        print("Name:", meta.get("name"))
        print("Description:", str(meta.get("description"))[:300])
        print("Columns count:", len(meta.get("columns", [])))
        cols = [c.get("name") for c in meta.get("columns", [])]
        print("First 20 columns:", cols[:20])
except Exception as e:
    print("Meta Exception:", e)
