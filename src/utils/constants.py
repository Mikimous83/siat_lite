"""
Constantes del sistema SIATLITE
"""

# ========== ESTADOS DE CASO ==========
ESTADOS_CASO = [
    'Abierto',
    'En Proceso',
    'Cerrado',
    'Archivado'
]

# ========== TIPOS DE PERSONA ==========
TIPOS_PERSONA = [
    'Conductor',
    'Pasajero',
    'Peatón',
    'Testigo',
    'Otro'
]

# ========== ESTADOS DE SALUD ==========
ESTADOS_SALUD = [
    'Ileso',
    'Herido Leve',
    'Herido Grave',
    'Crítico',
    'Fallecido'
]

# ========== CONDICIONES CLIMÁTICAS ==========
CONDICIONES_CLIMATICAS = [
    'Soleado',
    'Nublado',
    'Lluvioso',
    'Neblina',
    'Tormenta',
    'Viento Fuerte',
    'Granizo'
]

# ========== ILUMINACIÓN ==========
NIVELES_ILUMINACION = [
    'Día',
    'Noche con iluminación',
    'Noche sin iluminación',
    'Amanecer/Atardecer'
]

# ========== SEÑALIZACIÓN ==========
ESTADOS_SENALIZACION = [
    'Adecuada',
    'Deficiente',
    'Inexistente',
    'En mal estado'
]

# ========== SEXO ==========
SEXOS = ['M', 'F', 'Otro']

# ========== ROLES DE USUARIO ==========
ROLES = [
    'Administrador',
    'Operador',
    'Consultor',
    'Inspector'
]

# ========== FORMATOS DE EXPORTACIÓN ==========
FORMATOS_EXPORTACION = [
    'PDF',
    'Excel',
    'CSV',
    'JSON'
]

# ========== TIPOS DE VÍA ==========
TIPOS_VIA = [
    'Avenida',
    'Jirón',
    'Calle',
    'Carretera',
    'Autopista',
    'Camino',
    'Pasaje',
    'Malecón'
]

# ========== TIPOS DE VEHÍCULO ==========
TIPOS_VEHICULO = [
    'Auto',
    'Camioneta',
    'Moto',
    'Mototaxi',
    'Bus',
    'Microbus',
    'Camión',
    'Tráiler',
    'Bicicleta',
    'Otro'
]

# ========== TIPOS DE ACCIDENTE ==========
TIPOS_ACCIDENTE = [
    'Colisión',
    'Choque',
    'Atropello',
    'Volcadura',
    'Despiste',
    'Caída de Pasajero',
    'Incendio',
    'Otro'
]

# ========== NIVELES DE GRAVEDAD ==========
NIVELES_GRAVEDAD = [
    'Leve',
    'Moderado',
    'Grave'
]

# ========== COLORES PARA GRÁFICOS ==========
COLORES_GRAFICOS = {
    'primary': '#2A82DA',
    'success': '#28A745',
    'danger': '#DC3545',
    'warning': '#FFC107',
    'info': '#17A2B8',
    'secondary': '#6C757D',
    'dark': '#343A40',
    'light': '#F8F9FA'
}

# ========== COLORES DEL TEMA ==========
COLORS = {
    'primary': '#2A82DA',
    'primary_hover': '#1E5FA8',
    'success': '#28A745',
    'danger': '#DC3545',
    'warning': '#FFC107',
    'info': '#17A2B8',
    'dark': '#1E1E28',
    'dark_light': '#282838',
    'background': '#2A2A3A',
    'card': '#32323F',
    'text': '#DCDCDC',
    'text_secondary': '#9A9A9A',
    'border': '#404050',
}

