import pandas as pd

# Load the Excel file
excel_file = r'c:\Users\Admin\OneDrive\Desktop\OMSAIMURUGAN\nov 11.xlsx'

# Read Finance sheet with header at row 2 (index 1)
finance_df = pd.read_excel(excel_file, sheet_name='Finance', header=1)

# Apply filter: Balance Amount != 0
finance_filtered = finance_df[(finance_df['Balance Amount '] != 0) & (finance_df['Balance Amount '].notna())].copy()

# Remove rows where Names is NaN (empty rows)
finance_filtered = finance_filtered[finance_filtered['Names'].notna()]

# Select only the main columns (first 7 columns)
main_columns = ['Date Given ', 'Names', 'Balance Weeks', ' Amount Given', 'Balance Amount ', 'Amount Paid ']
finance_display = finance_filtered[main_columns].reset_index(drop=True)

print("✓ Finance Data (filtered by Balance Amount != 0):\n")
print(finance_display.to_string())
print(f"\n✓ Total filtered records: {len(finance_filtered)}")
print(f"✓ Columns shown: {', '.join(main_columns)}")
