import pandas as pd

file_path = r"G:\Projects\neco-payment-manager-BE\COUNTING_PKGING__BATCH A_2025_SSCE_EXT.xlsx"
try:
    # Read first 10 rows without header to see raw data
    df = pd.read_excel(file_path, header=None, nrows=10)
    print("First 10 rows:")
    print(df)
except Exception as e:
    print(f"Error reading file: {e}")
