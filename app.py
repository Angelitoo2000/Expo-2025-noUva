from flask import Flask

app = Flask(__name__)

from routes.carreras_routes import carreras_bp
from routes.comentarios_routes import comentarios_bp
from routes.podcasts_routes import podcasts_bp
from routes.universidades_routes import universidades_bp
from routes.usuarios_routes import usuarios_bp

app.register_blueprint(carreras_bp)
app.register_blueprint(comentarios_bp)
app.register_blueprint(podcasts_bp)
app.register_blueprint(universidades_bp)
app.register_blueprint(usuarios_bp)

if __name__ == '__main__':
    app.run(debug=True)