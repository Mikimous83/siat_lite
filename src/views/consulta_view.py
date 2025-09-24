import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox


class ConsultaView:
    def __init__(self, parent, controller):
        self.controller = controller
        self.window = ttk.Toplevel(parent)
        self.window.title("Consulta de Accidentes")
        self.window.geometry("1000x700")
        self.setup_ui()

    def setup_ui(self):
        """Configurar interfaz de consulta"""
        # Panel de filtros
        self.setup_filtros()

        # Tabla de resultados
        self.setup_tabla_resultados()

        # Botones de acción
        self.setup_botones()

    def setup_filtros(self):
        """Panel de filtros de búsqueda"""
        filtros_frame = ttk.LabelFrame(self.window, text="🔍 Filtros de Búsqueda", bootstyle="primary")
        filtros_frame.pack(fill=X, padx=10, pady=10)

        # Fila 1: Fechas
        fecha_frame = ttk.Frame(filtros_frame)
        fecha_frame.pack(fill=X, padx=5, pady=5)

        ttk.Label(fecha_frame, text="Fecha Desde:").pack(side=LEFT, padx=(0, 5))
        self.fecha_desde = ttk.DateEntry(fecha_frame, bootstyle="info")
        self.fecha_desde.pack(side=LEFT, padx=(0, 20))

        ttk.Label(fecha_frame, text="Fecha Hasta:").pack(side=LEFT, padx=(0, 5))
        self.fecha_hasta = ttk.DateEntry(fecha_frame, bootstyle="info")
        self.fecha_hasta.pack(side=LEFT, padx=(0, 20))

        # Fila 2: Ubicación y tipo
        ubicacion_frame = ttk.Frame(filtros_frame)
        ubicacion_frame.pack(fill=X, padx=5, pady=5)

        ttk.Label(ubicacion_frame, text="Lugar:").pack(side=LEFT, padx=(0, 5))
        self.lugar_entry = ttk.Entry(ubicacion_frame, width=20)
        self.lugar_entry.pack(side=LEFT, padx=(0, 20))

        ttk.Label(ubicacion_frame, text="Distrito:").pack(side=LEFT, padx=(0, 5))
        self.distrito_combo = ttk.Combobox(ubicacion_frame, width=15,
                                           values=["Trujillo", "La Esperanza", "El Porvenir", "Florencia de Mora"])
        self.distrito_combo.pack(side=LEFT, padx=(0, 20))

        ttk.Label(ubicacion_frame, text="Tipo:").pack(side=LEFT, padx=(0, 5))
        self.tipo_combo = ttk.Combobox(ubicacion_frame, width=15,
                                       values=["Colisión", "Atropello", "Volcadura", "Choque"])
        self.tipo_combo.pack(side=LEFT, padx=(0, 20))

        # Botones de filtro
        botones_frame = ttk.Frame(filtros_frame)
        botones_frame.pack(fill=X, padx=5, pady=5)

        ttk.Button(botones_frame, text="🔍 Buscar",
                   bootstyle="primary", command=self.buscar_accidentes).pack(side=LEFT, padx=5)
        ttk.Button(botones_frame, text="🗑️ Limpiar",
                   bootstyle="secondary-outline", command=self.limpiar_filtros).pack(side=LEFT, padx=5)

    def setup_tabla_resultados(self):
        """Tabla de resultados con scroll"""
        tabla_frame = ttk.LabelFrame(self.window, text="📋 Resultados", bootstyle="info")
        tabla_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Configurar columnas
        columnas = ('ID', 'Número Caso', 'Fecha', 'Hora', 'Lugar', 'Tipo', 'Gravedad', 'Heridos', 'Fallecidos')
        self.tree = ttk.Treeview(tabla_frame, columns=columnas, show='headings', height=15)

        # Configurar headers
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=CENTER)

        # Scrollbars
        scrollbar_v = ttk.Scrollbar(tabla_frame, orient=VERTICAL, command=self.tree.yview)
        scrollbar_h = ttk.Scrollbar(tabla_frame, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

        # Pack elementos
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar_v.pack(side=RIGHT, fill=Y)
        scrollbar_h.pack(side=BOTTOM, fill=X)

        # Evento doble click
        self.tree.bind('<Double-1>', self.ver_detalle_accidente)

    def setup_botones(self):
        """Botones de acción"""
        botones_frame = ttk.Frame(self.window)
        botones_frame.pack(fill=X, padx=10, pady=10)

        ttk.Button(botones_frame, text="👁️ Ver Detalle",
                   bootstyle="info", command=self.ver_detalle_seleccionado).pack(side=LEFT, padx=5)
        ttk.Button(botones_frame, text="✏️ Editar",
                   bootstyle="warning", command=self.editar_seleccionado).pack(side=LEFT, padx=5)
        ttk.Button(botones_frame, text="📊 Exportar",
                   bootstyle="success", command=self.exportar_resultados).pack(side=LEFT, padx=5)
        ttk.Button(botones_frame, text="❌ Cerrar",
                   bootstyle="danger-outline", command=self.window.destroy).pack(side=RIGHT, padx=5)

    def buscar_accidentes(self):
        """Ejecutar búsqueda con filtros"""
        filtros = self.recopilar_filtros()
        self.controller.buscar_accidentes(filtros)

    def recopilar_filtros(self):
        """Recopilar filtros del formulario"""
        return {
            'fecha_desde': self.fecha_desde.entry.get() if self.fecha_desde.entry.get() else None,
            'fecha_hasta': self.fecha_hasta.entry.get() if self.fecha_hasta.entry.get() else None,
            'lugar': self.lugar_entry.get() if self.lugar_entry.get() else None,
            'distrito': self.distrito_combo.get() if self.distrito_combo.get() else None,
            'tipo_accidente': self.tipo_combo.get() if self.tipo_combo.get() else None
        }

    def mostrar_resultados(self, accidentes):
        """Mostrar resultados en la tabla"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Agregar resultados
        for accidente in accidentes:
            self.tree.insert('', END, values=(
                accidente['id_accidente'],
                accidente['numero_caso'],
                accidente['fecha'],
                accidente['hora'],
                accidente['lugar'][:30] + '...' if len(accidente['lugar']) > 30 else accidente['lugar'],
                accidente['tipo_accidente'],
                accidente['gravedad'],
                accidente['heridos'],
                accidente['fallecidos']
            ))

    def limpiar_filtros(self):
        """Limpiar todos los filtros"""
        self.fecha_desde.entry.delete(0, END)
        self.fecha_hasta.entry.delete(0, END)
        self.lugar_entry.delete(0, END)
        self.distrito_combo.set('')
        self.tipo_combo.set('')

        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

    def ver_detalle_accidente(self, event):
        """Ver detalle al hacer doble click"""
        self.ver_detalle_seleccionado()

    def ver_detalle_seleccionado(self):
        """Ver detalle del accidente seleccionado"""
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            id_accidente = item['values'][0]
            self.controller.ver_detalle_accidente(id_accidente)
        else:
            Messagebox.show_warning("Advertencia", "Seleccione un accidente")

    def editar_seleccionado(self):
        """Editar el accidente seleccionado"""
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            id_accidente = item['values'][0]
            self.controller.editar_accidente(id_accidente)
        else:
            Messagebox.show_warning("Advertencia", "Seleccione un accidente")

    def exportar_resultados(self):
        """Exportar resultados a Excel/CSV"""
        if not self.tree.get_children():
            Messagebox.show_warning("Advertencia", "No hay resultados para exportar")
            return

        self.controller.exportar_consulta()