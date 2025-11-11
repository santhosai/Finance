from flask import Flask, jsonify

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
                <p><strong>💵 Amount Given:</strong> ₹${data.amount_given.toLocaleString()}</p>
                <p><strong>💸 Amount Paid:</strong> ₹${data.amount_paid.toLocaleString()}</p>
                <p><strong>⏳ Balance Amount:</strong> ₹${data.balance_amount.toLocaleString()}</p>
                <p><strong>💰 Weekly Amount:</strong> ₹${data.weekly_amount}</p>
                <p><strong>✅ Paid Weeks:</strong> ${data.paid_weeks} weeks</p>
                <p><strong>📆 Balance Weeks:</strong> ${data.balance_weeks} weeks</p>
                <p><strong>📊 Total Weeks:</strong> 10 weeks</p>
            `;
        });
    }
    </script>
</body>
</html>
    '''

@app.route('/api/names')
def get_names():
    return jsonify(['Jaga', 'Ravi', 'Kumar'])

@app.route('/api/person/<name>')
def get_person_details(name):
    data = {
        'Jaga': {'amount_given': 10000, 'amount_paid': 3000},
        'Ravi': {'amount_given': 2000, 'amount_paid': 400},
        'Kumar': {'amount_given': 5500, 'amount_paid': 1100}
    }
    
    if name in data:
        person = data[name]
        
        # Fixed logic: Always 10 weeks total
        weekly_amount = person['amount_given'] / 10
        paid_weeks = int(person['amount_paid'] / weekly_amount)
        balance_weeks = 10 - paid_weeks
        balance_amount = person['amount_given'] - person['amount_paid']
        
        return jsonify({
            'name': name,
            'amount_given': person['amount_given'],
            'amount_paid': person['amount_paid'],
            'balance_amount': balance_amount,
            'weekly_amount': int(weekly_amount),
            'paid_weeks': paid_weeks,
            'balance_weeks': balance_weeks
        })
    
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
