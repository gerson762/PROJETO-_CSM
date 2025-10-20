import uuid
import hashlib
import random
import string
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Função auxiliar para simular o hashing de senha
def hash_password(password):
    # Usa SHA256 para simular um hash seguro (nativo do Python)
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# =========================================================
# SIMULAÇÃO DO BANCO DE DADOS (PARA FUNCIONAR NO VERCEL)
# =========================================================

# Armazenamento em memória (os dados são perdidos após o deploy)
USERS = {
    "test@educaprime.com": {
        "id": 1,
        "email": "test@educaprime.com",
        "password_hash": hash_password("senha123"), # Usa hashlib
        "full_name": "Usuário de Teste Admin",
        "role": "admin",
        "recovery_token": None
    },
    "leitor@educaprime.com": {
        "id": 2,
        "email": "leitor@educaprime.com",
        "password_hash": hash_password("senha123"), # Usa hashlib
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
# ROTAS DO FLASK
# =========================================================

# Rota para servir os arquivos HTML, CSS e JS (Necessário para o Vercel)
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

# Rota para login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = USERS.get(email)

    if user and user["password_hash"] == hash_password(password): # Comparação usando hashlib
        user_role = user["role"]
        return jsonify({"success": True, "message": "Login realizado com sucesso!", "role": user_role})
    else:
        return jsonify({"success": False, "message": "Login ou senha incorretos."})

# Rota para cadastro de novo usuário
@app.route('/register', methods=['POST'])
def register():
    global USERS, NEXT_USER_ID
    data = request.get_json()
    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')

    if email in USERS:
        return jsonify({"success": False, "message": "Este e-mail já está cadastrado."})

    hashed_password = hash_password(password)

    USERS[email] = {
        "id": NEXT_USER_ID,
        "email": email,
        "password_hash": hashed_password,
        "full_name": full_name,
        "role": "leitor",
        "recovery_token": None
    }
    NEXT_USER_ID += 1
    return jsonify({"success": True, "message": "Usuário cadastrado com sucesso!"})

# Rota para solicitar recuperação de senha (Etapa 1)
@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')

    if email in USERS:
        token = ''.join(random.choices(string.digits, k=6))
        USERS[email]["recovery_token"] = token
        
        print(f"CÓDIGO DE RECUPERAÇÃO ENVIADO PARA {email}: {token}")
        return jsonify({"success": True, "message": "Código de recuperação enviado!"})
    else:
        return jsonify({"success": False, "message": "E-mail não encontrado."})

# Rota para redefinir a senha (Etapa 2)
@app.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data.get('email')
    token = data.get('token')
    new_password = data.get('new_password')

    user = USERS.get(email)

    if user and user["recovery_token"] == token:
        user["password_hash"] = hash_password(new_password)
        user["recovery_token"] = None
        return jsonify({"success": True, "message": "Senha redefinida com sucesso!"})
    else:
        return jsonify({"success": False, "message": "Token de recuperação inválido."})


# Rotas do CRUD para Cursos
@app.route('/courses', methods=['GET', 'POST'])
def handle_courses():
    global COURSES, NEXT_COURSE_ID

    if request.method == 'GET':
        courses_list = [{"id": course["id"], "name": course["course_name"]} for course in COURSES.values()]
        return jsonify(courses_list)
    
    if request.method == 'POST':
        data = request.get_json()
        course_name = data.get('name')
        if not course_name:
            return jsonify({"success": False, "message": "O nome do curso é obrigatório."}), 400

        new_id = NEXT_COURSE_ID
        COURSES[new_id] = {"id": new_id, "course_name": course_name}
        NEXT_COURSE_ID += 1
        return jsonify({"success": True, "message": "Curso adicionado com sucesso!"})

@app.route('/courses/<int:course_id>', methods=['PUT', 'DELETE'])
def handle_course(course_id):
    global COURSES
    user_role = request.headers.get('Authorization')

    if user_role not in ['admin', 'editor']:
        return jsonify({"success": False, "message": "Acesso não autorizado."}), 403

    if request.method == 'PUT':
        data = request.get_json()
        course_name = data.get('name')

        if not course_name:
            return jsonify({"success": False, "message": "O nome do curso é obrigatório."}), 400

        if course_id in COURSES:
            COURSES[course_id]["course_name"] = course_name
            return jsonify({"success": True, "message": "Curso atualizado com sucesso!"})
        else:
            return jsonify({"success": False, "message": "Curso não encontrado."}), 404
    
    if request.method == 'DELETE':
        if user_role != 'admin':
            return jsonify({"success": False, "message": "Acesso não autorizado. Apenas administradores podem excluir."}), 403

        if course_id in COURSES:
            del COURSES[course_id]
            return jsonify({"success": True, "message": "Curso excluído com sucesso!"})
        else:
            return jsonify({"success": False, "message": "Curso não encontrado."}), 404
