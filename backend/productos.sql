DROP TABLE IF EXISTS producto;

CREATE TABLE producto(
    id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR NOT NULL,
    descripcion VARCHAR NOT NULL,
    precio VARCHAR NOT NULL,
    stock VARCHAR NOT NULL,
    categoria VARCHAR NOT NULL,
    img BLOB NOT NULL,
    uid_vendedor VARCHAR NOT NULL
);

DROP TABLE IF EXISTS  imagenes;

CREATE TABLE imagenes(
    id_imagen INTEGER PRIMARY KEY AUTOINCREMENT,
    img BLOB NOT NULL
);

DROP TABLE IF EXISTS productoss;

CREATE TABLE productoss(
    id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR NOT NULL,
    descripcion VARCHAR NOT NULL,
    precio NUMERIC NOT NULL,
    stock INT NOT NULL,
    categoria VARCHAR NOT NULL,
    uid_vendedor VARCHAR NOT NULL
); 