# ========== MENSAJES DEL SISTEMA ==========
MENSAJES = {
    # Mensajes de éxito
    'exito_crear': '✓ Registro creado exitosamente',
    'exito_actualizar': '✓ Registro actualizado exitosamente',
    'exito_eliminar': '✓ Registro eliminado exitosamente',
    'exito_guardar': '✓ Datos guardados correctamente',
    'exito_exportar': '✓ Exportación completada',
    'exito_importar': '✓ Importación completada',

    # Mensajes de error
    'error_crear': '✗ Error al crear el registro',
    'error_actualizar': '✗ Error al actualizar el registro',
    'error_eliminar': '✗ Error al eliminar el registro',
    'error_guardar': '✗ Error al guardar los datos',
    'error_cargar': '✗ Error al cargar los datos',
    'error_exportar': '✗ Error en la exportación',
    'error_importar': '✗ Error en la importación',
    'error_conexion': '✗ Error de conexión a la base de datos',
    'error_permisos': '✗ No tiene permisos para realizar esta acción',

    # Mensajes de confirmación
    'confirmar_eliminar': '¿Está seguro de eliminar este registro?\n\nEsta acción no se puede deshacer.',
    'confirmar_salir': '¿Está seguro de salir?\n\nLos cambios no guardados se perderán.',
    'confirmar_cancelar': '¿Está seguro de cancelar?\n\nLos cambios no guardados se perderán.',

    # Mensajes de advertencia
    'sin_seleccion': 'Debe seleccionar un registro',
    'sin_datos': 'No hay datos para mostrar',
    'campos_obligatorios': 'Complete todos los campos obligatorios',
    'datos_invalidos': 'Los datos ingresados no son válidos',
    'registro_duplicado': 'Ya existe un registro con estos datos',

    # Mensajes informativos
    'cargando': 'Cargando datos...',
    'procesando': 'Procesando...',
    'guardando': 'Guardando cambios...',
    'buscando': 'Buscando...',
    'exportando': 'Exportando datos...',
    'generando_reporte': 'Generando reporte...',
}

# ========== LÍMITES DEL SISTEMA ==========
LIMITES = {
    'max_caracteres_texto': 255,
    'max_caracteres_descripcion': 1000,
    'max_archivos_adjuntos': 10,
    'max_tamaño_archivo_mb': 10,
    'max_registros_exportacion': 10000,
    'timeout_consulta_segundos': 30,
}

# ========== CONFIGURACIÓN DE PAGINACIÓN ==========
PAGINACION = {
    'registros_por_pagina': 50,
    'opciones_registros': [10, 25, 50, 100, 200],
}

# ========== PATRONES DE VALIDACIÓN ==========
PATRONES = {
    'dni': r'^\d{8}$',
    'placa_antigua': r'^[A-Z]{3}-\d{3}$',
    'placa_nueva': r'^[A-Z]{3}-\d{4}$',
    'telefono_fijo': r'^\d{7}$',
    'telefono_celular': r'^\d{9}$',
    'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    'fecha': r'^\d{4}-\d{2}-\d{2}$',
    'hora': r'^\d{2}:\d{2}$',
}

# ========== RANGOS VÁLIDOS ==========
RANGOS = {
    'latitud': (-90, 90),
    'longitud': (-180, 180),
    'edad': (0, 120),
    'año_vehiculo': (1900, 2100),
}

# ========== DEPARTAMENTOS DEL PERÚ ==========
DEPARTAMENTOS = [
    'Amazonas', 'Áncash', 'Apurímac', 'Arequipa', 'Ayacucho',
    'Cajamarca', 'Callao', 'Cusco', 'Huancavelica', 'Huánuco',
    'Ica', 'Junín', 'La Libertad', 'Lambayeque', 'Lima',
    'Loreto', 'Madre de Dios', 'Moquegua', 'Pasco', 'Piura',
    'Puno', 'San Martín', 'Tacna', 'Tumbes', 'Ucayali'
]

# ========== MARCAS DE VEHÍCULOS COMUNES ==========
MARCAS_VEHICULOS = [
    'Toyota', 'Hyundai', 'Nissan', 'Chevrolet', 'Kia',
    'Honda', 'Mazda', 'Volkswagen', 'Ford', 'Suzuki',
    'Mitsubishi', 'Subaru', 'Peugeot', 'Renault', 'Fiat',
    'Mercedes-Benz', 'BMW', 'Audi', 'Volvo', 'JAC',
    'Great Wall', 'Chery', 'MG', 'Haval', 'Otro'
]

