from models.usuario_model import UsuarioModel
from services.validation_service import ValidationService
from ttkbootstrap.dialogs import Messagebox


class UsuarioController:
    def __init__(self):
        self.usuario_model = UsuarioModel()
        self.validation_service = ValidationService()
        self.usuario_actual = None

    def autenticar_usuario(self, email, password):
        """Autenticar usuario"""
        try:
            usuario = self.usuario_model.autenticar_usuario(email, password)
            if usuario:
                self.usuario_actual = {
                    'id': usuario[0],
                    'nombre': usuario[1],
                    'apellido': usuario[2],
                    'nivel_acceso': usuario[3],
                    'nombre_completo': f"{usuario[1]} {usuario[2]}"
                }

                # Actualizar último acceso
                self.usuario_model.actualizar_ultimo_acceso(usuario[0])
                return True
            return False

        except Exception as e:
            print(f"Error en autenticación: {str(e)}")
            return False

    def crear_usuario(self, datos_usuario):
        """Crear nuevo usuario"""
        try:
            # Validar permisos
            if not self._tiene_permisos_admin():
                Messagebox.show_error("Error", "No tiene permisos para crear usuarios")
                return False

            # Validar datos
            errores = self.validation_service.validar_usuario(datos_usuario)
            if errores:
                self._mostrar_errores(errores)
                return False

            # Crear usuario
            id_usuario = self.usuario_model.crear_usuario(datos_usuario)
            Messagebox.show_info("Éxito", f"Usuario creado con ID: {id_usuario}")
            return True

        except Exception as e:
            Messagebox.show_error("Error", f"Error al crear usuario: {str(e)}")
            return False

    def obtener_usuarios_activos(self):
        """Obtener lista de usuarios activos"""
        try:
            return self.usuario_model.obtener_usuarios_activos()
        except Exception as e:
            print(f"Error al obtener usuarios: {str(e)}")
            return []

    def cambiar_password(self, password_actual, password_nueva):
        """Cambiar contraseña del usuario actual"""
        try:
            if not self.usuario_actual:
                return False

            # Verificar contraseña actual
            if not self.usuario_model.verificar_password(self.usuario_actual['id'], password_actual):
                Messagebox.show_error("Error", "Contraseña actual incorrecta")
                return False

            # Validar nueva contraseña
            if len(password_nueva) < 6:
                Messagebox.show_error("Error", "La contraseña debe tener al menos 6 caracteres")
                return False

            # Actualizar contraseña
            if self.usuario_model.actualizar_password(self.usuario_actual['id'], password_nueva):
                Messagebox.show_info("Éxito", "Contraseña actualizada correctamente")
                return True
            return False

        except Exception as e:
            Messagebox.show_error("Error", f"Error al cambiar contraseña: {str(e)}")
            return False

    def _tiene_permisos_admin(self):
        """Verificar si el usuario actual tiene permisos de administrador"""
        return self.usuario_actual and self.usuario_actual['nivel_acceso'] == 'administrador'

    def _mostrar_errores(self, errores):
        """Mostrar errores de validación"""
        mensaje = "\\n".join(errores)
        Messagebox.show_error("Errores de Validación", mensaje)