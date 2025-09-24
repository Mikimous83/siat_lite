# src/views/accidente_form_view.py
import uuid
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import tkinter as tk


class AccidenteFormView:
    def __init__(self, parent, controller):
        self.controller = controller
        self.window = ttk.Toplevel(parent)
        self.window.title("Registro de Accidente")
        self.window.geometry("900x700")

        # Estructuras para almacenar temporalmente personas/vehículos
        # Usamos mapas local_id -> datos para facilitar editar/eliminar
        self.personas_map = {}
        self.vehiculos_map = {}

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
        # DateEntry de ttkbootstrap
        self.fecha_entry = ttk.DateEntry(frame, bootstyle="success")
        self.fecha_entry.pack(fill=X, pady=(0, 10))

        # Hora
        ttk.Label(frame, text="Hora (HH:MM):").pack(anchor=W, pady=5)
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

        # Descripción (campo adicional no destructivo)
        ttk.Label(frame, text="Descripción / Observaciones:").pack(anchor=W, pady=5)
        self.descripcion_text = tk.Text(frame, height=4)
        self.descripcion_text.pack(fill=X, pady=(0, 10))

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

        ttk.Label(frame, text="Provincia:").pack(anchor=W, pady=5)
        self.provincia_entry = ttk.Entry(frame)
        self.provincia_entry.pack(fill=X, pady=(0, 10))

        ttk.Label(frame, text="Departamento:").pack(anchor=W, pady=5)
        self.departamento_entry = ttk.Entry(frame)
        self.departamento_entry.pack(fill=X, pady=(0, 10))

    def setup_vehiculos(self):
        """Pestaña de vehículos: Treeview + botones + acciones"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🚗 Vehículos")

        # Treeview para listar vehículos añadidos temporalmente
        columnas = ("Placa", "Tipo", "Marca", "Modelo", "Conductor")
        self.tree_vehiculos = ttk.Treeview(frame, columns=columnas, show="headings", height=8)
        for col in columnas:
            self.tree_vehiculos.heading(col, text=col)
            self.tree_vehiculos.column(col, width=120, anchor='w')
        self.tree_vehiculos.pack(fill=X, pady=10, padx=10)

        # Botones para gestionar vehículos
        frame_btn = ttk.Frame(frame)
        frame_btn.pack(fill=X, padx=10, pady=5)

        ttk.Button(frame_btn, text="➕ Agregar", bootstyle="success",
                   command=self._open_add_vehiculo).pack(side=LEFT, padx=5)
        ttk.Button(frame_btn, text="✏️ Editar", bootstyle="warning",
                   command=self._open_edit_vehiculo).pack(side=LEFT, padx=5)
        ttk.Button(frame_btn, text="❌ Eliminar", bootstyle="danger-outline",
                   command=self._eliminar_vehiculo).pack(side=LEFT, padx=5)

    def setup_personas(self):
        """Pestaña de personas: Treeview + botones + acciones"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="👥 Personas")

        columnas = ("Tipo", "Nombre Completo", "DNI", "Edad", "Estado Salud")
        self.tree_personas = ttk.Treeview(frame, columns=columnas, show="headings", height=8)
        for col in columnas:
            self.tree_personas.heading(col, text=col)
            self.tree_personas.column(col, width=140, anchor='w')
        self.tree_personas.pack(fill=X, pady=10, padx=10)

        # Botones para gestionar personas
        frame_btn = ttk.Frame(frame)
        frame_btn.pack(fill=X, padx=10, pady=5)

        ttk.Button(frame_btn, text="➕ Agregar", bootstyle="success",
                   command=self._open_add_persona).pack(side=LEFT, padx=5)
        ttk.Button(frame_btn, text="✏️ Editar", bootstyle="warning",
                   command=self._open_edit_persona).pack(side=LEFT, padx=5)
        ttk.Button(frame_btn, text="❌ Eliminar", bootstyle="danger-outline",
                   command=self._eliminar_persona).pack(side=LEFT, padx=5)

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

    # ----------------------------
    # Métodos para abrir diálogos
    # ----------------------------
    def _open_add_persona(self):
        PersonaDialog(self.window, on_save=self._on_persona_saved)

    def _open_edit_persona(self):
        sel = self.tree_personas.selection()
        if not sel:
            Messagebox.show_error("Error", "Seleccione una persona para editar.")
            return
        local_id = sel[0]
        data = self.personas_map.get(local_id)
        if not data:
            Messagebox.show_error("Error", "Persona no encontrada.")
            return
        PersonaDialog(self.window, on_save=self._on_persona_saved, data=data)

    def _open_add_vehiculo(self):
        VehiculoDialog(self.window, on_save=self._on_vehiculo_saved)

    def _open_edit_vehiculo(self):
        sel = self.tree_vehiculos.selection()
        if not sel:
            Messagebox.show_error("Error", "Seleccione un vehículo para editar.")
            return
        local_id = sel[0]
        data = self.vehiculos_map.get(local_id)
        if not data:
            Messagebox.show_error("Error", "Vehículo no encontrado.")
            return
        VehiculoDialog(self.window, on_save=self._on_vehiculo_saved, data=data)

    # ----------------------------
    # Callbacks de guardado local
    # ----------------------------
    def _on_persona_saved(self, persona):
        """Callback cuando se agrega/edita una persona desde el dialog."""
        # persona debe ser dict; si viene con local_id -> edición
        local_id = persona.get('local_id') or uuid.uuid4().hex
        persona['local_id'] = local_id
        # guardar/actualizar en mapa
        self.personas_map[local_id] = persona

        # actualizar treeview (si existe el iid, editar; si no, insertar)
        if local_id in self.tree_personas.get_children():
            # actualizar fila
            self.tree_personas.item(local_id, values=(
                persona.get('tipo_persona', ''),
                f"{persona.get('nombre','')} {persona.get('apellido','')}".strip(),
                persona.get('dni',''),
                persona.get('edad',''),
                persona.get('estado_salud','')
            ))
        else:
            # insertar nueva fila con iid = local_id
            self.tree_personas.insert('', 'end', iid=local_id, values=(
                persona.get('tipo_persona', ''),
                f"{persona.get('nombre','')} {persona.get('apellido','')}".strip(),
                persona.get('dni',''),
                persona.get('edad',''),
                persona.get('estado_salud','')
            ))

    def _on_vehiculo_saved(self, vehiculo):
        """Callback cuando se agrega/edita un vehículo desde el dialog."""
        local_id = vehiculo.get('local_id') or uuid.uuid4().hex
        vehiculo['local_id'] = local_id
        self.vehiculos_map[local_id] = vehiculo

        if local_id in self.tree_vehiculos.get_children():
            self.tree_vehiculos.item(local_id, values=(
                vehiculo.get('placa',''),
                vehiculo.get('tipo_vehiculo',''),
                vehiculo.get('marca',''),
                vehiculo.get('modelo',''),
                vehiculo.get('conductor_nombre','')
            ))
        else:
            self.tree_vehiculos.insert('', 'end', iid=local_id, values=(
                vehiculo.get('placa',''),
                vehiculo.get('tipo_vehiculo',''),
                vehiculo.get('marca',''),
                vehiculo.get('modelo',''),
                vehiculo.get('conductor_nombre','')
            ))

    # ----------------------------
    # Eliminar elementos
    # ----------------------------
    def _eliminar_persona(self):
        sel = self.tree_personas.selection()
        if not sel:
            Messagebox.show_error("Error", "Seleccione una persona para eliminar.")
            return
        local_id = sel[0]
        confirm = Messagebox.yesno("Confirmar", "¿Eliminar la persona seleccionada?")
        if confirm:
            try:
                del self.personas_map[local_id]
            except KeyError:
                pass
            self.tree_personas.delete(local_id)

    def _eliminar_vehiculo(self):
        sel = self.tree_vehiculos.selection()
        if not sel:
            Messagebox.show_error("Error", "Seleccione un vehículo para eliminar.")
            return
        local_id = sel[0]
        confirm = Messagebox.yesno("Confirmar", "¿Eliminar el vehículo seleccionado?")
        if confirm:
            try:
                del self.vehiculos_map[local_id]
            except KeyError:
                pass
            self.tree_vehiculos.delete(local_id)

    # ----------------------------
    # Recopilar datos y validar
    # ----------------------------
    def recopilar_datos(self):
        """Recopilar todos los datos del formulario (incluye personas/vehículos)"""
        datos = {
            'fecha': self.fecha_entry.entry.get() if hasattr(self.fecha_entry, 'entry') else self.fecha_entry.get(),
            'hora': self.hora_entry.get(),
            'lugar': self.lugar_entry.get(),
            'distrito': self.distrito_entry.get(),
            'provincia': getattr(self, 'provincia_entry', ttk.Entry()).get() if hasattr(self, 'provincia_entry') else '',
            'departamento': getattr(self, 'departamento_entry', ttk.Entry()).get() if hasattr(self, 'departamento_entry') else '',
            'tipo_accidente': self.tipo_combo.get(),
            'gravedad': self.gravedad_combo.get(),
            'descripcion': self.descripcion_text.get("1.0", "end").strip(),
            # pasar listas de personas/vehiculos para que el controller las procese
            'personas': list(self.personas_map.values()),
            'vehiculos': list(self.vehiculos_map.values())
        }

        # conteos básicos
        datos['vehiculos_involucrados'] = len(datos['vehiculos'])
        datos['heridos'] = sum(1 for p in datos['personas'] if p.get('tipo_persona') == 'herido')
        datos['fallecidos'] = sum(1 for p in datos['personas'] if p.get('tipo_persona') == 'fallecido')

        return datos

    def validar_datos(self, datos):
        """Validar datos antes de enviar"""
        if not datos['fecha']:
            Messagebox.show_error("Error", "La fecha es obligatoria")
            return False
        if not datos['lugar']:
            Messagebox.show_error("Error", "El lugar es obligatorio")
            return False
        return True

    def guardar_accidente(self):
        """Recopilar datos y enviar al controlador"""
        datos = self.recopilar_datos()
        if not self.validar_datos(datos):
            return
        # Llamada al controlador (tu controller puede procesar people/vehicles)
        try:
            resultado = self.controller.guardar_accidente(datos)
            # El controlador, en tu implementación, muestra mensajes; aquí manejamos cierre si devolvió True
            if resultado:
                # Si el controller ya destruye la view (como en tu controlador original), no repetir
                try:
                    self.window.destroy()
                except:
                    pass
            else:
                # Guardado no exitoso; el controlador ya muestra error normalmente
                pass
        except Exception as e:
            Messagebox.show_error("Error", f"Error al guardar accidente: {e}")


