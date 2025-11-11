import pandas as pd
from flask import Flask, render_template, jsonify
from datetime import datetime
import os

app = Flask(__name__)

# Excel file path
excel_file = r'c:\Users\Admin\OneDrive\Desktop\OMSAIMURUGAN\nov 11.xlsx'

def load_finance_data():
    """Load and filter finance data from Excel - called on each request"""
    # Read Finance sheet with header at row 2 (index 1)
    finance_df = pd.read_excel(excel_file, sheet_name='Finance', header=1)
    
    # Apply filter: Balance Amount != 0
    finance_filtered = finance_df[(finance_df['Balance Amount '] != 0) & (finance_df['Balance Amount '].notna())].copy()
    
    # Remove rows where Names is NaN (empty rows)
    finance_filtered = finance_filtered[finance_filtered['Names'].notna()]
    
    # Reset index
    return finance_filtered.reset_index(drop=True)

@app.route('/')
def index():
    # Provide a cache-busting version value for the background image.
    # If you place a background image at static/bg.jpg the template will use it.
    import os, time
    bg_path = os.path.join(app.static_folder, 'bg.jpg')
    if os.path.exists(bg_path):
        bg_version = int(os.path.getmtime(bg_path))
    else:
        bg_version = int(time.time())
    return render_template('index.html', bg_version=bg_version)

@app.route('/api/names')
def get_names():
    """Get list of all names"""
    finance_filtered = load_finance_data()
    names = sorted(finance_filtered['Names'].unique().tolist())
    return jsonify(names)

@app.route('/api/person/<name>')
def get_person_details(name):
    """Get details for a specific person"""
    finance_filtered = load_finance_data()
    person_data = finance_filtered[finance_filtered['Names'] == name]
    
    if person_data.empty:
        return jsonify({'error': 'Person not found'}), 404
    
    row = person_data.iloc[0]
    
    # Calculate paid weeks (count non-zero values in date columns)
    date_columns = [col for col in finance_filtered.columns if '202' in str(col) or '201' in str(col)]
    paid_weeks = 0
    for col in date_columns:
        if pd.notna(row[col]) and row[col] != 0:
            paid_weeks += 1
    
    # Balance weeks
    balance_weeks = row['Balance Weeks'] if pd.notna(row['Balance Weeks']) else 0
    
    details = {
        'name': row['Names'],
        'date_given': row['Date Given '].strftime('%d-%m-%Y') if pd.notna(row['Date Given ']) else 'N/A',
        'amount_given': float(row[' Amount Given']) if pd.notna(row[' Amount Given']) else 0,
        'amount_paid': float(row['Amount Paid ']) if pd.notna(row['Amount Paid ']) else 0,
        'balance_amount': float(row['Balance Amount ']),
        'balance_weeks': int(balance_weeks),
        'paid_weeks': paid_weeks,
        'total_weeks': int(balance_weeks) + paid_weeks
    }
    
    return jsonify(details)

if __name__ == '__main__':
    # Bind to 0.0.0.0 so other devices on the same LAN (your phone) can access the app
    # Run on port 5001 to avoid any cached/old app instances on :5000
    # Example: http://<your-pc-ip>:5001
    app.run(host='0.0.0.0', debug=True, port=5001)
