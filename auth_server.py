from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_user(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT username, password FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    return user

def add_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

def remove_user(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('DELETE FROM users WHERE username = ?', (username,))
    conn.commit()
    conn.close()

def update_user(username, new_password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('UPDATE users SET password = ? WHERE username = ?', (new_password, username))
    conn.commit()
    conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user = get_user(username)
    if user and user[1] == password:
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "failure"}), 401

@app.route('/add_user', methods=['POST'])
def add_user_route():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    add_user(username, password)
    return jsonify({"status": "user added"}), 201

@app.route('/remove_user', methods=['POST'])
def remove_user_route():
    data = request.json
    username = data.get('username')
    remove_user(username)
    return jsonify({"status": "user removed"}), 200

@app.route('/update_user', methods=['POST'])
def update_user_route():
    data = request.json
    username = data.get('username')
    new_password = data.get('new_password')
    update_user(username, new_password)
    return jsonify({"status": "user updated"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)