# =================================================
# Dialog para Persona (Agregar / Editar)
# =================================================
class PersonaDialog:
    def __init__(self, parent, on_save, data=None):
        """
        parent: ventana padre
        on_save: callback que recibe dict persona
        data: dict con datos (si es edición)
        """
        self.on_save = on_save
        self.data = data or {}
        self.top = ttk.Toplevel(parent)
        self.top.title("Agregar Persona" if not data else "Editar Persona")
        self.top.grab_set()
        self._build()

        if data:
            self._fill_with_data(data)

    def _build(self):
        frm = ttk.Frame(self.top, padding=10)
        frm.pack(fill=BOTH, expand=True)

        # Tipo de persona
        ttk.Label(frm, text="Tipo (rol):").grid(row=0, column=0, sticky=W, pady=3)
        self.tipo_cb = ttk.Combobox(frm, values=["conductor", "pasajero", "peatón", "herido", "fallecido", "testigo"])
        self.tipo_cb.grid(row=0, column=1, sticky=EW, pady=3)

        # Nombre / Apellido
        ttk.Label(frm, text="Nombre:").grid(row=1, column=0, sticky=W, pady=3)
        self.nombre_e = ttk.Entry(frm)
        self.nombre_e.grid(row=1, column=1, sticky=EW, pady=3)

        ttk.Label(frm, text="Apellido:").grid(row=2, column=0, sticky=W, pady=3)
        self.apellido_e = ttk.Entry(frm)
        self.apellido_e.grid(row=2, column=1, sticky=EW, pady=3)

        # DNI / Edad
        ttk.Label(frm, text="DNI:").grid(row=3, column=0, sticky=W, pady=3)
        self.dni_e = ttk.Entry(frm)
        self.dni_e.grid(row=3, column=1, sticky=EW, pady=3)

        ttk.Label(frm, text="Edad:").grid(row=4, column=0, sticky=W, pady=3)
        self.edad_e = ttk.Spinbox(frm, from_=0, to=120)
        self.edad_e.grid(row=4, column=1, sticky=EW, pady=3)

        # Estado salud / Hospital
        ttk.Label(frm, text="Estado salud:").grid(row=5, column=0, sticky=W, pady=3)
        self.estado_salud_e = ttk.Entry(frm)
        self.estado_salud_e.grid(row=5, column=1, sticky=EW, pady=3)

        ttk.Label(frm, text="Hospital (si aplica):").grid(row=6, column=0, sticky=W, pady=3)
        self.hospital_e = ttk.Entry(frm)
        self.hospital_e.grid(row=6, column=1, sticky=EW, pady=3)

        # Lesiones (texto)
        ttk.Label(frm, text="Lesiones / Observaciones:").grid(row=7, column=0, sticky=NW, pady=3)
        self.lesiones_t = tk.Text(frm, height=4)
        self.lesiones_t.grid(row=7, column=1, sticky=EW, pady=3)

        # Botones
        btn_frm = ttk.Frame(frm)
        btn_frm.grid(row=8, column=0, columnspan=2, pady=8)
        ttk.Button(btn_frm, text="Guardar", bootstyle="success", command=self._guardar).pack(side=LEFT, padx=5)
        ttk.Button(btn_frm, text="Cancelar", bootstyle="danger-outline", command=self.top.destroy).pack(side=LEFT, padx=5)

        # make columns expand
        frm.columnconfigure(1, weight=1)

    def _fill_with_data(self, data):
        self.tipo_cb.set(data.get('tipo_persona', ''))
        self.nombre_e.insert(0, data.get('nombre', ''))
        self.apellido_e.insert(0, data.get('apellido', ''))
        self.dni_e.insert(0, data.get('dni', ''))
        if data.get('edad') is not None:
            self.edad_e.delete(0, 'end')
            self.edad_e.insert(0, str(data.get('edad')))
        self.estado_salud_e.insert(0, data.get('estado_salud', ''))
        self.hospital_e.insert(0, data.get('hospital_traslado', ''))
        self.lesiones_t.insert("1.0", data.get('lesiones_descripcion', ''))
        # mantener local_id si viene (para edición)
        if data.get('local_id'):
            self.data['local_id'] = data['local_id']

    def _guardar(self):
        # Validaciones mínimas
        tipo = self.tipo_cb.get().strip()
        nombre = self.nombre_e.get().strip()
        apellido = self.apellido_e.get().strip()

        if not tipo or not nombre:
            Messagebox.show_error("Error", "Tipo y Nombre son obligatorios.")
            return

        persona = {
            'local_id': self.data.get('local_id'),
            'tipo_persona': tipo,
            'nombre': nombre,
            'apellido': apellido,
            'dni': self.dni_e.get().strip(),
            'edad': self.edad_e.get().strip(),
            'estado_salud': self.estado_salud_e.get().strip(),
            'hospital_traslado': self.hospital_e.get().strip(),
            'lesiones_descripcion': self.lesiones_t.get("1.0", "end").strip()
        }

        # llamar callback
        try:
            self.on_save(persona)
            self.top.destroy()
        except Exception as e:
            Messagebox.show_error("Error", f"No se pudo guardar la persona: {e}")


