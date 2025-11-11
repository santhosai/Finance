import pandas as pd
from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', bg_version=123456)

@app.route('/api/names')
def get_names():
    try:
        df = pd.read_excel('nov 11.xlsx', sheet_name='Finance', header=1)
        df = df[(df['Balance Amount '] != 0) & (df['Balance Amount '].notna())]
        df = df[df['Names'].notna()]
        names = sorted(df['Names'].unique().tolist())
        return jsonify(names)
    except:
        return jsonify(['Test User'])

@app.route('/api/person/<name>')
def get_person_details(name):
    try:
        df = pd.read_excel('nov 11.xlsx', sheet_name='Finance', header=1)
        person = df[df['Names'] == name].iloc[0]
        
        return jsonify({
            'name': person['Names'],
            'date_given': 'N/A',
            'amount_given': float(person[' Amount Given']),
            'amount_paid': float(person['Amount Paid ']),
            'balance_amount': float(person['Balance Amount ']),
            'balance_weeks': int(person['Balance Weeks']),
            'paid_weeks': 3,  # Fixed for now
            'total_weeks': 10
        })
    except:
        return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
