import pandas as pd
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch


class ExportService:
    def __init__(self):
        self.export_path = "exports"
        self._ensure_export_directory()

    def _ensure_export_directory(self):
        """Crear directorio de exportaciones"""
        os.makedirs(self.export_path, exist_ok=True)

    def exportar_excel(self, datos, nombre_archivo, titulo_hoja="Datos"):
        """Exportar datos a Excel"""
        try:
            # Generar nombre único
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_completo = f"{nombre_archivo}_{timestamp}.xlsx"
            ruta_archivo = os.path.join(self.export_path, nombre_completo)

            # Crear DataFrame
            df = pd.DataFrame(datos)

            # Exportar a Excel con formato
            with pd.ExcelWriter(ruta_archivo, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=titulo_hoja, index=False)

                # Obtener workbook y worksheet para formato
                workbook = writer.book
                worksheet = writer.sheets[titulo_hoja]

                # Ajustar ancho de columnas
                for column in worksheet.columns:
                    max_length = 0
                    column = [cell for cell in column]
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = (max_length + 2) * 1.2
                    worksheet.column_dimensions[column[0].column_letter].width = adjusted_width

            return ruta_archivo

        except Exception as e:
            raise Exception(f"Error al exportar Excel: {str(e)}")

    def exportar_csv(self, datos, nombre_archivo):
        """Exportar datos a CSV"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_completo = f"{nombre_archivo}_{timestamp}.csv"
            ruta_archivo = os.path.join(self.export_path, nombre_completo)

            df = pd.DataFrame(datos)
            df.to_csv(ruta_archivo, index=False, encoding='utf-8')

            return ruta_archivo

        except Exception as e:
            raise Exception(f"Error al exportar CSV: {str(e)}")

    def generar_reporte_pdf(self, nombre_archivo, titulo):
        """Generar reporte en PDF"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_completo = f"{nombre_archivo}_{timestamp}.pdf"
            ruta_archivo = os.path.join(self.export_path, nombre_completo)

            # Crear documento PDF
            doc = SimpleDocTemplate(ruta_archivo, pagesize=A4)
            story = []

            # Estilos
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                spaceAfter=30,
                alignment=1  # Centrado
            )

            # Título
            story.append(Paragraph(titulo, title_style))
            story.append(Spacer(1, 12))

            # Fecha de generación
            fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
            story.append(Paragraph(f"Generado el: {fecha_actual}", styles['Normal']))
            story.append(Spacer(1, 20))

            # Construir PDF
            doc.build(story)

            return ruta_archivo

        except Exception as e:
            raise Exception(f"Error al generar PDF: {str(e)}")