import sqlite3
from flask import Flask, g, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATABASE = 'gas_data.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    return render_template('index.html')

# API ruta za dohvatanje svih očitavanja
@app.route('/api/readings', methods=['GET'])
def get_readings():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM readouts ORDER BY id DESC LIMIT 50")
    readings = cursor.fetchall()
    return jsonify([dict(r) for r in readings])

# API ruta za dodavanje novog očitavanja sa Arduina
@app.route('/api/readings', methods=['POST'])
def add_reading():
    data = request.json
    if not data or 'value' not in data:
        return jsonify({'error': 'Vrednost (value) je obavezna'}), 400

    val = data['value']
    status = "ALARM" if val > 400 else "NORMAL"

    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO readouts (value, status) VALUES (?, ?)", (val, status))
    db.commit()

    return jsonify({'id': cursor.lastrowid, 'value': val, 'status': status}), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)