import hashlib
import random
import string
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Função auxiliar para simular o hashing de senha
def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# =========================================================
# SIMULAÇÃO DO BANCO DE DADOS (MEMÓRIA)
# =========================================================
USERS = {
    "test@educaprime.com": {
        "id": 1,
        "email": "test@educaprime.com",
        "password_hash": hash_password("senha123"),
        "full_name": "Usuário de Teste Admin",
        "role": "admin",
        "recovery_token": None
    },
    "leitor@educaprime.com": {
        "id": 2,
        "email": "leitor@educaprime.com",
        "password_hash": hash_password("senha123"),
        "full_name": "Usuário Leitor",
        "role": "leitor",
        "recovery_token": None
    }
}
NEXT_USER_ID = 3

COURSES = {
    1: {"id": 1, "course_name": "GESTÃO DE PROJETOS"},
    2: {"id": 2, "course_name": "PROGRAMAÇAO EM PYTHON"},
    3: {"id": 3, "course_name": "MARKETING DIGITAL"}
}
NEXT_COURSE_ID = 4

# =========================================================
# ROTAS
# =========================================================

# Rota genérica para servir arquivos estáticos (HTML, CSS, JS)
@app.route('/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory('.', filename)

# Rota para a raiz (página inicial)
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = USERS.get(email)
    if user and user["password_hash"] == hash_password(password):
        return jsonify({"success": True, "message": "Login realizado com sucesso!", "role": user["role"]})
    else:
        return jsonify({"success": False, "message": "Login ou senha incorretos."})

@app.route('/register', methods=['POST'])
def register():
    global USERS, NEXT_USER_ID
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')

    if email in USERS:
        return jsonify({"success": False, "message": "Este e-mail já está cadastrado."})

    USERS[email] = {
        "id": NEXT_USER_ID,
        "email": email,
        "password_hash": hash_password(password),
        "full_name": full_name,
        "role": "leitor",
        "recovery_token": None
    }
    NEXT_USER_ID += 1
    return jsonify({"success": True, "message": "Usuário cadastrado com sucesso!"})

@app.route('/courses', methods=['GET', 'POST'])
def handle_courses():
    global COURSES, NEXT_COURSE_ID
    if request.method == 'GET':
        courses_list = [{"id": c["id"], "name": c["course_name"]} for c in COURSES.values()]
        return jsonify(courses_list)
    if request.method == 'POST':
        data = request.get_json()
        new_id = NEXT_COURSE_ID
        COURSES[new_id] = {"id": new_id, "course_name": data.get('name')}
        NEXT_COURSE_ID += 1
        return jsonify({"success": True, "message": "Curso adicionado!"})

@app.route('/courses/<int:course_id>', methods=['PUT', 'DELETE'])
def handle_course_item(course_id):
    global COURSES
    # Simplificando a verificação de role para o teste
    if request.method == 'DELETE':
        if course_id in COURSES:
            del COURSES[course_id]
        return jsonify({"success": True, "message": "Curso excluído!"})
    if request.method == 'PUT':
        data = request.get_json()
        if course_id in COURSES:
            COURSES[course_id]["course_name"] = data.get('name')
        return jsonify({"success": True, "message": "Curso atualizado!"})