import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox


class AccidenteFormView:
    def __init__(self, parent, controller):
        self.controller = controller
        self.window = ttk.Toplevel(parent)
        self.window.title("Registro de Accidente")
        self.window.geometry("900x700")
        self.setup_form()

    def setup_form(self):
        """Configurar formulario de registro"""
        # Notebook con pestañas
        self.notebook = ttk.Notebook(self.window, bootstyle="primary")
        self.notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Pestaña 1: Datos básicos
        self.setup_datos_basicos()

        # Pestaña 2: Ubicación
        self.setup_ubicacion()

        # Pestaña 3: Vehículos
        self.setup_vehiculos()

        # Pestaña 4: Personas
        self.setup_personas()

        # Botones de acción
        self.setup_action_buttons()

    def setup_datos_basicos(self):
        """Pestaña de datos básicos"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📋 Datos Básicos")

        # Fecha
        ttk.Label(frame, text="Fecha del Accidente:").pack(anchor=W, pady=5)
        self.fecha_entry = ttk.DateEntry(frame, bootstyle="success")
        self.fecha_entry.pack(fill=X, pady=(0, 10))

        # Hora
        ttk.Label(frame, text="Hora:").pack(anchor=W, pady=5)
        self.hora_entry = ttk.Entry(frame)
        self.hora_entry.pack(fill=X, pady=(0, 10))

        # Tipo de accidente
        ttk.Label(frame, text="Tipo de Accidente:").pack(anchor=W, pady=5)
        self.tipo_combo = ttk.Combobox(frame,
                                       values=["Colisión", "Atropello", "Volcadura", "Choque"],
                                       bootstyle="info")
        self.tipo_combo.pack(fill=X, pady=(0, 10))

        # Gravedad
        ttk.Label(frame, text="Gravedad:").pack(anchor=W, pady=5)
        self.gravedad_combo = ttk.Combobox(frame,
                                           values=["Leve", "Grave", "Muy Grave", "Fatal"],
                                           bootstyle="danger")
        self.gravedad_combo.pack(fill=X, pady=(0, 10))

    def setup_ubicacion(self):
        """Pestaña de ubicación"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📍 Ubicación")

        ttk.Label(frame, text="Lugar del Accidente:").pack(anchor=W, pady=5)
        self.lugar_entry = ttk.Entry(frame)
        self.lugar_entry.pack(fill=X, pady=(0, 10))

        ttk.Label(frame, text="Distrito:").pack(anchor=W, pady=5)
        self.distrito_entry = ttk.Entry(frame)
        self.distrito_entry.pack(fill=X, pady=(0, 10))

    def setup_vehiculos(self):
        """Pestaña de vehículos"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🚗 Vehículos")

        # Aquí va la lista de vehículos y botones para agregar/editar
        pass

    def setup_personas(self):
        """Pestaña de personas"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="👥 Personas")

        # Aquí va la gestión de personas involucradas
        pass

    def setup_action_buttons(self):
        """Botones de guardar/cancelar"""
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill=X, padx=10, pady=10)

        ttk.Button(button_frame,
                   text="💾 Guardar",
                   bootstyle="success",
                   command=self.guardar_accidente).pack(side=RIGHT, padx=5)

        ttk.Button(button_frame,
                   text="❌ Cancelar",
                   bootstyle="danger-outline",
                   command=self.window.destroy).pack(side=RIGHT, padx=5)

    def guardar_accidente(self):
        """Recopilar datos y enviar al controlador"""
        datos = self.recopilar_datos()
        if self.validar_datos(datos):
            self.controller.guardar_accidente(datos)

    def recopilar_datos(self):
        """Recopilar todos los datos del formulario"""
        return {
            'fecha': self.fecha_entry.entry.get(),
            'hora': self.hora_entry.get(),
            'lugar': self.lugar_entry.get(),
            'distrito': self.distrito_entry.get(),
            'tipo_accidente': self.tipo_combo.get(),
            'gravedad': self.gravedad_combo.get()
        }

    def validar_datos(self, datos):
        """Validar datos antes de enviar"""
        if not datos['fecha']:
            Messagebox.show_error("Error", "La fecha es obligatoria")
            return False
        if not datos['lugar']:
            Messagebox.show_error("Error", "El lugar es obligatorio")
            return False
        return True