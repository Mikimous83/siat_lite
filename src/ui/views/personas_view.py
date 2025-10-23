from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
)
from PyQt6.QtCore import Qt
from src.models.persona_model import PersonaModel
from src.models.database_connection import DatabaseConnection as Database


class PersonasView(QWidget):
    """Vista principal para gestión de personas"""

    def __init__(self, db_connection):
        super().__init__()
        self.db = db_connection
        self.model = PersonaModel(self.db)
        self.setup_ui()
        self.load_data()

    # =====================================================
    # 🧩 INTERFAZ
    # =====================================================
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Barra de herramientas
        toolbar = QFrame()
        tb_layout = QHBoxLayout(toolbar)
        btn_agregar = QPushButton("➕ Agregar")
        btn_agregar.setMinimumHeight(36)
        btn_agregar.clicked.connect(self.agregar_persona)
        btn_eliminar = QPushButton("🗑️ Eliminar")
        btn_eliminar.setMinimumHeight(36)
        btn_eliminar.clicked.connect(self.eliminar_persona)
        tb_layout.addWidget(btn_agregar)
        tb_layout.addWidget(btn_eliminar)
        tb_layout.addStretch()
        layout.addWidget(toolbar)

        # Tabla
        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "ID", "N° Caso", "Tipo", "Nombre", "Apellido",
            "DNI", "Edad", "Sexo", "Estado", "Teléfono"
        ])
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

    # =====================================================
    # 📦 CARGA DE DATOS
    # =====================================================
    def load_data(self):
        """Carga las personas desde la base de datos"""
        try:
            personas = self.model.obtener_personas()
            self.table.setRowCount(len(personas))

            for i, p in enumerate(personas):
                valores = list(p.values())
                for j, val in enumerate(valores):
                    item = QTableWidgetItem(str(val))
                    if j == 8:  # Estado salud
                        estado = str(val).lower()
                        if "grave" in estado:
                            item.setForeground(Qt.GlobalColor.red)
                        elif "leve" in estado:
                            item.setForeground(Qt.GlobalColor.darkYellow)
                        elif "fallecido" in estado:
                            item.setForeground(Qt.GlobalColor.darkRed)
                        else:
                            item.setForeground(Qt.GlobalColor.darkGreen)
                    self.table.setItem(i, j, item)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar personas:\n{e}")

    # =====================================================
    # 🧭 ACCIONES
    # =====================================================
    def agregar_persona(self):
        dialog = PersonaFormDialog(self.db)
        if dialog.exec():
            self.load_data()

    def eliminar_persona(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Seleccione", "Seleccione una persona para eliminar")
            return

        id_persona = int(self.table.item(row, 0).text())
        confirm = QMessageBox.question(
            self,
            "Confirmar",
            "¿Eliminar esta persona?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            if self.model.eliminar_persona(id_persona):
                QMessageBox.information(self, "Éxito", "Persona eliminada correctamente")
                self.load_data()

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QPushButton, QMessageBox
)
from src.models.persona_model import PersonaModel


class PersonaFormDialog(QDialog):
    """Formulario para agregar persona vinculada a un accidente"""

    def __init__(self, db_connection):
        super().__init__()
        self.db = db_connection
        self.model = PersonaModel(db_connection)
        self.setWindowTitle("Agregar Persona")
        self.setMinimumWidth(400)
        self.setup_ui()
        self.load_accidentes()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Accidente
        layout.addWidget(QLabel("Número de Caso:"))
        self.cmb_accidente = QComboBox()
        layout.addWidget(self.cmb_accidente)

        # Tipo de persona
        layout.addWidget(QLabel("Tipo Persona:"))
        self.cmb_tipo = QComboBox()
        self.cmb_tipo.addItems(["Conductor", "Pasajero", "Peatón", "Testigo"])
        layout.addWidget(self.cmb_tipo)

        # Nombre y apellido
        layout.addWidget(QLabel("Nombre:"))
        self.txt_nombre = QLineEdit()
        layout.addWidget(self.txt_nombre)
        layout.addWidget(QLabel("Apellido:"))
        self.txt_apellido = QLineEdit()
        layout.addWidget(self.txt_apellido)

        # DNI, edad, sexo
        layout.addWidget(QLabel("DNI:"))
        self.txt_dni = QLineEdit()
        layout.addWidget(self.txt_dni)
        layout.addWidget(QLabel("Edad:"))
        self.txt_edad = QLineEdit()
        layout.addWidget(self.txt_edad)
        layout.addWidget(QLabel("Sexo:"))
        self.cmb_sexo = QComboBox()
        self.cmb_sexo.addItems(["M", "F"])
        layout.addWidget(self.cmb_sexo)

        # Estado de salud
        layout.addWidget(QLabel("Estado de Salud:"))
        self.cmb_estado = QComboBox()
        self.cmb_estado.addItems(["Ileso", "Herido Leve", "Herido Grave", "Fallecido"])
        layout.addWidget(self.cmb_estado)

        # Botones
        btn_layout = QHBoxLayout()
        btn_guardar = QPushButton("💾 Guardar")
        btn_guardar.clicked.connect(self.guardar_persona)
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.clicked.connect(self.reject)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_guardar)
        btn_layout.addWidget(btn_cancelar)
        layout.addLayout(btn_layout)

    def load_accidentes(self):
        """Carga los números de caso desde la tabla accidentes"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id_accidente, numero_caso FROM accidentes ORDER BY fecha DESC")
            self.accidentes = cursor.fetchall()

            for acc in self.accidentes:
                self.cmb_accidente.addItem(acc[1], acc[0])

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar accidentes:\n{e}")

    def guardar_persona(self):
        """Guarda una persona en la base de datos"""
        try:
            id_accidente = self.cmb_accidente.currentData()
            datos = {
                "id_accidente": id_accidente,
                "tipo_persona": self.cmb_tipo.currentText(),
                "nombre": self.txt_nombre.text(),
                "apellido": self.txt_apellido.text(),
                "dni": self.txt_dni.text(),
                "edad": self.txt_edad.text(),
                "sexo": self.cmb_sexo.currentText(),
                "direccion": "",
                "telefono": "",
                "estado_salud": self.cmb_estado.currentText(),
                "hospital_traslado": "",
                "lesiones_descripcion": "",
                "parentesco_conductor": "",
                "posicion_vehiculo": "",
                "uso_cinturon": 0,
                "uso_casco": 0,
            }

            if not datos["nombre"] or not datos["apellido"]:
                QMessageBox.warning(self, "Campos incompletos", "Debe ingresar nombre y apellido.")
                return

            persona_id = self.model.crear_persona(datos)
            QMessageBox.information(self, "✅ Éxito", f"Persona registrada (ID: {persona_id})")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar la persona:\n{e}")
