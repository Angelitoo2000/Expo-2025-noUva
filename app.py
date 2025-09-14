import hashlib
import mysql.connector
from flask import Flask, jsonify, render_template, request, session, url_for
from flask_cors import CORS
import os
import uuid


app = Flask(__name__)
app.secret_key = "clave_super_secreta"   

app.config.update(
    SESSION_COOKIE_SAMESITE="Lax",  
    SESSION_COOKIE_SECURE=False     
)

CORS(app, supports_credentials=True, origins=["http://127.0.0.1:5000", "http://localhost:5000"])


UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- Database connection ---
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="fercho1232",   
            database="nouva",
            port=3306,
            ssl_disabled=True
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_user_data():
    if 'user_id' not in session:
        return None
    connection = get_db_connection()
    if connection is None:
        return None
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT nombre, foto_url FROM usuario WHERE usuario_id=%s", (session['user_id'],))
        user = cursor.fetchone()
        if user and (not user['foto_url']):
            user['foto_url'] = "default.png"
        return user
    except mysql.connector.Error as err:
        print(f"Error getting user data: {err}")
        return None
    finally:
        cursor.close()
        connection.close()

# --- Main routes ---
@app.route('/')
def principal():
    return render_template('Pagina_principal/principal_page.html')

@app.route('/login')
def login():
    return render_template('login_registro.html')

@app.route('/home')
def home_page():
    user_data = get_user_data()
    return render_template('Home/Home.html', user_data=user_data)

@app.route('/universities')
def universities_page():
    user_data = get_user_data()
    return render_template('universities/universities.html', user_data=user_data)

@app.route('/subcription')
def subcription_page():
    user_data = get_user_data()
    return render_template('subcription/subcription.html', user_data=user_data)

@app.route('/perfil')
def perfil_page():
    user_data = get_user_data()
    return render_template('perfil/perfil.html', user_data=user_data)

@app.route('/podcasts')
def podcasts_page():
    user_data = get_user_data()
    return render_template('podcasts/podcast.html', user_data=user_data)

@app.route('/challenges')
def challenges_page():
    user_data = get_user_data()
    return render_template('challenge/challenges.html', user_data=user_data)

@app.route('/challengeFuncional')
def challengeFuncional_page():
    user_data = get_user_data()
    return render_template('challenge-funcional/funcional-challenge.html', user_data=user_data)

@app.route('/donBosco')
def donBosco_page():
    user_data = get_user_data()
    return render_template('donBosco/Don_bosco.html', user_data=user_data)

# --- Register ---
@app.route('/users/register', methods=['POST'])
def register():
    data = request.json
    nombre = data.get('nombre')
    email = data.get('email')
    contrasena = data.get('contrasena')

    if not nombre or not email or not contrasena:
        return jsonify({"error": "All fields are required."}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Could not connect to the database."}), 500

    cursor = connection.cursor()
    try:
        cursor.execute("SELECT email FROM usuario WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({"error": "This email is already registered."}), 409

        hashed_password = hash_password(contrasena)
        cursor.execute("INSERT INTO usuario (nombre, email, contrasena) VALUES (%s, %s, %s)",
                       (nombre, email, hashed_password))
        connection.commit()
        return jsonify({"message": "Registration successful."}), 201
    finally:
        cursor.close()
        connection.close()


@app.route('/users/login', methods=['POST'])
def login_user():
    data = request.json
    email = data.get('email')
    contrasena = data.get('contrasena')

    if not email or not contrasena:
        return jsonify({"error": "All fields are required."}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Could not connect to the database."}), 500

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT usuario_id, contrasena FROM usuario WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user and user['contrasena'] == hash_password(contrasena):
            session['user_id'] = user['usuario_id']
            return jsonify({
                "message": "Login successful.",
                "redirect_url": url_for('home_page')
            }), 200
        else:
            return jsonify({"error": "Invalid email or password."}), 401
    finally:
        cursor.close()
        connection.close()


@app.route('/profile', methods=['GET', 'PUT'])
def profile():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized."}), 401

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Could not connect to the database."}), 500

    cursor = connection.cursor(dictionary=True)

    if request.method == 'GET':
        try:
            cursor.execute("SELECT nombre, foto_url FROM usuario WHERE usuario_id=%s", (session['user_id'],))
            user = cursor.fetchone()
            if user:
                return jsonify(user), 200
            else:
                return jsonify({"error": "User not found."}), 404
        finally:
            cursor.close()
            connection.close()

    elif request.method == 'PUT':
        data = request.json
        new_name = data.get('nombre')
        if not new_name:
            return jsonify({"error": "Name cannot be empty."}), 400

        try:
            cursor.execute("UPDATE usuario SET nombre = %s WHERE usuario_id = %s", (new_name, session['user_id']))
            connection.commit()
            return jsonify({"message": "Profile updated successfully."}), 200
        finally:
            cursor.close()
            connection.close()

# --- Upload & delete profile picture ---
@app.route('/profile/picture', methods=['POST'])
def upload_picture():
    if 'user_id' not in session: 
        return jsonify({"error": "Unauthorized."}), 401
    if 'file' not in request.files: 
        return jsonify({"error": "No file provided."}), 400
    file = request.files['file']
    if file.filename == '': 
        return jsonify({"error": "No file selected."}), 400
    
    if file:
        original_filename = file.filename
        file_extension = os.path.splitext(original_filename)[1]
        new_filename = str(uuid.uuid4()) + file_extension
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        
        file.save(filepath)
        
        connection = get_db_connection()
        if connection is None: 
            return jsonify({"error": "Could not connect to the database."}), 500
        
        cursor = connection.cursor()
        query = "UPDATE usuario SET foto_url = %s WHERE usuario_id = %s"
        db_path = f"uploads/{new_filename}" 
        cursor.execute(query, (db_path, session['user_id']))
        connection.commit()
        cursor.close()
        connection.close()
        
        full_url = url_for('static', filename=db_path)
        return jsonify({"message": "Profile picture updated successfully.", "foto_url": full_url}), 200
        
    return jsonify({"error": "An error occurred while uploading the file."}), 500

@app.route('/profile/picture', methods=['DELETE'])
def delete_picture():
    if 'user_id' not in session: 
        return jsonify({"error": "Unauthorized."}), 401
    
    connection = get_db_connection()
    if connection is None: 
        return jsonify({"error": "Could not connect to the database."}), 500
    
    cursor = connection.cursor()
    cursor.execute("UPDATE usuario SET foto_url = 'default.png' WHERE usuario_id = %s", (session['user_id'],))
    connection.commit()
    cursor.close()
    connection.close()
    
    default_url = url_for('static', filename='default.png')
    return jsonify({"message": "Profile picture removed.", "foto_url": default_url}), 200

# --- Run ---
if __name__ == '__main__':
    app.run(debug=True)
