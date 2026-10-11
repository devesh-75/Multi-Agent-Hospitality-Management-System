"""
Comprehensive Dataset Profiling Script for Agentic Fintech in Hospitality
Inspects C:\\Users\\deves\\Downloads\\project and outputs rigorous metadata.
"""

import os
import glob
import json
import pandas as pd
import numpy as np

PROJECT_DIR = r"C:\Users\deves\Downloads\project"

def inspect_all():
    csv_files = sorted(glob.glob(os.path.join(PROJECT_DIR, "*.csv")))
    print(f"Total CSV files found: {len(csv_files)}")
    
    full_inventory = []
    
    for fpath in csv_files:
        fname = os.path.basename(fpath)
        size_bytes = os.path.getsize(fpath)
        df = pd.read_csv(fpath)
        
        col_details = []
        for col in df.columns:
            s = df[col]
            null_count = int(s.isnull().sum())
            null_pct = round(float(s.isnull().mean()) * 100, 2)
            unique_count = int(s.nunique())
            
            # Identify samples
            samples = s.dropna().head(3).tolist()
            samples_str = [str(x)[:60] for x in samples]
            
            col_details.append({
                "column_name": col,
                "dtype": str(s.dtype),
                "null_count": null_count,
                "null_pct": null_pct,
                "unique_count": unique_count,
                "sample_values": samples_str
            })
            
        full_inventory.append({
            "filename": fname,
            "filepath": fpath,
            "file_size_bytes": size_bytes,
            "row_count": len(df),
            "column_count": len(df.columns),
            "columns": col_details
        })
        
    with open("docs/data_profiling_full.json", "w") as out:
        json.dump(full_inventory, out, indent=2)
        
    print("Exported docs/data_profiling_full.json successfully.")
    
    # Print high level summary table
    print("\n--- DATASET INVENTORY SUMMARY ---")
    print(f"{'Filename':<30} | {'Rows':<6} | {'Cols':<6} | {'Size (KB)':<10}")
    print("-" * 60)
    for item in full_inventory:
        print(f"{item['filename']:<30} | {item['row_count']:<6} | {item['column_count']:<6} | {item['file_size_bytes']/1024:<10.1f}")

if __name__ == "__main__":
    inspect_all()
