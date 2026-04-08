## Codigo de mySQL

CREATE DATABASE IF NOT EXISTS nouva;
USE nouva;
 
CREATE TABLE usuario (
    usuario_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    foto_url VARCHAR(255) NOT NULL DEFAULT 'default.png'
);


 
CREATE TABLE universidades (
    universidad_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre_u VARCHAR(150) NOT NULL,
    descripcion TEXT,
    imagen_url TEXT
);
 
CREATE TABLE carreras (
    carrera_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    duracion VARCHAR(50),
    universidad_id INT,
    FOREIGN KEY (universidad_id) REFERENCES universidades(universidad_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
 
CREATE TABLE podcasts (
    podcast_id INT PRIMARY KEY AUTO_INCREMENT,
    video TEXT NOT NULL,
    nombre_video VARCHAR(150) NOT NULL,
    descripcion TEXT,
    universidad_id INT,
    carrera_id INT,
    FOREIGN KEY (universidad_id) REFERENCES universidades(universidad_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    FOREIGN KEY (carrera_id) REFERENCES carreras(carrera_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);
 
CREATE TABLE comentarios (
    comentario_id INT PRIMARY KEY AUTO_INCREMENT,
    contenido TEXT NOT NULL,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    usuario_id INT,
    podcast_id INT,
    FOREIGN KEY (usuario_id) REFERENCES usuario(usuario_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (podcast_id) REFERENCES podcasts(podcast_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
 
INSERT INTO carreras (nombre, descripcion) VALUES ('Systems engineering', 'Engineering program at Don Bosco University is the discipline responsible for creating, developing, and managing software systems. This degree program is the engine that drives technology, from the applications you use on your phone to the complex systems that control entire companies and networks.');

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE comentarios;
TRUNCATE TABLE podcasts;
TRUNCATE TABLE carreras;
SET FOREIGN_KEY_CHECKS = 1;CREATE DATABASE IF NOT EXISTS nouva;
USE nouva;
