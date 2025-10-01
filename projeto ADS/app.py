import sqlite3
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from bcrypt import hashpw, gensalt, checkpw
import random
import string

app = Flask(__name__)
CORS(app)

# Função para inicializar o banco de dados
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT,
            recovery_token TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT NOT NULL
        )
    ''')
    conn.commit()

    test_email = "test@educaprime.com"
    cursor.execute("SELECT * FROM Users WHERE email = ?", (test_email,))
    if not cursor.fetchone():
        password = "senha123"
        hashed_password = hashpw(password.encode('utf-8'), gensalt())
        cursor.execute("INSERT INTO Users (email, password_hash, full_name) VALUES (?, ?, ?)",
                       (test_email, hashed_password.decode('utf-8'), "Usuário de Teste"))
        conn.commit()
    conn.close()

# Rota para servir os arquivos HTML, CSS e JS
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

# Rota para login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM Users WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()

    if result and checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
        return jsonify({"success": True, "message": "Login realizado com sucesso!"})
    else:
        return jsonify({"success": False, "message": "Login ou senha incorretos."})

# Rota para cadastro de novo usuário
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT email FROM Users WHERE email = ?", (email,))
    if cursor.fetchone():
        conn.close()
        return jsonify({"success": False, "message": "Este e-mail já está cadastrado."})

    hashed_password = hashpw(password.encode('utf-8'), gensalt())

    try:
        cursor.execute("INSERT INTO Users (full_name, email, password_hash) VALUES (?, ?, ?)",
                       (full_name, email, hashed_password.decode('utf-8')))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Usuário cadastrado com sucesso!"})
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"success": False, "message": "Erro ao cadastrar. Tente novamente."})

# Rota para solicitar recuperação de senha (Etapa 1)
@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM Users WHERE email = ?", (email,))
    user = cursor.fetchone()

    if user:
        token = ''.join(random.choices(string.digits, k=6))
        cursor.execute("UPDATE Users SET recovery_token = ? WHERE email = ?", (token, email))
        conn.commit()
        conn.close()
        print(f"CÓDIGO DE RECUPERAÇÃO ENVIADO PARA {email}: {token}")
        return jsonify({"success": True, "message": "Código de recuperação enviado!"})
    else:
        conn.close()
        return jsonify({"success": False, "message": "E-mail não encontrado."})

# Rota para redefinir a senha (Etapa 2)
@app.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data.get('email')
    token = data.get('token')
    new_password = data.get('new_password')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT recovery_token FROM Users WHERE email = ?", (email,))
    result = cursor.fetchone()

    if result and result[0] == token:
        hashed_password = hashpw(new_password.encode('utf-8'), gensalt())
        cursor.execute("UPDATE Users SET password_hash = ?, recovery_token = NULL WHERE email = ?",
                       (hashed_password.decode('utf-8'), email))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Senha redefinida com sucesso!"})
    else:
        conn.close()
        return jsonify({"success": False, "message": "Token de recuperação inválido."})

# Rotas do CRUD para Cursos
@app.route('/courses', methods=['GET', 'POST'])
def handle_courses():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    if request.method == 'GET':
        cursor.execute("SELECT id, course_name FROM Courses")
        courses = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
        conn.close()
        return jsonify(courses)
    
    if request.method == 'POST':
        data = request.get_json()
        course_name = data.get('name')
        if not course_name:
            conn.close()
            return jsonify({"success": False, "message": "O nome do curso é obrigatório."}), 400

        try:
            cursor.execute("INSERT INTO Courses (course_name) VALUES (?)", (course_name,))
            conn.commit()
            conn.close()
            return jsonify({"success": True, "message": "Curso adicionado com sucesso!"})
        except sqlite3.IntegrityError:
            conn.close()
            return jsonify({"success": False, "message": "Erro ao adicionar o curso."}), 500

@app.route('/courses/<int:course_id>', methods=['PUT', 'DELETE'])
def handle_course(course_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'PUT':
        data = request.get_json()
        course_name = data.get('name')
        if not course_name:
            conn.close()
            return jsonify({"success": False, "message": "O nome do curso é obrigatório."}), 400
        
        cursor.execute("UPDATE Courses SET course_name = ? WHERE id = ?", (course_name, course_id))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Curso atualizado com sucesso!"})
    
    if request.method == 'DELETE':
        cursor.execute("DELETE FROM Courses WHERE id = ?", (course_id,))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Curso excluído com sucesso!"})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)