from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit, QDialog,
    QFormLayout, QComboBox, QDateEdit, QTimeEdit, QTextEdit, QSpinBox,
    QDoubleSpinBox, QMessageBox, QDialogButtonBox, QTabWidget
)
from PyQt6.QtCore import Qt, QDate, QTime
from datetime import datetime
from src.models.database_connection import DatabaseConnection as Database
from src.models.accidente_model import AccidenteModel


class AccidentesView(QWidget):
    """Vista principal de gestión de accidentes"""

    def __init__(self):
        super().__init__()
        self.db = Database().connect()
        self.model = AccidenteModel(self.db)
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # ===== Toolbar =====
        toolbar = QFrame()
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setSpacing(10)

        btn_nuevo = QPushButton("➕ Nuevo Accidente")
        btn_nuevo.setObjectName("btnSuccess")
        btn_nuevo.clicked.connect(self.abrir_formulario_nuevo)

        btn_editar = QPushButton("✏️ Editar")
        btn_editar.clicked.connect(self.editar_accidente)

        btn_eliminar = QPushButton("🗑️ Eliminar")
        btn_eliminar.setObjectName("btnDanger")
        btn_eliminar.clicked.connect(self.eliminar_accidente)

        toolbar_layout.addWidget(btn_nuevo)
        toolbar_layout.addWidget(btn_editar)
        toolbar_layout.addWidget(btn_eliminar)
        toolbar_layout.addStretch()
        layout.addWidget(toolbar)

        # ===== Tabla =====
        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "ID", "N° Caso", "Fecha", "Hora", "Lugar", "Tipo",
            "Gravedad", "Heridos", "Fallecidos", "Estado"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

    # =====================================================
    # CRUD PRINCIPAL
    # =====================================================
    def load_data(self):
        """Carga los registros de accidentes y aplica colores según gravedad y estado"""
        try:
            registros = self.model.obtener_todos()
            self.table.setRowCount(len(registros))

            for i, r in enumerate(registros):
                datos = [
                    r.get("id_accidente", ""),
                    r.get("numero_caso", ""),
                    r.get("fecha", ""),
                    r.get("hora", ""),
                    r.get("lugar", ""),
                    r.get("tipo_accidente", ""),
                    r.get("nivel_gravedad", ""),
                    r.get("heridos", ""),
                    r.get("fallecidos", ""),
                    r.get("estado_caso", "")
                ]

                for j, val in enumerate(datos):
                    item = QTableWidgetItem(str(val))

                    # --- Colorear GRAVEDAD ---
                    if j == 6:  # columna gravedad
                        gravedad = str(val).lower()
                        if "leve" in gravedad:
                            item.setForeground(Qt.GlobalColor.green)
                        elif "moderado" in gravedad:
                            item.setForeground(Qt.GlobalColor.darkYellow)
                        elif "grave" in gravedad:
                            item.setForeground(Qt.GlobalColor.red)
                        item.setFont(item.font())  # para mantener estilo

                    # --- Colorear ESTADO ---
                    elif j == 9:  # columna estado
                        estado = str(val).lower()
                        if "abierto" in estado:
                            item.setForeground(Qt.GlobalColor.blue)
                        elif "en proceso" in estado:
                            item.setForeground(Qt.GlobalColor.darkYellow)
                        elif "cerrado" in estado:
                            item.setForeground(Qt.GlobalColor.darkGray)

                    self.table.setItem(i, j, item)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar datos:\n{e}")

    def abrir_formulario_nuevo(self):
        dialog = AccidenteDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted and dialog.result_data:
            try:
                self.model.insertar(dialog.result_data)
                QMessageBox.information(self, "Éxito", "Accidente registrado correctamente.")
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo registrar el accidente:\n{e}")

    def editar_accidente(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Advertencia", "Seleccione un accidente para editar")
            return

        id_accidente = int(self.table.item(row, 0).text())
        registros = self.model.obtener_todos()
        registro = next((r for r in registros if r["id_accidente"] == id_accidente), None)
        if not registro:
            QMessageBox.critical(self, "Error", "No se encontró el registro.")
            return

        dialog = AccidenteDialog(self, edit_mode=True, data=registro)
        if dialog.exec() == QDialog.DialogCode.Accepted and dialog.result_data:
            try:
                self.model.actualizar(id_accidente, dialog.result_data)
                QMessageBox.information(self, "Éxito", "Accidente actualizado correctamente.")
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo actualizar:\n{e}")

    def eliminar_accidente(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Advertencia", "Seleccione un accidente para eliminar")
            return

        id_accidente = int(self.table.item(row, 0).text())
        reply = QMessageBox.question(
            self, "Confirmar Eliminación",
            "¿Está seguro de eliminar este accidente?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.model.eliminar(id_accidente)
                QMessageBox.information(self, "Éxito", "Accidente eliminado correctamente.")
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar:\n{e}")


# =====================================================
# DIALOGO DE FORMULARIO
# =====================================================
class AccidenteDialog(QDialog):
    """Formulario para crear o editar accidentes"""

    def __init__(self, parent=None, edit_mode=False, data=None):
        super().__init__(parent)
        self.edit_mode = edit_mode
        self.model = getattr(parent, "model", None)
        self.data = data or {}
        self.result_data = None
        self.setWindowTitle("✏️ Editar Accidente" if edit_mode else "➕ Nuevo Accidente")
        self.setMinimumSize(700, 500)
        self.setup_ui()

        if self.edit_mode:
            numero = self.data.get("numero_caso", "")
            self.txt_numero_caso.setText(numero)
            self.txt_numero_caso.setDisabled(True)
        else:
            numero_auto = self.model.generar_numero_caso() if self.model else "ACC-AUTO"
            self.txt_numero_caso.setText(numero_auto)
            self.txt_numero_caso.setDisabled(True)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        tabs = QTabWidget()
        tabs.addTab(self.create_general_tab(), "📋 Datos Generales")
        tabs.addTab(self.create_ubicacion_tab(), "📍 Ubicación y Condiciones")
        layout.addWidget(tabs)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.validar_y_guardar)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def create_general_tab(self):
        widget = QWidget()
        form = QFormLayout(widget)

        self.txt_numero_caso = QLineEdit()
        self.date_fecha = QDateEdit(QDate.currentDate())
        self.date_fecha.setCalendarPopup(True)
        self.time_hora = QTimeEdit(QTime.currentTime())
        self.cmb_tipo = QComboBox()
        self.cmb_tipo.addItems(["1 - Colisión", "2 - Choque", "3 - Atropello"])
        self.cmb_gravedad = QComboBox()
        self.cmb_gravedad.addItems(["1 - Leve", "2 - Moderado", "3 - Grave"])
        self.spin_heridos = QSpinBox(); self.spin_heridos.setRange(0, 100)
        self.spin_fallecidos = QSpinBox(); self.spin_fallecidos.setRange(0, 100)
        self.txt_descripcion = QTextEdit()

        if self.edit_mode and self.data:
            self.date_fecha.setDate(QDate.fromString(self.data.get("fecha", ""), "yyyy-MM-dd"))
            self.time_hora.setTime(QTime.fromString(self.data.get("hora", ""), "HH:mm"))
            self.spin_heridos.setValue(int(self.data.get("heridos", 0)))
            self.spin_fallecidos.setValue(int(self.data.get("fallecidos", 0)))
            self.txt_descripcion.setPlainText(self.data.get("descripcion", ""))

        form.addRow("Número de Caso:", self.txt_numero_caso)
        form.addRow("Fecha:", self.date_fecha)
        form.addRow("Hora:", self.time_hora)
        form.addRow("Tipo (ID):", self.cmb_tipo)
        form.addRow("Gravedad (ID):", self.cmb_gravedad)
        form.addRow("Heridos:", self.spin_heridos)
        form.addRow("Fallecidos:", self.spin_fallecidos)
        form.addRow("Descripción:", self.txt_descripcion)
        return widget

    def create_ubicacion_tab(self):
        widget = QWidget()
        form = QFormLayout(widget)
        self.txt_lugar = QLineEdit()
        self.spin_latitud = QDoubleSpinBox(); self.spin_latitud.setRange(-90, 90); self.spin_latitud.setDecimals(8)
        self.spin_longitud = QDoubleSpinBox(); self.spin_longitud.setRange(-180, 180); self.spin_longitud.setDecimals(8)
        self.cmb_tipo_via = QComboBox(); self.cmb_tipo_via.addItems(["1 - Avenida", "2 - Carretera", "3 - Calle"])
        self.cmb_clima = QComboBox(); self.cmb_clima.addItems(["Soleado", "Nublado", "Lluvioso", "Neblina"])
        self.cmb_iluminacion = QComboBox(); self.cmb_iluminacion.addItems(["Día", "Noche con iluminación", "Noche sin iluminación"])
        self.cmb_senalizacion = QComboBox(); self.cmb_senalizacion.addItems(["Adecuada", "Deficiente", "Inexistente"])

        if self.edit_mode and self.data:
            self.txt_lugar.setText(self.data.get("lugar", ""))
            self.spin_latitud.setValue(float(self.data.get("latitud", 0)))
            self.spin_longitud.setValue(float(self.data.get("longitud", 0)))

        form.addRow("Lugar:", self.txt_lugar)
        form.addRow("Latitud:", self.spin_latitud)
        form.addRow("Longitud:", self.spin_longitud)
        form.addRow("Tipo de Vía (ID):", self.cmb_tipo_via)
        form.addRow("Condiciones Climáticas:", self.cmb_clima)
        form.addRow("Iluminación:", self.cmb_iluminacion)
        form.addRow("Señalización:", self.cmb_senalizacion)
        return widget

    def validar_y_guardar(self):
        if not self.txt_lugar.text().strip():
            QMessageBox.warning(self, "Advertencia", "Debe ingresar el lugar del accidente.")
            return
        self.result_data = self.get_data()  # ✅ guarda datos antes de cerrar
        self.accept()

    def get_data(self):
        id_tipo = int(self.cmb_tipo.currentText().split(" - ")[0])
        id_gravedad = int(self.cmb_gravedad.currentText().split(" - ")[0])
        id_tipo_via = int(self.cmb_tipo_via.currentText().split(" - ")[0])

        return {
            "numero_caso": self.txt_numero_caso.text(),
            "fecha": self.date_fecha.date().toString("yyyy-MM-dd"),
            "hora": self.time_hora.time().toString("HH:mm"),
            "lugar": self.txt_lugar.text(),
            "latitud": self.spin_latitud.value(),
            "longitud": self.spin_longitud.value(),
            "id_tipo_accidente": id_tipo,
            "id_comisaria": 1,
            "id_usuario_registro": 1,
            "id_gravedad": id_gravedad,
            "descripcion": self.txt_descripcion.toPlainText(),
            "condiciones_climaticas": self.cmb_clima.currentText(),
            "id_tipo_via": id_tipo_via,
            "iluminacion": self.cmb_iluminacion.currentText(),
            "señalizacion": self.cmb_senalizacion.currentText(),
            "estado_caso": "Abierto",
            "heridos": self.spin_heridos.value(),
            "fallecidos": self.spin_fallecidos.value(),
            "vehiculos_involucrados": 0,
            "croquis_url": "",
            "fotos_url": "",
            "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "fecha_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
