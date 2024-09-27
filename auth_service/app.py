from flask import Flask, request, jsonify

app = Flask(__name__)

# Datos de usuario hardcodeados
users = {
    'admin': 'admin'
}

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if users.get(username) == password:
        return jsonify({'message': 'Login exitoso'}), 200
    else:
        return jsonify({'message': 'Credenciales incorrectas'}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