# =================================================
# Dialog para Vehículo (Agregar / Editar)
# =================================================
class VehiculoDialog:
    def __init__(self, parent, on_save, data=None):
        self.on_save = on_save
        self.data = data or {}
        self.top = ttk.Toplevel(parent)
        self.top.title("Agregar Vehículo" if not data else "Editar Vehículo")
        self.top.grab_set()
        self._build()

        if data:
            self._fill_with_data(data)

    def _build(self):
        frm = ttk.Frame(self.top, padding=10)
        frm.pack(fill=BOTH, expand=True)

        ttk.Label(frm, text="Placa:").grid(row=0, column=0, sticky=W, pady=3)
        self.placa_e = ttk.Entry(frm)
        self.placa_e.grid(row=0, column=1, sticky=EW, pady=3)

        ttk.Label(frm, text="Tipo vehículo:").grid(row=1, column=0, sticky=W, pady=3)
        self.tipo_cb = ttk.Combobox(frm, values=["Automóvil", "Camioneta", "Camión", "Motocicleta", "Bicicleta", "Otro"])
        self.tipo_cb.grid(row=1, column=1, sticky=EW, pady=3)

        ttk.Label(frm, text="Marca:").grid(row=2, column=0, sticky=W, pady=3)
        self.marca_e = ttk.Entry(frm)
        self.marca_e.grid(row=2, column=1, sticky=EW, pady=3)

        ttk.Label(frm, text="Modelo:").grid(row=3, column=0, sticky=W, pady=3)
        self.modelo_e = ttk.Entry(frm)
        self.modelo_e.grid(row=3, column=1, sticky=EW, pady=3)

        ttk.Label(frm, text="Color:").grid(row=4, column=0, sticky=W, pady=3)
        self.color_e = ttk.Entry(frm)
        self.color_e.grid(row=4, column=1, sticky=EW, pady=3)

        ttk.Label(frm, text="Conductor (Nombre):").grid(row=5, column=0, sticky=W, pady=3)
        self.conductor_e = ttk.Entry(frm)
        self.conductor_e.grid(row=5, column=1, sticky=EW, pady=3)

        ttk.Label(frm, text="DNI Conductor:").grid(row=6, column=0, sticky=W, pady=3)
        self.conductor_dni_e = ttk.Entry(frm)
        self.conductor_dni_e.grid(row=6, column=1, sticky=EW, pady=3)

        # Botones
        btn_frm = ttk.Frame(frm)
        btn_frm.grid(row=7, column=0, columnspan=2, pady=8)
        ttk.Button(btn_frm, text="Guardar", bootstyle="success", command=self._guardar).pack(side=LEFT, padx=5)
        ttk.Button(btn_frm, text="Cancelar", bootstyle="danger-outline", command=self.top.destroy).pack(side=LEFT, padx=5)

        frm.columnconfigure(1, weight=1)

    def _fill_with_data(self, data):
        self.placa_e.insert(0, data.get('placa', ''))
        self.tipo_cb.set(data.get('tipo_vehiculo', ''))
        self.marca_e.insert(0, data.get('marca', ''))
        self.modelo_e.insert(0, data.get('modelo', ''))
        self.color_e.insert(0, data.get('color', ''))
        self.conductor_e.insert(0, data.get('conductor_nombre', ''))
        self.conductor_dni_e.insert(0, data.get('conductor_dni', ''))
        if data.get('local_id'):
            self.data['local_id'] = data['local_id']

    def _guardar(self):
        placa = self.placa_e.get().strip()
        if not placa:
            Messagebox.show_error("Error", "La placa es obligatoria.")
            return

        vehiculo = {
            'local_id': self.data.get('local_id'),
            'placa': placa,
            'tipo_vehiculo': self.tipo_cb.get().strip(),
            'marca': self.marca_e.get().strip(),
            'modelo': self.modelo_e.get().strip(),
            'color': self.color_e.get().strip(),
            'conductor_nombre': self.conductor_e.get().strip(),
            'conductor_dni': self.conductor_dni_e.get().strip()
        }

        try:
            self.on_save(vehiculo)
            self.top.destroy()
        except Exception as e:
            Messagebox.show_error("Error", f"No se pudo guardar el vehículo: {e}")
