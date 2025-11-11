from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>OmSaiMurugan Finance</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: Arial; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .card { background: white; padding: 30px; border-radius: 15px; max-width: 500px; margin: 0 auto; }
        h1 { text-align: center; color: white; margin-bottom: 30px; }
        select, button { width: 100%; padding: 15px; margin: 10px 0; border-radius: 10px; border: 2px solid #667eea; }
        button { background: #667eea; color: white; cursor: pointer; }
        #result { margin-top: 20px; padding: 20px; background: #f8f9fa; border-radius: 10px; }
    </style>
</head>
<body>
    <h1>OmSaiMurugan Finance</h1>
    <div class="card">
        <select id="names"><option>Loading...</option></select>
        <button onclick="showDetails()">View Details</button>
        <div id="result"></div>
    </div>
    
    <script>
    fetch('/api/names').then(r=>r.json()).then(names=>{
        document.getElementById('names').innerHTML = names.map(n=>`<option value="${n}">${n}</option>`).join('');
    });
    
    function showDetails(){
        const name = document.getElementById('names').value;
        fetch('/api/person/'+name).then(r=>r.json()).then(data=>{
            document.getElementById('result').innerHTML = `
                <h3>📊 ${data.name}</h3>
                <p><strong>📅 Date Given:</strong> ${data.date_given}</p>
                <p><strong>💵 Amount Given:</strong> ₹${data.amount_given.toLocaleString()}</p>
                <p><strong>💸 Amount Paid:</strong> ₹${data.amount_paid.toLocaleString()}</p>
                <p><strong>⏳ Balance Amount:</strong> ₹${data.balance_amount.toLocaleString()}</p>
                <p><strong>💰 Weekly Amount:</strong> ₹${data.weekly_amount}</p>
                <p><strong>✅ Paid Weeks:</strong> ${data.paid_weeks} weeks</p>
                <p><strong>📆 Balance Weeks:</strong> ${data.balance_weeks} weeks</p>
            `;
        });
    }
    </script>
</body>
</html>
    '''

def load_finance_data():
    try:
        df = pd.read_excel('nov 11.xlsx', sheet_name='Finance', header=1)
        df = df[(df['Balance Amount '] != 0) & (df['Balance Amount '].notna())]
        df = df[df['Names'].notna()]
        return df.reset_index(drop=True)
    except Exception as e:
        print(f"Excel error: {e}")
        # Fallback to test data if Excel fails
        return pd.DataFrame([
            {'Names': 'Jaga', ' Amount Given': 10000, 'Amount Paid ': 3000, 'Balance Amount ': 7000, 'Date Given ': '2024-11-01'},
            {'Names': 'Ravi', ' Amount Given': 2000, 'Amount Paid ': 400, 'Balance Amount ': 1600, 'Date Given ': '2024-11-01'}
        ])

@app.route('/api/names')
def get_names():
    df = load_finance_data()
    names = sorted(df['Names'].unique().tolist())
    return jsonify(names)

@app.route('/api/person/<name>')
def get_person_details(name):
    df = load_finance_data()
    person_data = df[df['Names'] == name]
    
    if person_data.empty:
        return jsonify({'error': 'Person not found'}), 404
    
    row = person_data.iloc[0]
    
    # Get values safely
    amount_given = float(row[' Amount Given']) if pd.notna(row[' Amount Given']) else 0
    amount_paid = float(row['Amount Paid ']) if pd.notna(row['Amount Paid ']) else 0
    balance_amount = float(row['Balance Amount ']) if pd.notna(row['Balance Amount ']) else 0
    
    # Fixed logic: Always 10 weeks total
    if amount_given > 0:
        weekly_amount = amount_given / 10
        paid_weeks = int(amount_paid / weekly_amount)
        balance_weeks = 10 - paid_weeks
    else:
        weekly_amount = 0
        paid_weeks = 0
        balance_weeks = 10
    
    # Format date
    try:
        date_given = row['Date Given '].strftime('%d-%m-%Y') if pd.notna(row['Date Given ']) else 'N/A'
    except:
        date_given = 'N/A'
    
    return jsonify({
        'name': row['Names'],
        'date_given': date_given,
        'amount_given': amount_given,
        'amount_paid': amount_paid,
        'balance_amount': balance_amount,
        'weekly_amount': int(weekly_amount),
        'paid_weeks': paid_weeks,
        'balance_weeks': balance_weeks
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
