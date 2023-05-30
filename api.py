from flask import Flask, request, jsonify
from functools import wraps
import jwt
import model

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

users = {
    "admin": "admin_password"
}

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"message": "Authentication required"}), 401
        try:
            jwt.decode(token, app.config['SECRET_KEY'])
        except jwt.DecodeError:
            return jsonify({"message": "Invalid token"}), 401
        return f(*args, **kwargs)
    return decorated

def generate_token(username):
    payload = {'username': username}
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if check_auth(username, password):
        token = generate_token(username)
        return jsonify({'token': token.decode('utf-8')})
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

def check_auth(username, password):
    return username in users and users[username] == password

@app.route('/keywords', methods=['POST'])
@requires_auth
def keywords():
    data = request.get_json()
    segment = data.get('segment')
    locality = data.get('locality')

    if segment is None or locality is None:
        return jsonify({'message': 'Segment and locality are required parameters.'}), 400

    prompt = f"Ótimo! Liste para mim quais são as palavras chave para uma empresa de {segment}, localizada em {locality}. Responda apenas a lista, incluindo algumas de cauda longa. A lista deve ter no máximo 15 itens. Não inclua explicações antes ou depois da lista. O resultado deve ser apenas uma lista de palavras chave separadas por vírgula."

    response = model.prompt(prompt)
    response = response.replace('\n', '')
    return jsonify({'keywords': response})


if __name__ == '__main__':
    app.run()
