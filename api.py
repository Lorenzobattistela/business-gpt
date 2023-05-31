from flask import Flask, request, jsonify
from functools import wraps
import jwt
import model

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

users = {
    "admin": "admin_password"
}
model = model.Model()

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

@app.route('/description', methods=['POST'])
@requires_auth
def description():
    data = request.get_json()
    company_name = data.get('company_name')
    old_description = data.get('old_description')

    if company_name is None or old_description is None:
        return jsonify({'message': 'Company name and old description are required parameters.'}), 400
    
    prompt = "Agora preciso que você crie uma descrição com, no máximo, 750 caracteres para o Google Meu Negócio dessa empresa. O nome da empresa é {company_name}. Utilize como base as informações da descrição atual:{old_description}. Lembre-se de deixar o SEO otimizado com as palavras chave. Ao responder, envie apenas o texto da descrição e mais nada."
    response = model.prompt(prompt)
    response = response.replace('\n', '')
    return jsonify({'description': response})

@app.route('/post', methods=['POST'])
@requires_auth
def post():
    data = request.get_json()
    company_name = data.get('company_name')
    product_or_service_name = data.get('product_or_service_name')
    prompt_type = 'impulse_post'

    if company_name is None or product_or_service_name is None:
        return jsonify({'message': 'Company name and product or service name are required parameters.'}), 400
    
    model.prompt(f"A estrutura do [POST IMPULSO] serve para criar a descrição de Posts para o Google Meu Negócio. Essa descrição deve ser escrita utilizando a técnica AIDA de copywriting e deve sempre incluir as palavras chave que listamos lá no começo e que são relevantes para a empresa {company_name}. O objetivo desses posts é ganhar relevância para as palavras chave, para que o perfil melhore seu ranqueamento nas buscas. Sempre que eu te solicitar isso, vou te informar o produto ou serviço que vamos divulgar no post. Entendido?", prompt_type=prompt_type)

    response = model.prompt(f"[POST IMPULSO] Serviço: Divulgar o produto/serviço de {product_or_service_name}. Responda apenas com a divulgação e mais nada.", prompt_type=prompt_type)
    response = response.replace('\n', '')
    return jsonify({'post': response})

@app.route('/evaluation', methods=['POST'])
@requires_auth
def evaluation():
    data = request.get_json()
    company_name = data.get('company_name')
    evaluation = data.get('evaluation')
    prompt_type = 'client_evaluation'

    if company_name is None or evaluation is None:
        return jsonify({'message': 'Company name and evaluation are required parameters.'}), 400
    
    model.prompt(f"A estrutura [AVALIAÇÃO] serve para responder as avaliações realizadas pelos clientes na página do Google Meu Negócio da {company_name}. Precisamos fazer respostas amigáveis, positivas e devem sempre incluir as palavras chave que listamos lá no começo e que são relevantes para o melhor ranqueamento da empresa, bem como as cidades de atuação. Preciso que você altere o padrão das respostas e torne-as diferentes, para a pessoa perceber que foi escrito diretamente para ela. O objetivo dessas respostas é fidelizar o cliente e ganhar relevância para as palavras chave, para melhorar nas buscas. Sempre que eu for te solicitar isso, vou colar abaixo a avaliação realizada pelo cliente. Responda apenas a resposta da avaliação e mais nada. Entendido?", prompt_type=prompt_type)

    response = model.prompt(f"CLIENTE: {evaluation}", prompt_type=prompt_type)
    response = response.replace('\n', '')
    return jsonify({'evaluation': response})

if __name__ == '__main__':
    app.run()
