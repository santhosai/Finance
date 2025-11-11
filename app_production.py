from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Finance App Working!</h1><a href="/api/names">Test API</a>'

@app.route('/api/names')
def get_names():
    return jsonify(['Jaga', 'Ravi'])

@app.route('/api/person/<name>')
def get_person_details(name):
    if name == 'Jaga':
        return jsonify({
            'name': 'Jaga',
            'amount_given': 10000,
            'amount_paid': 3000,
            'balance_amount': 7000,
            'balance_weeks': 7,
            'paid_weeks': 3
        })
    return jsonify({'error': 'Not found'})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
