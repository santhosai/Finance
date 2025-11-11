import pandas as pd
from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)

def load_finance_data():
    try:
        finance_df = pd.read_excel('nov 11.xlsx', sheet_name='Finance', header=1)
        finance_filtered = finance_df[(finance_df['Balance Amount '] != 0) & (finance_df['Balance Amount '].notna())].copy()
        finance_filtered = finance_filtered[finance_filtered['Names'].notna()]
        return finance_filtered.reset_index(drop=True)
    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame()

@app.route('/')
def index():
    return render_template('index.html', bg_version=123456)

@app.route('/api/names')
def get_names():
    finance_filtered = load_finance_data()
    if finance_filtered.empty:
        return jsonify([])
    names = sorted(finance_filtered['Names'].unique().tolist())
    return jsonify(names)

@app.route('/api/person/<name>')
def get_person_details(name):
    finance_filtered = load_finance_data()
    if finance_filtered.empty:
        return jsonify({'error': 'No data available'}), 404
        
    person_data = finance_filtered[finance_filtered['Names'] == name]
    if person_data.empty:
        return jsonify({'error': 'Person not found'}), 404
    
    row = person_data.iloc[0]
    
    # Simple calculation
    amount_given = float(row[' Amount Given']) if pd.notna(row[' Amount Given']) else 0
    amount_paid = float(row['Amount Paid ']) if pd.notna(row['Amount Paid ']) else 0
    balance_weeks = int(row['Balance Weeks']) if pd.notna(row['Balance Weeks']) else 0
    
    # Calculate paid weeks: simple ratio
    if amount_given > 0:
        payment_ratio = amount_paid / amount_given
        estimated_total_weeks = balance_weeks / (1 - payment_ratio) if payment_ratio < 1 else balance_weeks
        paid_weeks = int(estimated_total_weeks - balance_weeks)
    else:
        paid_weeks = 0
    
    details = {
        'name': row['Names'],
        'date_given': row['Date Given '].strftime('%d-%m-%Y') if pd.notna(row['Date Given ']) else 'N/A',
        'amount_given': amount_given,
        'amount_paid': amount_paid,
        'balance_amount': float(row['Balance Amount ']),
        'balance_weeks': balance_weeks,
        'paid_weeks': max(0, paid_weeks),
        'total_weeks': max(0, paid_weeks) + balance_weeks
    }
    
    return jsonify(details)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
