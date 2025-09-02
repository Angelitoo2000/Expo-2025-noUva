from flask import Blueprint, jsonify
from db import get_db_connection

comentarios_bp = Blueprint('comentarios', __name__)

@comentarios_bp.route('/comentarios', methods=['GET'])
def get_comentarios():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        'SELECT comentario_id, contenido, fecha, usuario_id, podcast_id FROM comentarios'
    )
    comentarios = cursor.fetchall()
    cursor.close()
    connection.close()
   
    results = [
        {'id': p[0], 'contenido': p[1], 'fecha': p[2].strftime('%Y-%m-%d %H:%M:%S'), 'usuario_id': p[3], 'podcast_id': p[4]} for p in comentarios
        ]
    return jsonify(results)
