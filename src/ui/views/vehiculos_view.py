from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QDialog,
    QLineEdit, QComboBox, QTextEdit, QFormLayout, QSpinBox
)
from PyQt6.QtCore import Qt
from src.models.vehiculo_model import VehiculoModel


# =====================================================
# 🧱 VISTA PRINCIPAL
# =====================================================
class VehiculosView(QWidget):
    """Vista de gestión de vehículos involucrados"""

    def __init__(self, db, id_accidente=None):
        super().__init__()
        self.db = db
        self.id_accidente = id_accidente
        self.model = VehiculoModel(db)
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # ---------- TOOLBAR ----------
        toolbar = QFrame()
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(15, 10, 15, 10)
        toolbar_layout.setSpacing(10)

        self.btn_agregar = QPushButton("➕ Agregar Vehículo")
        self.btn_agregar.setObjectName("btnSuccess")
        self.btn_agregar.clicked.connect(self.agregar_vehiculo)

        self.btn_editar = QPushButton("✏️ Editar")
        self.btn_editar.clicked.connect(self.editar_vehiculo)

        self.btn_eliminar = QPushButton("🗑️ Eliminar")
        self.btn_eliminar.setObjectName("btnDanger")
        self.btn_eliminar.clicked.connect(self.eliminar_vehiculo)

        for btn in [self.btn_agregar, self.btn_editar, self.btn_eliminar]:
            btn.setMinimumHeight(38)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            toolbar_layout.addWidget(btn)
        toolbar_layout.addStretch()
        layout.addWidget(toolbar)

        # ---------- TABLA ----------
        self.table = QTableWidget()
        self.table.setColumnCount(12)
        self.table.setHorizontalHeaderLabels([
            "ID", "Tipo", "Placa", "Marca", "Modelo", "Año",
            "Color", "Estado", "Motor", "Chasis", "Conductor", "Propietario"
        ])
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

    # =====================================================
    # 📥 CARGA DE DATOS
    # =====================================================
    def load_data(self):
        """Carga vehículos de la base de datos"""
        self.table.setRowCount(0)
        if not self.id_accidente:
            return

        try:
            vehiculos = self.model.obtener_por_accidente(self.id_accidente)
            self.table.setRowCount(len(vehiculos))

            for row, v in enumerate(vehiculos):
                fila = [
                    v["id_vehiculo"],
                    v.get("tipo_vehiculo", ""),
                    v.get("placa", ""),
                    v.get("marca", ""),
                    v.get("modelo", ""),
                    v.get("anio", ""),
                    v.get("color", ""),
                    v.get("estado_vehiculo", ""),
                    v.get("numero_motor", ""),
                    v.get("numero_chasis", ""),
                    f"{v.get('conductor_nombre', '')} {v.get('conductor_apellido', '')}",
                    v.get("propietario_nombre", "")
                ]

                for col, valor in enumerate(fila):
                    item = QTableWidgetItem(str(valor))
                    if col == 7:  # Estado visual
                        estado = str(valor).lower()
                        if "pérdida" in estado:
                            item.setForeground(Qt.GlobalColor.red)
                        elif "grave" in estado:
                            item.setForeground(Qt.GlobalColor.darkYellow)
                        elif "leve" in estado:
                            item.setForeground(Qt.GlobalColor.darkGreen)
                    self.table.setItem(row, col, item)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar vehículos:\n{e}")

    # =====================================================
    # CRUD
    # =====================================================
    def agregar_vehiculo(self):
        if not self.id_accidente:
            QMessageBox.warning(self, "Advertencia", "Debe seleccionar un accidente antes de agregar vehículos.")
            return

        dialog = VehiculoFormDialog(self.model, self.id_accidente, self)
        if dialog.exec():
            self.load_data()

    def editar_vehiculo(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Advertencia", "Seleccione un vehículo para editar.")
            return

        id_vehiculo = int(self.table.item(row, 0).text())
        vehiculo = self.model.obtener_por_id(id_vehiculo)
        if not vehiculo:
            QMessageBox.warning(self, "Error", "No se encontró información del vehículo.")
            return

        dialog = VehiculoFormDialog(self.model, self.id_accidente, self)
        dialog.setWindowTitle("✏️ Editar Vehículo")
        dialog.set_data(vehiculo)

        if dialog.exec():
            datos = dialog.get_data()
            try:
                if self.model.actualizar_vehiculo(id_vehiculo, datos):
                    QMessageBox.information(self, "Éxito", "Vehículo actualizado correctamente.")
                    self.load_data()
                else:
                    QMessageBox.warning(self, "Atención", "No se actualizó ningún registro.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo actualizar: {e}")

    def eliminar_vehiculo(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Advertencia", "Seleccione un vehículo para eliminar.")
            return

        id_vehiculo = int(self.table.item(row, 0).text())
        reply = QMessageBox.question(
            self, "Confirmar eliminación",
            "¿Está seguro de eliminar este vehículo?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                if self.model.eliminar_vehiculo(id_vehiculo):
                    QMessageBox.information(self, "Éxito", "Vehículo eliminado correctamente.")
                    self.load_data()
                else:
                    QMessageBox.warning(self, "Atención", "No se eliminó ningún registro.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar:\n{e}")


# =====================================================
# 🧾 FORMULARIO DE VEHÍCULO
# =====================================================
class VehiculoFormDialog(QDialog):
    """Formulario para agregar o editar vehículo"""

    def __init__(self, model, id_accidente, parent=None):
        super().__init__(parent)
        self.model = model
        self.id_accidente = id_accidente
        self.setWindowTitle("🚗 Registrar Vehículo")
        self.setMinimumWidth(600)
        self.setup_ui()

    # =====================================================
    # 🧱 INTERFAZ
    # =====================================================
    def setup_ui(self):
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        # --- Campos principales ---
        self.cmb_tipo = QComboBox()
        self.cmb_tipo.addItems(["Auto", "Camioneta", "Moto", "Bus", "Camión", "Otro"])
        self.txt_marca = QLineEdit()
        self.txt_modelo = QLineEdit()
        self.txt_placa = QLineEdit()
        self.spn_anio = QSpinBox()
        self.spn_anio.setRange(1980, 2035)
        self.txt_color = QLineEdit()
        self.txt_motor = QLineEdit()
        self.txt_chasis = QLineEdit()
        self.cmb_estado = QComboBox()
        self.cmb_estado.addItems(["Sin daños", "Daños Leves", "Daños Graves", "Pérdida Total"])
        self.txt_danos = QTextEdit()
        self.txt_danos.setPlaceholderText("Describa brevemente los daños visibles en el vehículo...")

        # --- Campos del conductor ---
        self.txt_conductor_dni = QLineEdit()
        self.txt_conductor_dni.setPlaceholderText("Ej: 45678912")

        self.btn_buscar_conductor = QPushButton("🔍 Buscar por DNI")
        self.btn_buscar_conductor.setObjectName("btnSecondary")
        self.btn_buscar_conductor.clicked.connect(self.buscar_conductor)

        dni_layout = QHBoxLayout()
        dni_layout.addWidget(self.txt_conductor_dni)
        dni_layout.addWidget(self.btn_buscar_conductor)

        self.txt_conductor_nombre = QLineEdit()
        self.txt_conductor_apellido = QLineEdit()
        self.txt_conductor_licencia = QLineEdit()
        self.txt_conductor_telefono = QLineEdit()

        # --- Propietario ---
        self.txt_propietario_nombre = QLineEdit()

        # --- Aseguradora ---
        self.txt_aseguradora = QLineEdit()
        self.txt_aseguradora.setPlaceholderText("Nombre de la aseguradora (si aplica)")

        # --- Formulario ---
        form_layout.addRow("Tipo de Vehículo:", self.cmb_tipo)
        form_layout.addRow("Marca:", self.txt_marca)
        form_layout.addRow("Modelo:", self.txt_modelo)
        form_layout.addRow("Placa:", self.txt_placa)
        form_layout.addRow("Año:", self.spn_anio)
        form_layout.addRow("Color:", self.txt_color)
        form_layout.addRow("N° Motor:", self.txt_motor)
        form_layout.addRow("N° Chasis:", self.txt_chasis)
        form_layout.addRow("Estado:", self.cmb_estado)
        form_layout.addRow("Descripción de Daños:", self.txt_danos)
        form_layout.addRow("Aseguradora:", self.txt_aseguradora)

        form_layout.addRow(QLabel("<b>Datos del Conductor</b>"))
        form_layout.addRow("DNI:", dni_layout)
        form_layout.addRow("Nombre:", self.txt_conductor_nombre)
        form_layout.addRow("Apellido:", self.txt_conductor_apellido)
        form_layout.addRow("Licencia:", self.txt_conductor_licencia)
        form_layout.addRow("Teléfono:", self.txt_conductor_telefono)

        form_layout.addRow(QLabel("<b>Propietario</b>"))
        form_layout.addRow("Nombre:", self.txt_propietario_nombre)

        layout.addLayout(form_layout)

        # --- Botones ---
        btn_layout = QHBoxLayout()
        self.btn_guardar = QPushButton("💾 Guardar")
        self.btn_cancelar = QPushButton("❌ Cancelar")

        self.btn_guardar.clicked.connect(self.guardar)
        self.btn_cancelar.clicked.connect(self.reject)

        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_guardar)
        btn_layout.addWidget(self.btn_cancelar)
        layout.addLayout(btn_layout)

    # =====================================================
    # 🔎 BUSCAR CONDUCTOR POR DNI
    # =====================================================
    def buscar_conductor(self):
        """Busca el conductor en la tabla personas por DNI"""
        dni = self.txt_conductor_dni.text().strip()
        if not dni:
            QMessageBox.warning(self, "Advertencia", "Ingrese un DNI antes de buscar.")
            return

        try:
            persona = self.model.buscar_persona_por_dni(dni)
            if not persona:
                QMessageBox.information(self, "Sin resultados", f"No se encontró persona con DNI {dni}.")
                return

            # ✅ Autocompletar campos
            self.txt_conductor_nombre.setText(persona.get("nombre", ""))
            self.txt_conductor_apellido.setText(persona.get("apellido", ""))
            self.txt_conductor_telefono.setText(persona.get("telefono", ""))

            QMessageBox.information(
                self,
                "Persona encontrada",
                f"✅ {persona.get('nombre', '')} {persona.get('apellido', '')} fue cargado correctamente."
            )

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al buscar persona:\n{e}")

    # =====================================================
    # 💾 GUARDAR REGISTRO
    # =====================================================
    def guardar(self):
        """Guardar vehículo en la base de datos"""
        try:
            datos = self.get_data()
            if not datos["marca"] or not datos["placa"]:
                QMessageBox.warning(self, "Campos obligatorios", "Debe ingresar al menos la marca y la placa.")
                return

            self.model.crear_vehiculo(datos)
            QMessageBox.information(self, "Éxito", "Vehículo registrado correctamente.")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo registrar el vehículo:\n{e}")

    # =====================================================
    # 🧩 GET / SET
    # =====================================================
    def get_data(self):
        return {
            "id_accidente": self.id_accidente,
            "tipo_vehiculo": self.cmb_tipo.currentText(),
            "marca": self.txt_marca.text(),
            "modelo": self.txt_modelo.text(),
            "placa": self.txt_placa.text(),
            "anio": self.spn_anio.value(),
            "color": self.txt_color.text(),
            "numero_motor": self.txt_motor.text(),
            "numero_chasis": self.txt_chasis.text(),
            "estado_vehiculo": self.cmb_estado.currentText(),
            "daños_descripcion": self.txt_danos.toPlainText(),
            "conductor_nombre": self.txt_conductor_nombre.text(),
            "conductor_apellido": self.txt_conductor_apellido.text(),
            "conductor_dni": self.txt_conductor_dni.text(),
            "conductor_licencia": self.txt_conductor_licencia.text(),
            "conductor_telefono": self.txt_conductor_telefono.text(),
            "propietario_nombre": self.txt_propietario_nombre.text(),
            "id_aseguradora": None
        }

    def set_data(self, vehiculo):
        """Carga los datos del vehículo existente"""
        self.cmb_tipo.setCurrentText(vehiculo.get("tipo_vehiculo", ""))
        self.txt_marca.setText(vehiculo.get("marca", ""))
        self.txt_modelo.setText(vehiculo.get("modelo", ""))
        self.txt_placa.setText(vehiculo.get("placa", ""))
        self.spn_anio.setValue(vehiculo.get("anio", 2020))
        self.txt_color.setText(vehiculo.get("color", ""))
        self.txt_motor.setText(vehiculo.get("numero_motor", ""))
        self.txt_chasis.setText(vehiculo.get("numero_chasis", ""))
        self.cmb_estado.setCurrentText(vehiculo.get("estado_vehiculo", ""))
        self.txt_danos.setPlainText(vehiculo.get("daños_descripcion", ""))
        self.txt_conductor_nombre.setText(vehiculo.get("conductor_nombre", ""))
        self.txt_conductor_apellido.setText(vehiculo.get("conductor_apellido", ""))
        self.txt_conductor_dni.setText(vehiculo.get("conductor_dni", ""))
        self.txt_conductor_licencia.setText(vehiculo.get("conductor_licencia", ""))
        self.txt_conductor_telefono.setText(vehiculo.get("conductor_telefono", ""))
        self.txt_propietario_nombre.setText(vehiculo.get("propietario_nombre", ""))
