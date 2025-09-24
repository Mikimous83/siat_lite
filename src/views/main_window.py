import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class MainWindow:
    def __init__(self, controller):
        self.controller = controller
        self.root = ttk.Window(themename="superhero")
        self.root.title("SIAT-Lite v1.0 - Sistema de Accidentes de Tránsito")
        self.root.geometry("1200x800")
        self.setup_ui()

    def setup_ui(self):
        """Configurar la interfaz principal"""
        # Header
        header_frame = ttk.Frame(self.root, bootstyle="primary")
        header_frame.pack(fill=X, pady=(0, 10))

        ttk.Label(header_frame,
                  text="🚗 SIAT-Lite",
                  font=("Arial", 24, "bold"),
                  bootstyle="inverse-primary").pack(pady=10)

        # Navigation
        nav_frame = ttk.Frame(self.root)
        nav_frame.pack(fill=X, pady=(0, 20))

        ttk.Button(nav_frame,
                   text="📝 Registrar Accidente",
                   bootstyle="success-outline",
                   command=self.controller.abrir_registro_accidente).pack(side=LEFT, padx=5)

        ttk.Button(nav_frame,
                   text="🔍 Consultar Accidentes",
                   bootstyle="info-outline",
                   command=self.controller.abrir_consulta).pack(side=LEFT, padx=5)

        ttk.Button(nav_frame,
                   text="📊 Reportes",
                   bootstyle="warning-outline",
                   command=self.controller.abrir_reportes).pack(side=LEFT, padx=5)

        # Dashboard con estadísticas
        self.setup_dashboard()

    def setup_dashboard(self):
        """Panel de estadísticas rápidas"""
        stats_frame = ttk.LabelFrame(self.root, text="📈 Estadísticas del Mes", bootstyle="primary")
        stats_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Aquí van los widgets de estadísticas
        pass

    def run(self):
        self.root.mainloop()