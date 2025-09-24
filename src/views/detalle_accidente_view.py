# src/views/detalle_accidente_view.py
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class DetalleAccidenteView(ttk.Toplevel):
    def __init__(self, parent, accidente, vehiculos, personas):
        super().__init__(parent)
        self.title(f"Detalle Accidente #{accidente[0]}")
        self.geometry("800x600")
        self.resizable(True, True)

        # Notebook con pestañas
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Pestañas
        self.setup_accidente(accidente)
        self.setup_vehiculos(vehiculos)
        self.setup_personas(personas)

        # Botón cerrar
        ttk.Button(self, text="❌ Cerrar", bootstyle="danger", command=self.destroy).pack(pady=10)

    # ------------------- pestaña accidente -------------------
    def setup_accidente(self, accidente):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📄 Datos del Accidente")

        labels = [
            ("ID", accidente[0]),
            ("Número de Caso", accidente[1]),
            ("Fecha", accidente[2]),
            ("Hora", accidente[3]),
            ("Lugar", accidente[4]),
            ("Distrito", accidente[5]),
            ("Tipo", accidente[6]),
            ("Gravedad", accidente[7]),
            ("Descripción", accidente[8] if len(accidente) > 8 else ""),
            ("Heridos", accidente[11] if len(accidente) > 11 else 0),
            ("Fallecidos", accidente[12] if len(accidente) > 12 else 0),
        ]

        for i, (campo, valor) in enumerate(labels):
            ttk.Label(frame, text=f"{campo}:", bootstyle="inverse-primary").grid(row=i, column=0, sticky=W, padx=5, pady=5)
            ttk.Label(frame, text=str(valor)).grid(row=i, column=1, sticky=W, padx=5, pady=5)

    # ------------------- pestaña vehículos -------------------
    def setup_vehiculos(self, vehiculos):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🚗 Vehículos")

        columnas = ("Placa", "Marca", "Modelo", "Color", "Conductor")
        tree = ttk.Treeview(frame, columns=columnas, show="headings", height=8)
        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor=CENTER)
        tree.pack(fill=BOTH, expand=True, pady=10)

        for v in vehiculos:
            tree.insert("", "end", values=v)

    # ------------------- pestaña personas -------------------
    def setup_personas(self, personas):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="👥 Personas")

        columnas = ("DNI", "Nombre", "Edad", "Rol", "Estado")
        tree = ttk.Treeview(frame, columns=columnas, show="headings", height=8)
        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor=CENTER)
        tree.pack(fill=BOTH, expand=True, pady=10)

        for p in personas:
            tree.insert("", "end", values=p)
