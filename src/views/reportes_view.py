import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ReportesView:
    def __init__(self, parent, controller):
        self.controller = controller
        self.window = ttk.Toplevel(parent)
        self.window.title("Reportes y Estadísticas")
        self.window.geometry("1200x800")
        self.setup_ui()

    def setup_ui(self):
        """Configurar interfaz de reportes"""
        # Panel de control
        self.setup_panel_control()

        # Dashboard con métricas
        self.setup_dashboard()

        # Área de gráficos
        self.setup_area_graficos()

    def setup_panel_control(self):
        """Panel de controles de reportes"""
        control_frame = ttk.LabelFrame(self.window, text="📊 Configuración de Reportes", bootstyle="primary")
        control_frame.pack(fill=X, padx=10, pady=10)

        # Período de análisis
        periodo_frame = ttk.Frame(control_frame)
        periodo_frame.pack(fill=X, padx=5, pady=5)

        ttk.Label(periodo_frame, text="Período:").pack(side=LEFT, padx=(0, 5))
        self.periodo_combo = ttk.Combobox(periodo_frame, width=15,
                                          values=["Último Mes", "Últimos 3 Meses", "Último Año", "Personalizado"])
        self.periodo_combo.pack(side=LEFT, padx=(0, 20))
        self.periodo_combo.set("Último Mes")

        # Tipo de reporte
        ttk.Label(periodo_frame, text="Tipo de Reporte:").pack(side=LEFT, padx=(0, 5))
        self.tipo_reporte_combo = ttk.Combobox(periodo_frame, width=20,
                                               values=["Resumen General", "Por Distrito", "Por Tipo de Accidente",
                                                       "Por Gravedad", "Tendencias Temporales"])
        self.tipo_reporte_combo.pack(side=LEFT, padx=(0, 20))
        self.tipo_reporte_combo.set("Resumen General")

        # Botones
        ttk.Button(periodo_frame, text="📈 Generar Reporte",
                   bootstyle="success", command=self.generar_reporte).pack(side=LEFT, padx=20)
        ttk.Button(periodo_frame, text="💾 Exportar PDF",
                   bootstyle="info", command=self.exportar_pdf).pack(side=LEFT, padx=5)

    def setup_dashboard(self):
        """Dashboard con métricas principales"""
        dashboard_frame = ttk.LabelFrame(self.window, text="📋 Métricas Principales", bootstyle="info")
        dashboard_frame.pack(fill=X, padx=10, pady=(0, 10))

        # Frame para métricas
        metrics_frame = ttk.Frame(dashboard_frame)
        metrics_frame.pack(fill=X, padx=10, pady=10)

        # Total de accidentes
        self.total_accidentes_gauge = ttk.Floodgauge(
            metrics_frame,
            bootstyle="primary",
            mask="Total Accidentes: {}",
            value=0,
            maximum=1000
        )
        self.total_accidentes_gauge.pack(side=LEFT, padx=20)

        # Heridos
        self.heridos_gauge = ttk.Floodgauge(
            metrics_frame,
            bootstyle="warning",
            mask="Total Heridos: {}",
            value=0,
            maximum=500
        )
        self.heridos_gauge.pack(side=LEFT, padx=20)

        # Fallecidos
        self.fallecidos_gauge = ttk.Floodgauge(
            metrics_frame,
            bootstyle="danger",
            mask="Total Fallecidos: {}",
            value=0,
            maximum=100
        )
        self.fallecidos_gauge.pack(side=LEFT, padx=20)

        # Índice de gravedad
        self.gravedad_meter = ttk.Meter(
            metrics_frame,
            metersize=120,
            bootstyle="danger",
            subtext="Índice Gravedad",
            textright="%"
        )
        self.gravedad_meter.pack(side=LEFT, padx=20)

    def setup_area_graficos(self):
        """Área para mostrar gráficos"""
        graficos_frame = ttk.LabelFrame(self.window, text="📊 Gráficos y Análisis", bootstyle="success")
        graficos_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Notebook para diferentes tipos de gráficos
        self.graficos_notebook = ttk.Notebook(graficos_frame, bootstyle="success")
        self.graficos_notebook.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # Frame para gráfico de barras
        self.frame_barras = ttk.Frame(self.graficos_notebook)
        self.graficos_notebook.add(self.frame_barras, text="📊 Por Distrito")

        # Frame para gráfico de líneas
        self.frame_lineas = ttk.Frame(self.graficos_notebook)
        self.graficos_notebook.add(self.frame_lineas, text="📈 Tendencias")

        # Frame para gráfico circular
        self.frame_circular = ttk.Frame(self.graficos_notebook)
        self.graficos_notebook.add(self.frame_circular, text="🥧 Por Tipo")

    def generar_reporte(self):
        """Generar reporte según configuración"""
        periodo = self.periodo_combo.get()
        tipo_reporte = self.tipo_reporte_combo.get()

        # Solicitar datos al controlador
        self.controller.generar_reporte_estadistico(periodo, tipo_reporte)

    def actualizar_metricas(self, datos_metricas):
        """Actualizar métricas del dashboard"""
        self.total_accidentes_gauge.configure(value=datos_metricas['total_accidentes'])
        self.heridos_gauge.configure(value=datos_metricas['total_heridos'])
        self.fallecidos_gauge.configure(value=datos_metricas['total_fallecidos'])

        # Calcular índice de gravedad
        if datos_metricas['total_accidentes'] > 0:
            indice = (datos_metricas['total_fallecidos'] * 100) / datos_metricas['total_accidentes']
            self.gravedad_meter.configure(amountused=min(indice, 100))

    def mostrar_grafico_barras(self, datos, titulo):
        """Mostrar gráfico de barras"""
        # Limpiar frame
        for widget in self.frame_barras.winfo_children():
            widget.destroy()

        # Crear figura matplotlib
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(datos['labels'], datos['values'], color=['#007bff', '#28a745', '#ffc107', '#dc3545'])
        ax.set_title(titulo)
        ax.set_ylabel('Número de Accidentes')
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Integrar con tkinter
        canvas = FigureCanvasTkAgg(fig, self.frame_barras)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)

    def mostrar_grafico_lineas(self, datos, titulo):
        """Mostrar gráfico de líneas para tendencias"""
        # Limpiar frame
        for widget in self.frame_lineas.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(datos['fechas'], datos['valores'], marker='o', linewidth=2, color='#007bff')
        ax.set_title(titulo)
        ax.set_xlabel('Fecha')
        ax.set_ylabel('Número de Accidentes')
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, self.frame_lineas)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)

    def mostrar_grafico_circular(self, datos, titulo):
        """Mostrar gráfico circular"""
        # Limpiar frame
        for widget in self.frame_circular.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(datos['values'], labels=datos['labels'], autopct='%1.1f%%', startangle=90,
               colors=['#007bff', '#28a745', '#ffc107', '#dc3545', '#6f42c1'])
        ax.set_title(titulo)

        canvas = FigureCanvasTkAgg(fig, self.frame_circular)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)

    def exportar_pdf(self):
        """Exportar reporte a PDF"""
        self.controller.exportar_reporte_pdf()