# ========== ASEGURADORAS PRINCIPALES ==========
ASEGURADORAS = [
    'Rímac Seguros',
    'Pacífico Seguros',
    'La Positiva Seguros',
    'Mapfre Perú',
    'HDI Seguros',
    'Chubb Seguros',
    'Cardif',
    'Interseguro',
    'Otro'
]

# ========== CÓDIGOS DE ERROR ==========
CODIGOS_ERROR = {
    1000: 'Error general del sistema',
    1001: 'Error de base de datos',
    1002: 'Error de validación',
    1003: 'Error de permisos',
    1004: 'Registro no encontrado',
    1005: 'Operación no permitida',
    2000: 'Error de conexión',
    2001: 'Timeout de consulta',
    3000: 'Error de archivo',
    3001: 'Formato de archivo no válido',
    3002: 'Tamaño de archivo excedido',
}

# ========== CONFIGURACIÓN DE REPORTES ==========
CONFIG_REPORTES = {
    'titulo_empresa': 'SIATLITE',
    'subtitulo_empresa': 'Sistema de Información de Accidentes de Tránsito',
    'pie_pagina': 'Generado por SIATLITE © 2025',
    'logo_path': 'resources/images/logo.png',
    'margen_superior': 2.5,
    'margen_inferior': 2.5,
    'margen_izquierdo': 2.5,
    'margen_derecho': 2.5,
}

# ========== URLs Y CONTACTOS ==========
CONTACTOS = {
    'email_soporte': 'soporte@siatlite.com',
    'telefono_soporte': '(01) 555-0123',
    'sitio_web': 'https://siatlite.com',
    'manual_usuario': 'https://siatlite.com/manual',
}

# ========== VERSIÓN DEL SISTEMA ==========
VERSION = {
    'numero': '1.0.0',
    'fecha': '2025-10-23',
    'nombre_codigo': 'Genesis',
}

# ========== CONFIGURACIÓN DE BACKUP ==========
CONFIG_BACKUP = {
    'directorio': 'backups',
    'prefijo_archivo': 'siatlite_backup',
    'extension': '.db',
    'mantener_ultimos': 10,
    'backup_automatico': True,
    'frecuencia_horas': 24,
}

# ========== ESTADÍSTICAS PREDETERMINADAS ==========
STATS_DEFAULT = {
    'total_accidentes': 0,
    'mes_actual': 0,
    'graves': 0,
    'pendientes': 0,
    'total_heridos': 0,
    'total_fallecidos': 0,
}

# ========== TEXTO DE AYUDA ==========
AYUDA = {
    'accidentes': 'Gestione los accidentes de tránsito registrados en el sistema',
    'personas': 'Administre las personas involucradas en los accidentes',
    'vehiculos': 'Controle los vehículos involucrados en accidentes',
    'reportes': 'Genere reportes y estadísticas del sistema',
    'configuracion': 'Configure los parámetros del sistema',
}

# ========== ATAJOS DE TECLADO ==========
SHORTCUTS = {
    'nuevo': 'Ctrl+N',
    'guardar': 'Ctrl+S',
    'buscar': 'Ctrl+F',
    'eliminar': 'Del',
    'actualizar': 'F5',
    'salir': 'Alt+F4',
}

# ========== EXPORTAR TODO ==========
__all__ = [
    'ESTADOS_CASO',
    'TIPOS_PERSONA',
    'ESTADOS_SALUD',
    'CONDICIONES_CLIMATICAS',
    'NIVELES_ILUMINACION',
    'ESTADOS_SENALIZACION',
    'SEXOS',
    'ROLES',
    'FORMATOS_EXPORTACION',
    'TIPOS_VIA',
    'TIPOS_VEHICULO',
    'TIPOS_ACCIDENTE',
    'NIVELES_GRAVEDAD',
    'COLORES_GRAFICOS',
    'COLORS',
    'MENSAJES',
    'LIMITES',
    'PAGINACION',
    'PATRONES',
    'RANGOS',
    'DEPARTAMENTOS',
    'MARCAS_VEHICULOS',
    'ASEGURADORAS',
    'CODIGOS_ERROR',
    'CONFIG_REPORTES',
    'CONTACTOS',
    'VERSION',
    'CONFIG_BACKUP',
    'STATS_DEFAULT',
    'AYUDA',
    'SHORTCUTS',
]