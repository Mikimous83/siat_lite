PRAGMA foreign_keys = ON;

-- =====================================================
-- 🌎 UBICACIONES GEOGRÁFICAS
-- =====================================================
CREATE TABLE IF NOT EXISTS ubicaciones (
    id_ubicacion INTEGER PRIMARY KEY AUTOINCREMENT,
    departamento VARCHAR(100) NOT NULL,
    provincia VARCHAR(100) NOT NULL,
    distrito VARCHAR(100) NOT NULL
);

-- =====================================================
-- 🧩 ROLES DE USUARIOS
-- =====================================================
CREATE TABLE IF NOT EXISTS roles (
    id_rol INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_rol VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT
);

-- =====================================================
-- 🏢 ASEGURADORAS
-- =====================================================
CREATE TABLE IF NOT EXISTS aseguradoras (
    id_aseguradora INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(15),
    direccion VARCHAR(200)
);

-- =====================================================
-- 📂 TIPOS DE DOCUMENTO
-- =====================================================
CREATE TABLE IF NOT EXISTS tipos_documento (
    id_tipo_doc INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_tipo VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT
);

-- =====================================================
-- 🧠 TIPOS DE ACCIDENTE
-- =====================================================
CREATE TABLE IF NOT EXISTS tipos_accidente (
    id_tipo INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_tipo VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT,
    gravedad_base VARCHAR(20),
    activo BOOLEAN DEFAULT 1
);

-- =====================================================
-- 🚘 TIPOS DE VEHÍCULO
-- =====================================================
CREATE TABLE IF NOT EXISTS tipos_vehiculo (
    id_tipo_vehiculo INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_tipo VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT
);

-- =====================================================
-- 🧭 TIPOS DE VÍA
-- =====================================================
CREATE TABLE IF NOT EXISTS tipos_via (
    id_tipo_via INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_tipo VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT
);

-- =====================================================
-- 🧾 NIVELES DE GRAVEDAD (CATÁLOGO)
-- =====================================================
CREATE TABLE IF NOT EXISTS niveles_gravedad (
    id_gravedad INTEGER PRIMARY KEY AUTOINCREMENT,
    nivel VARCHAR(20) NOT NULL UNIQUE,
    descripcion TEXT
);

-- =====================================================
-- 👮‍♂️ USUARIOS DEL SISTEMA
-- =====================================================
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    id_rol INTEGER,
    codigo_usuario VARCHAR(20) UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    dni VARCHAR(8),
    cargo VARCHAR(50),
    institucion VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    telefono VARCHAR(15),
    password_hash VARCHAR(255),
    activo BOOLEAN DEFAULT 1,
    ultimo_acceso TEXT,
    fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_rol) REFERENCES roles(id_rol) ON UPDATE CASCADE
);

-- =====================================================
-- 🏢 COMISARIAS
-- =====================================================
CREATE TABLE IF NOT EXISTS comisarias (
    id_comisaria INTEGER PRIMARY KEY AUTOINCREMENT,
    id_ubicacion INTEGER,
    nombre_comisaria VARCHAR(100) NOT NULL,
    direccion VARCHAR(200),
    telefono VARCHAR(15),
    comisario_cargo VARCHAR(100),
    activo BOOLEAN DEFAULT 1,
    FOREIGN KEY (id_ubicacion) REFERENCES ubicaciones(id_ubicacion) ON UPDATE CASCADE
);

-- =====================================================
-- 🧾 TABLA PRINCIPAL: ACCIDENTES
-- =====================================================
CREATE TABLE IF NOT EXISTS accidentes (
    id_accidente INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_caso VARCHAR(20) UNIQUE,
    fecha TEXT,
    hora TEXT,
    lugar VARCHAR(200),
    latitud DECIMAL(10, 8),
    longitud DECIMAL(11, 8),
    id_tipo INTEGER,
    id_comisaria INTEGER,
    id_usuario_registro INTEGER,
    id_gravedad INTEGER,
    descripcion TEXT,
    condiciones_climaticas VARCHAR(50),
    id_tipo_via INTEGER,
    iluminacion VARCHAR(30),
    señalizacion VARCHAR(30),
    estado_caso VARCHAR(20),
    heridos INTEGER DEFAULT 0,
    fallecidos INTEGER DEFAULT 0,
    vehiculos_involucrados INTEGER DEFAULT 0,
    croquis_url VARCHAR(255),
    fotos_url TEXT,
    fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TEXT,
    FOREIGN KEY (id_tipo) REFERENCES tipos_accidente(id_tipo),
    FOREIGN KEY (id_comisaria) REFERENCES comisarias(id_comisaria),
    FOREIGN KEY (id_usuario_registro) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_gravedad) REFERENCES niveles_gravedad(id_gravedad),
    FOREIGN KEY (id_tipo_via) REFERENCES tipos_via(id_tipo_via)
);

