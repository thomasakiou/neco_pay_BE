import pandas as pd

file_path = r"G:\Projects\neco-payment-manager-BE\COUNTING_PKGING__BATCH A_2025_SSCE_EXT.xlsx"
try:
    df = pd.read_excel(file_path, header=None, nrows=20)
    
    header_idx = -1
    for idx, row in df.iterrows():
        # Convert row to string and search for keywords
        row_str = str(row.values).upper()
        if "S/N" in row_str and "NAME" in row_str:
            header_idx = idx
            print(f"Found potential header at index {idx}")
            print("Row values:", row.values)
            break
            
    if header_idx != -1:
        # Read file again with correct header
        df_proper = pd.read_excel(file_path, header=header_idx, nrows=5)
        print("\nProper Headers detected:")
        print(list(df_proper.columns))
    else:
        print("Could not find header row.")
        
except Exception as e:
    print(f"Error reading file: {e}")
