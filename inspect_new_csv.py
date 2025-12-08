import pandas as pd

file_path = r"G:\Projects\neco-payment-manager-BE\DISTRIBUTORS_BATCH_A_2025_SSCE_EXTERNAL_cleaned.csv"
try:
    df = pd.read_csv(file_path, nrows=1)
    print("Full Headers List:")
    for col in df.columns:
        print(f"'{col}'")
except Exception as e:
    print(f"Error reading file: {e}")
