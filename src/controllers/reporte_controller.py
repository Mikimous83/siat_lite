from src.models.accidente_model import AccidenteModel
from src.models.persona_model import PersonaModel
from src.services.export_service import ExportService
from datetime import datetime, timedelta
import calendar


class ReporteController:
    def __init__(self, parent_window):
        self.parent_window = parent_window
        self.accidente_model = AccidenteModel()
        self.persona_model = PersonaModel()
        self.export_service = ExportService()
        self.current_view = None

    def mostrar_ventana_reportes(self):
        """Mostrar ventana de reportes"""
        from src.views.reportes_view import ReportesView
        self.current_view = ReportesView(self.parent_window, self)

        # Cargar datos iniciales
        self.generar_reporte_estadistico("Último Mes", "Resumen General")

    def generar_reporte_estadistico(self, periodo, tipo_reporte):
        """Generar reporte estadístico"""
        try:
            # Determinar rango de fechas
            fecha_desde, fecha_hasta = self._calcular_periodo(periodo)

            # Obtener métricas generales
            metricas = self._obtener_metricas_generales(fecha_desde, fecha_hasta)

            # Actualizar dashboard
            if self.current_view:
                self.current_view.actualizar_metricas(metricas)

            # Generar gráficos según tipo de reporte
            if tipo_reporte == "Por Distrito":
                self._generar_reporte_distritos(fecha_desde, fecha_hasta)
            elif tipo_reporte == "Por Tipo de Accidente":
                self._generar_reporte_tipos(fecha_desde, fecha_hasta)
            elif tipo_reporte == "Tendencias Temporales":
                self._generar_reporte_tendencias(fecha_desde, fecha_hasta)
            else:  # Resumen General
                self._generar_reporte_general(fecha_desde, fecha_hasta)

        except Exception as e:
            if self.current_view:
                from ttkbootstrap.dialogs import Messagebox
                Messagebox.show_error("Error", f"Error al generar reporte: {str(e)}")

    def _calcular_periodo(self, periodo):
        """Calcular fechas desde y hasta según período"""
        hoy = datetime.now().date()

        if periodo == "Último Mes":
            fecha_desde = hoy - timedelta(days=30)
        elif periodo == "Últimos 3 Meses":
            fecha_desde = hoy - timedelta(days=90)
        elif periodo == "Último Año":
            fecha_desde = hoy - timedelta(days=365)
        else:  # Personalizado - por ahora usar último mes
            fecha_desde = hoy - timedelta(days=30)

        return fecha_desde, hoy

    def _obtener_metricas_generales(self, fecha_desde, fecha_hasta):
        """Obtener métricas generales del período"""
        filtros = {
            'fecha_desde': fecha_desde.strftime('%Y-%m-%d'),
            'fecha_hasta': fecha_hasta.strftime('%Y-%m-%d')
        }

        # Obtener accidentes del período
        accidentes = self.accidente_model.obtener_accidentes(filtros)

        total_accidentes = len(accidentes)
        total_heridos = sum(acc[11] or 0 for acc in accidentes)
        total_fallecidos = sum(acc[12] or 0 for acc in accidentes)

        return {
            'total_accidentes': total_accidentes,
            'total_heridos': total_heridos,
            'total_fallecidos': total_fallecidos
        }

    def _generar_reporte_distritos(self, fecha_desde, fecha_hasta):
        """Generar reporte por distritos"""
        try:
            datos_distritos = self.accidente_model.obtener_estadisticas_por_distrito(
                fecha_desde.strftime('%Y-%m-%d'),
                fecha_hasta.strftime('%Y-%m-%d')
            )

            datos_grafico = {
                'labels': [d[0] for d in datos_distritos],
                'values': [d[1] for d in datos_distritos]
            }

            if self.current_view:
                self.current_view.mostrar_grafico_barras(
                    datos_grafico,
                    f"Accidentes por Distrito ({fecha_desde} - {fecha_hasta})"
                )

        except Exception as e:
            print(f"Error en reporte por distritos: {str(e)}")

    def _generar_reporte_tipos(self, fecha_desde, fecha_hasta):
        """Generar reporte por tipos de accidente"""
        try:
            datos_tipos = self.accidente_model.obtener_estadisticas_por_tipo(
                fecha_desde.strftime('%Y-%m-%d'),
                fecha_hasta.strftime('%Y-%m-%d')
            )

            datos_grafico = {
                'labels': [d[0] for d in datos_tipos],
                'values': [d[1] for d in datos_tipos]
            }

            if self.current_view:
                self.current_view.mostrar_grafico_circular(
                    datos_grafico,
                    f"Distribución por Tipo de Accidente ({fecha_desde} - {fecha_hasta})"
                )

        except Exception as e:
            print(f"Error en reporte por tipos: {str(e)}")

    def _generar_reporte_tendencias(self, fecha_desde, fecha_hasta):
        """Generar reporte de tendencias temporales"""
        try:
            datos_tendencias = self.accidente_model.obtener_tendencias_temporales(
                fecha_desde.strftime('%Y-%m-%d'),
                fecha_hasta.strftime('%Y-%m-%d')
            )

            datos_grafico = {
                'fechas': [d[0] for d in datos_tendencias],
                'valores': [d[1] for d in datos_tendencias]
            }

            if self.current_view:
                self.current_view.mostrar_grafico_lineas(
                    datos_grafico,
                    f"Tendencia Temporal de Accidentes ({fecha_desde} - {fecha_hasta})"
                )

        except Exception as e:
            print(f"Error en reporte de tendencias: {str(e)}")

    def _generar_reporte_general(self, fecha_desde, fecha_hasta):
        """Generar reporte general (múltiples gráficos)"""
        self._generar_reporte_distritos(fecha_desde, fecha_hasta)
        self._generar_reporte_tipos(fecha_desde, fecha_hasta)
        self._generar_reporte_tendencias(fecha_desde, fecha_hasta)

    def exportar_reporte_pdf(self):
        """Exportar reporte completo a PDF"""
        try:
            # Obtener datos actuales
            archivo_pdf = self.export_service.generar_reporte_pdf(
                "reporte_accidentes",
                "Reporte Estadístico de Accidentes de Tránsito"
            )

            if self.current_view:
                from ttkbootstrap.dialogs import Messagebox
                Messagebox.show_info("Éxito", f"Reporte exportado a: {archivo_pdf}")

        except Exception as e:
            print(f"Error en reporte de tendencias: {str(e)}")