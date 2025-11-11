from flask import Flask, render_template, jsonify

app = Flask(__name__)

test_data = [
    {'name': 'Jaga', 'amount_given': 10000, 'amount_paid': 3000, 'balance_amount': 7000, 'balance_weeks': 7},
    {'name': 'Ravi', 'amount_given': 5000, 'amount_paid': 1000, 'balance_amount': 4000, 'balance_weeks': 4}
]

@app.route('/')
def index():
    return render_template('index.html', bg_version=123456)

@app.route('/api/names')
def get_names():
    names = [person['name'] for person in test_data]
    return jsonify(names)

@app.route('/api/person/<name>')
def get_person_details(name):
    for person in test_data:
        if person['name'] == name:
            paid_weeks = person['amount_paid'] // 1000
            return jsonify({
                'name': person['name'],
                'date_given': '01-11-2024',
                'amount_given': person['amount_given'],
                'amount_paid': person['amount_paid'],
                'balance_amount': person['balance_amount'],
                'balance_weeks': person['balance_weeks'],
                'paid_weeks': paid_weeks,
                'total_weeks': paid_weeks + person['balance_weeks']
            })
    return jsonify({'error': 'Person not found'}), 404

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
