from flask import Blueprint, jsonify
from db import get_db_connection

podcasts_bp = Blueprint('podcasts', __name__)

@podcasts_bp.route('/podcasts', methods=['GET'])
def get_podcasts():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        'SELECT podcast_id, video, nombre_video, descripcion, universidad_id, carrera_id FROM podcasts'
    )
    podcasts = cursor.fetchall()
    cursor.close()
    connection.close()

    results = [
        { 'id': p[0], 'video': p[1], 'nombre_video': p[2], 'descripcion': p[3], 'universidad_id': p[4], 'carrera_id': p[5] } for p in podcasts
    ]
    return jsonify(results)
