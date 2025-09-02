from flask import Blueprint, jsonify
from db import get_db_connection

carreras_bp = Blueprint('carreras', __name__)

@carreras_bp.route('/carreras', methods=['GET'])
def get_carreras():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT carrera_id, nombre, descripcion, duracion, universidad_id FROM carreras')
    carreras = cursor.fetchall()
    
    cursor.close()
    connection.close()

    results = [
        {'id': p[0], 'nombre': p[1], 'descripcion': p[2], 'duracion': p[3], 'universidad_id': p[4]} for p in carreras
    ]

    return jsonify(results)