-- =====================================================
-- ⚙️ CAUSAS DE ACCIDENTE
-- =====================================================
CREATE TABLE IF NOT EXISTS causas_accidente (
    id_causa INTEGER PRIMARY KEY AUTOINCREMENT,
    id_accidente INTEGER NOT NULL,
    tipo_causa VARCHAR(50),
    descripcion_causa TEXT,
    factor_principal BOOLEAN DEFAULT 0,
    FOREIGN KEY (id_accidente) REFERENCES accidentes(id_accidente) ON DELETE CASCADE
);

-- =====================================================
-- 🧍‍♂️ PERSONAS INVOLUCRADAS
-- =====================================================
CREATE TABLE IF NOT EXISTS personas (
    id_persona INTEGER PRIMARY KEY AUTOINCREMENT,
    id_accidente INTEGER NOT NULL,
    tipo_persona VARCHAR(20),
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    dni VARCHAR(8),
    edad INTEGER,
    sexo VARCHAR(1),
    direccion VARCHAR(200),
    telefono VARCHAR(15),
    estado_salud VARCHAR(50),
    hospital_traslado VARCHAR(100),
    lesiones_descripcion TEXT,
    parentesco_conductor VARCHAR(50),
    posicion_vehiculo VARCHAR(30),
    uso_cinturon BOOLEAN,
    uso_casco BOOLEAN,
    FOREIGN KEY (id_accidente) REFERENCES accidentes(id_accidente) ON DELETE CASCADE
);

-- =====================================================
-- 🚗 VEHÍCULOS INVOLUCRADOS
-- =====================================================
CREATE TABLE IF NOT EXISTS vehiculos (
    id_vehiculo INTEGER PRIMARY KEY AUTOINCREMENT,
    id_accidente INTEGER NOT NULL,
    id_tipo_vehiculo INTEGER,
    id_aseguradora INTEGER,
    tipo_vehiculo VARCHAR(50),
    marca VARCHAR(50),
    modelo VARCHAR(50),
    placa VARCHAR(20),
    año INTEGER,
    color VARCHAR(30),
    numero_motor VARCHAR(50),
    numero_chasis VARCHAR(50),
    estado_vehiculo VARCHAR(30),
    daños_descripcion TEXT,
    conductor_nombre VARCHAR(100),
    conductor_apellido VARCHAR(100),
    conductor_dni VARCHAR(8),
    conductor_licencia VARCHAR(50),
    conductor_telefono VARCHAR(15),
    propietario_nombre VARCHAR(100),
    FOREIGN KEY (id_accidente) REFERENCES accidentes(id_accidente) ON DELETE CASCADE,
    FOREIGN KEY (id_tipo_vehiculo) REFERENCES tipos_vehiculo(id_tipo_vehiculo),
    FOREIGN KEY (id_aseguradora) REFERENCES aseguradoras(id_aseguradora)
);

-- =====================================================
-- 📄 DOCUMENTOS (EVIDENCIAS)
-- =====================================================
CREATE TABLE IF NOT EXISTS documentos (
    id_documento INTEGER PRIMARY KEY AUTOINCREMENT,
    id_accidente INTEGER NOT NULL,
    id_tipo_doc INTEGER,
    nombre_archivo VARCHAR(255),
    ruta_archivo VARCHAR(500),
    tamaño_kb INTEGER,
    fecha_subida TEXT DEFAULT CURRENT_TIMESTAMP,
    subido_por INTEGER,
    FOREIGN KEY (id_accidente) REFERENCES accidentes(id_accidente) ON DELETE CASCADE,
    FOREIGN KEY (id_tipo_doc) REFERENCES tipos_documento(id_tipo_doc),
    FOREIGN KEY (subido_por) REFERENCES usuarios(id_usuario)
);

-- =====================================================
-- 🧾 SEGUIMIENTOS DE CASOS
-- =====================================================
CREATE TABLE IF NOT EXISTS seguimientos (
    id_seguimiento INTEGER PRIMARY KEY AUTOINCREMENT,
    id_accidente INTEGER NOT NULL,
    fecha_seguimiento TEXT DEFAULT CURRENT_TIMESTAMP,
    estado_anterior VARCHAR(20),
    estado_nuevo VARCHAR(20),
    observaciones TEXT,
    id_usuario INTEGER,
    FOREIGN KEY (id_accidente) REFERENCES accidentes(id_accidente) ON DELETE CASCADE,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

-- =====================================================
-- 🕵️ AUDITORÍA DEL SISTEMA
-- =====================================================
CREATE TABLE IF NOT EXISTS auditoria (
    id_auditoria INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER,
    accion TEXT,
    tabla_afectada TEXT,
    fecha_hora TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);




-- Tokens de autenticación (confirmación y reseteo)
CREATE TABLE IF NOT EXISTS auth_tokens (
    id_token INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(100) NOT NULL,
    token VARCHAR(64) NOT NULL UNIQUE,
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('confirm', 'reset')),
    expiracion TEXT NOT NULL,
    usado BOOLEAN DEFAULT 0
);

-- Índices útiles
CREATE INDEX IF NOT EXISTS idx_auth_tokens_email ON auth_tokens(email);
CREATE INDEX IF NOT EXISTS idx_auth_tokens_token ON auth_tokens(token);