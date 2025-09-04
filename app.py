import hashlib
import mysql.connector
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Sh01@2",
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

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('login_registro.html')

@app.route('/home')
def home_page():
    return render_template('Home/index.html')

@app.route('/users/register', methods=['POST'])
def register_user():
    try:
        data = request.json
        name = data['nombre']
        lastname = data['apellido']
        email = data['email']
        password = data['contrasena']
    except KeyError as e:
        return jsonify({"error": f"Missing field in request: {e}"}), 400

    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        if connection is None:
            return jsonify({"error": "Could not connect to the database."}), 500
        
        cursor = connection.cursor()
        
        hashed_password = hash_password(password)

        query = """
            INSERT INTO usuarios (nombre, apellido, email, contrasena) 
            VALUES (%s, %s, %s, %s)
        """
        values = (name, lastname, email, hashed_password)

        cursor.execute(query, values)
        connection.commit()

        return jsonify({"message": "User registered successfully", "user": email}), 201

    except mysql.connector.Error as err:
        print(f"Error registering user: {err}")
        return jsonify({"error": "Email already exists or a database error occurred."}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/users/login', methods=['POST'])
def login_user():
    try:
        data = request.json
        email = data['email']
        password = data['password']
    except KeyError as e:
        return jsonify({"error": f"Missing field in request: {e}"}), 400

    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        if connection is None:
            return jsonify({"error": "Could not connect to the database."}), 500
        
        cursor = connection.cursor()

        query = "SELECT contrasena FROM usuarios WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        if result:
            stored_password = result[0]
            if hash_password(password) == stored_password:
                return jsonify({"message": "Login successful"}), 200
            else:
                return jsonify({"error": "Incorrect password"}), 401
        else:
            return jsonify({"error": "User not found"}), 404

    except mysql.connector.Error as err:
        print(f"Database error during login: {err}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == '__main__':
    app.run(debug=True)