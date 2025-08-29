from flask import Blueprint, jsonify
from db import get_db_connection
 
usuarios_bp = Blueprint('usuarios', __name__)
 
@usuarios_bp.route('/usuarios', methods=['GET'])
def get_usuarios():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        'SELECT usuario_id, nombre, apellido, email FROM usuarios'
    )
    usuarios = cursor.fetchall()
    cursor.close()
    connection.close()
   
    results = [
        {'id': p[0], 'nombre': p[1], 'apellido': p[2], 'email': p[3]} for p in usuarios
    ]
 
    return jsonify(results)
