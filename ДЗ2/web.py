from flask import Flask, json
import mariadb

app = Flask(__name__)

config = {
    'host': 'db',
    'user': 'user',
    'password': 'password',
    'database': 'tpos_database'
}

@app.route('/', methods=['GET'])
def get_data():
    connection = mariadb.connect(**config)
    cursor = connection.cursor()
    cursor.execute("SELECT * from data")
    data = {}
    for item in cursor:
        name = item[0]
        age = item[1]
        data[name] = age
    cursor.close()
    connection.close()
    return json.dumps(data), 200

@app.route('/health', methods=['GET'])
def health_check():
    return json.dumps({"status": "OK"}), 200
    pass

@app.errorhandler(404)
def not_found(e):
    return json.dumps({"error": "Not Found"}), 404
