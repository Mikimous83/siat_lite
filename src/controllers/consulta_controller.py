from src.models.accidente_model import AccidenteModel
from src.models.vehiculo_model import VehiculoModel
from src.models.persona_model import PersonaModel
from src.models.database_connection import DatabaseConnection
from src.services.export_service import ExportService


class ConsultaController:
    def __init__(self, parent_window):
        self.parent_window = parent_window

        # ✅ Crear conexión y pasársela a los modelos
        db = DatabaseConnection()
        self.accidente_model = AccidenteModel(db)
        self.vehiculo_model = VehiculoModel(db)
        self.persona_model = PersonaModel(db)

        self.export_service = ExportService()
        self.current_view = None

    def mostrar_ventana_consulta(self):
        """Mostrar ventana de consulta"""
        from src.views.consulta_view import ConsultaView
        self.current_view = ConsultaView(self.parent_window, self)

    def buscar_accidentes(self, filtros):
        """Buscar accidentes con filtros"""
        try:
            filtros_limpios = {k: v for k, v in filtros.items() if v}

            accidentes = self.accidente_model.obtener_accidentes(filtros_limpios)

            accidentes_formato = []
            for acc in accidentes:
                accidentes_formato.append({
                    'id_accidente': acc[0],
                    'numero_caso': acc[1],
                    'fecha': acc[2],
                    'hora': acc[3],
                    'lugar': acc[4],
                    'tipo_accidente': acc[6],
                    'gravedad': acc[7],
                    'heridos': acc[11] or 0,
                    'fallecidos': acc[12] or 0
                })

            if self.current_view:
                self.current_view.mostrar_resultados(accidentes_formato)

            return accidentes_formato

        except Exception as e:
            if self.current_view:
                from ttkbootstrap.dialogs import Messagebox
                Messagebox.show_error("Error", f"Error en búsqueda: {str(e)}")
            return []

    def ver_detalle_accidente(self, id_accidente):
        """Ver detalle completo de un accidente"""
        try:
            accidente = self.accidente_model.obtener_por_id(id_accidente)
            vehiculos = self.vehiculo_model.obtener_vehiculos_por_accidente(id_accidente)
            personas = self.persona_model.obtener_personas_por_accidente(id_accidente)

            from src.views.detalle_accidente_view import DetalleAccidenteView
            DetalleAccidenteView(self.parent_window, accidente, vehiculos, personas)

        except Exception as e:
            from ttkbootstrap.dialogs import Messagebox
            Messagebox.show_error("Error", f"Error al obtener detalle: {str(e)}")

    def editar_accidente(self, id_accidente):
        """Abrir editor de accidente"""
        try:
            from src.controllers.accidente_controller import AccidenteController
            accidente_controller = AccidenteController(self.parent_window)
            accidente_controller.editar_accidente(id_accidente)

        except Exception as e:
            from ttkbootstrap.dialogs import Messagebox
            Messagebox.show_error("Error", f"Error al editar: {str(e)}")

    def exportar_consulta(self):
        """Exportar resultados de consulta"""
        try:
            if not self.current_view or not self.current_view.tree.get_children():
                from ttkbootstrap.dialogs import Messagebox
                Messagebox.show_warning("Advertencia", "No hay datos para exportar")
                return

            datos_export = []
            for item in self.current_view.tree.get_children():
                valores = self.current_view.tree.item(item)['values']
                datos_export.append({
                    'ID': valores[0],
                    'Número Caso': valores[1],
                    'Fecha': valores[2],
                    'Hora': valores[3],
                    'Lugar': valores[4],
                    'Tipo': valores[5],
                    'Gravedad': valores[6],
                    'Heridos': valores[7],
                    'Fallecidos': valores[8]
                })

            archivo = self.export_service.exportar_excel(
                datos_export,
                "consulta_accidentes",
                "Consulta de Accidentes"
            )

            from ttkbootstrap.dialogs import Messagebox
            Messagebox.show_info("Éxito", f"Datos exportados a: {archivo}")

        except Exception as e:
            from ttkbootstrap.dialogs import Messagebox
            Messagebox.show_error("Error", f"Error al exportar: {str(e)}")
