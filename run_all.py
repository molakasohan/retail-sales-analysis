import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure working directory is the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Ensure data and outputs directories exist
os.makedirs("data", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# Copy sales_data.csv into data/ if it's in the root
if os.path.exists("sales_data.csv") and not os.path.exists("data/sales_data.csv"):
    import shutil
    shutil.copy("sales_data.csv", "data/sales_data.csv")

print("=" * 50)
print("STEP 1: Generating Dataset...")
print("=" * 50)
import generate_data
df = generate_data.generate_sales_data()
df.to_csv("data/sales_data.csv", index=False)
df.to_csv("sales_data.csv", index=False)
print(f"Generated {len(df)} transactions in 'data/sales_data.csv' and 'sales_data.csv'")

print("\n" + "=" * 50)
print("STEP 2: Running Analysis & Computing KPIs...")
print("=" * 50)
import analysis
analysis.DATA_PATH = "data/sales_data.csv"
analysis.OUT_DIR = "outputs"
analysis.main()

# Also copy outputs to root for easy viewing
for out_file in os.listdir("outputs"):
    src_file = os.path.join("outputs", out_file)
    dst_file = os.path.join(".", out_file)
    if os.path.isfile(src_file):
        import shutil
        shutil.copy(src_file, dst_file)

print("\n" + "=" * 50)
print("Pipeline execution completed successfully!")
print("=" * 50)
