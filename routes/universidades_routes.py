from flask import Blueprint, jsonify
from db import get_db_connection

universidades_bp = Blueprint('universidades', __name__)

@universidades_bp.route('/universidades', methods=['GET'])
def get_universidades():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        'SELECT universidad_id, nombre_u, descripcion, imagen_url FROM universidades'
    )
    universidades = cursor.fetchall()
    cursor.close()
    connection.close()

    results = [
        {'id': p[0], 'nombre': p[1], 'descripcion': p[2], 'imagen_url': p[3]} for p in universidades
    ]
    return jsonify(results)
