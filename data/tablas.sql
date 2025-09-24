CREATE TABLE accidentes (
    id_accidente INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_caso VARCHAR(20) UNIQUE NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    lugar VARCHAR(200) NOT NULL,
    distrito VARCHAR(100),
    provincia VARCHAR(100),
    departamento VARCHAR(100),
    latitud DECIMAL(10,8),
    longitud DECIMAL(11,8),
    tipo_accidente VARCHAR(50) NOT NULL,
    gravedad VARCHAR(20) NOT NULL,
    condiciones_climaticas VARCHAR(50),
    estado_via VARCHAR(50),
    iluminacion VARCHAR(30),
    superficie_via VARCHAR(30),
    señalizacion VARCHAR(30),
    heridos INTEGER DEFAULT 0,
    fallecidos INTEGER DEFAULT 0,
    vehiculos_involucrados INTEGER NOT NULL,
    descripcion TEXT,
    croquis_url VARCHAR(255),
    fotos_url TEXT,
    estado_caso VARCHAR(20) DEFAULT 'abierto',
    id_usuario_registro INTEGER,
    id_comisaria INTEGER,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME,
    FOREIGN KEY (id_usuario_registro) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_comisaria) REFERENCES comisarias(id_comisaria)
);

CREATE TABLE usuarios (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_usuario VARCHAR(20) UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    dni VARCHAR(8) UNIQUE,
    cargo VARCHAR(50),
    institucion VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    telefono VARCHAR(15),
    password_hash VARCHAR(255),
    nivel_acceso VARCHAR(20) DEFAULT 'operador',
    activo BOOLEAN DEFAULT 1,
    ultimo_acceso DATETIME,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE vehiculos (
    id_vehiculo INTEGER PRIMARY KEY AUTOINCREMENT,
    id_accidente INTEGER,
    tipo_vehiculo VARCHAR(50) NOT NULL,
    marca VARCHAR(50),
    modelo VARCHAR(50),
    placa VARCHAR(20),
    año INTEGER,
    color VARCHAR(30),
    numero_motor VARCHAR(50),
    numero_chasis VARCHAR(50),
    seguro_soat VARCHAR(50),
    estado_vehiculo VARCHAR(30),
    daños_descripcion TEXT,
    conductor_nombre VARCHAR(100),
    conductor_apellido VARCHAR(100),
    conductor_dni VARCHAR(8),
    conductor_licencia VARCHAR(50),
    conductor_telefono VARCHAR(15),
    propietario_nombre VARCHAR(100),
    propietario_dni VARCHAR(8),
    FOREIGN KEY (id_accidente) REFERENCES accidentes(id_accidente) ON DELETE CASCADE
);

CREATE TABLE personas (
    id_persona INTEGER PRIMARY KEY AUTOINCREMENT,
    id_accidente INTEGER,
    tipo_persona VARCHAR(20) NOT NULL, -- 'herido', 'fallecido', 'testigo', 'conductor', 'pasajero'
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    dni VARCHAR(8),
    edad INTEGER,
    sexo VARCHAR(1),
    direccion VARCHAR(200),
    telefono VARCHAR(15),
    estado_salud VARCHAR(50),
    hospital_traslado VARCHAR(100),
    lesiones_descripcion TEXT,
    parentesco_conductor VARCHAR(50),
    posicion_vehiculo VARCHAR(30), -- 'conductor', 'copiloto', 'pasajero_trasero'
    uso_cinturon BOOLEAN,
    uso_casco BOOLEAN,
    FOREIGN KEY (id_accidente) REFERENCES accidentes(id_accidente) ON DELETE CASCADE
);

CREATE TABLE comisarias (
    id_comisaria INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_comisaria VARCHAR(100) NOT NULL,
    distrito VARCHAR(100),
    provincia VARCHAR(100),
    departamento VARCHAR(100),
    direccion VARCHAR(200),
    telefono VARCHAR(15),
    comisario_cargo VARCHAR(100),
    activo BOOLEAN DEFAULT 1
);

CREATE TABLE tipos_accidente (
    id_tipo INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_tipo VARCHAR(50) NOT NULL,
    descripcion TEXT,
    gravedad_base VARCHAR(20),
    activo BOOLEAN DEFAULT 1
);

CREATE TABLE causas_accidente (
    id_causa INTEGER PRIMARY KEY AUTOINCREMENT,
    id_accidente INTEGER,
    tipo_causa VARCHAR(50), -- 'humana', 'vehicular', 'ambiental', 'infraestructura'
    descripcion_causa TEXT,
    factor_principal BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (id_accidente) REFERENCES accidentes(id_accidente) ON DELETE CASCADE
);

CREATE TABLE documentos (
    id_documento INTEGER PRIMARY KEY AUTOINCREMENT,
    id_accidente INTEGER,
    tipo_documento VARCHAR(50), -- 'parte_policial', 'certificado_medico', 'foto', 'croquis'
    nombre_archivo VARCHAR(255),
    ruta_archivo VARCHAR(500),
    tamaño_kb INTEGER,
    fecha_subida DATETIME DEFAULT CURRENT_TIMESTAMP,
    subido_por INTEGER,
    FOREIGN KEY (id_accidente) REFERENCES accidentes(id_accidente) ON DELETE CASCADE,
    FOREIGN KEY (subido_por) REFERENCES usuarios(id_usuario)
);

CREATE TABLE seguimientos (
    id_seguimiento INTEGER PRIMARY KEY AUTOINCREMENT,
    id_accidente INTEGER,
    fecha_seguimiento DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado_anterior VARCHAR(20),
    estado_nuevo VARCHAR(20),
    observaciones TEXT,
    id_usuario INTEGER,
    FOREIGN KEY (id_accidente) REFERENCES accidentes(id_accidente) ON DELETE CASCADE,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);
