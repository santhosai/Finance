import pandas as pd
from flask import Flask, render_template, jsonify
from datetime import datetime
import os

app = Flask(__name__)

# Excel file path - adjust for production
excel_file = 'nov 11.xlsx'

def load_finance_data():
    """Load and filter finance data from Excel - called on each request"""
    try:
        # Read Finance sheet with header at row 2 (index 1)
        finance_df = pd.read_excel(excel_file, sheet_name='Finance', header=1)
        
        # Apply filter: Balance Amount != 0
        finance_filtered = finance_df[(finance_df['Balance Amount '] != 0) & (finance_df['Balance Amount '].notna())].copy()
        
        # Remove rows where Names is NaN (empty rows)
        finance_filtered = finance_filtered[finance_filtered['Names'].notna()]
        
        # Reset index
        return finance_filtered.reset_index(drop=True)
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

@app.route('/')
def index():
    # Provide a cache-busting version value for the background image.
    import time
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
    if finance_filtered.empty:
        return jsonify([])
    names = sorted(finance_filtered['Names'].unique().tolist())
    return jsonify(names)

@app.route('/api/person/<name>')
def get_person_details(name):
    """Get details for a specific person"""
    finance_filtered = load_finance_data()
    if finance_filtered.empty:
        return jsonify({'error': 'No data available'}), 404
        
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
    # For production, use environment port or default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)