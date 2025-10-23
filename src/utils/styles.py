"""
Estilos globales modernos para SIATLITE
"""

# Colores del tema
COLORS = {
    'primary': '#2A82DA',
    'primary_hover': '#1E5FA8',
    'success': '#28A745',
    'danger': '#DC3545',
    'warning': '#FFC107',
    'info': '#17A2B8',
    'dark': '#1E1E28',
    'dark_light': '#282838',
    'background': '#2A2A3A',
    'card': '#32323F',
    'text': '#DCDCDC',
    'text_secondary': '#9A9A9A',
    'border': '#404050',
}

GLOBAL_STYLESHEET = f"""
/* ========== GENERAL ========== */
* {{
    font-family: 'Segoe UI', Arial, sans-serif;
}}

QMainWindow {{
    background-color: {COLORS['background']};
}}

QWidget {{
    color: {COLORS['text']};
}}

/* ========== BOTONES ========== */
QPushButton {{
    background-color: {COLORS['primary']};
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 500;
    font-size: 11pt;
}}

QPushButton:hover {{
    background-color: {COLORS['primary_hover']};
}}

QPushButton:pressed {{
    background-color: #164378;
}}

QPushButton:disabled {{
    background-color: #3A3A4A;
    color: #6A6A7A;
}}

QPushButton#btnSuccess {{
    background-color: {COLORS['success']};
}}

QPushButton#btnSuccess:hover {{
    background-color: #218838;
}}

QPushButton#btnDanger {{
    background-color: {COLORS['danger']};
}}

QPushButton#btnDanger:hover {{
    background-color: #C82333;
}}

QPushButton#btnWarning {{
    background-color: {COLORS['warning']};
    color: #000;
}}

QPushButton#btnWarning:hover {{
    background-color: #E0A800;
}}

QPushButton#btnSecondary {{
    background-color: {COLORS['card']};
    border: 2px solid {COLORS['border']};
}}

QPushButton#btnSecondary:hover {{
    background-color: #3A3A4A;
}}

/* ========== INPUTS ========== */
QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox {{
    background-color: {COLORS['card']};
    border: 2px solid {COLORS['border']};
    border-radius: 6px;
    padding: 8px 12px;
    color: {COLORS['text']};
    font-size: 10pt;
}}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, 
QSpinBox:focus, QDoubleSpinBox:focus {{
    border: 2px solid {COLORS['primary']};
}}

/* ========== COMBOBOX ========== */
QComboBox {{
    background-color: {COLORS['card']};
    border: 2px solid {COLORS['border']};
    border-radius: 6px;
    padding: 8px 12px;
    color: {COLORS['text']};
    font-size: 10pt;
}}

QComboBox:hover {{
    border: 2px solid {COLORS['primary']};
}}

QComboBox::drop-down {{
    border: none;
    width: 30px;
}}

QComboBox::down-arrow {{
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid {COLORS['text']};
    margin-right: 10px;
}}

QComboBox QAbstractItemView {{
    background-color: {COLORS['card']};
    border: 2px solid {COLORS['border']};
    selection-background-color: {COLORS['primary']};
    selection-color: white;
    padding: 5px;
}}

/* ========== TABLAS ========== */
QTableWidget {{
    background-color: {COLORS['card']};
    border: 2px solid {COLORS['border']};
    border-radius: 8px;
    gridline-color: {COLORS['border']};
    selection-background-color: {COLORS['primary']};
}}

QTableWidget::item {{
    padding: 8px;
    border: none;
}}

QTableWidget::item:selected {{
    background-color: {COLORS['primary']};
    color: white;
}}

QTableWidget::item:hover {{
    background-color: {COLORS['dark_light']};
}}

QHeaderView::section {{
    background-color: {COLORS['dark_light']};
    color: {COLORS['text']};
    padding: 10px;
    border: none;
    border-right: 1px solid {COLORS['border']};
    border-bottom: 2px solid {COLORS['border']};
    font-weight: bold;
    font-size: 10pt;
}}

/* ========== SCROLLBAR ========== */
QScrollBar:vertical {{
    background-color: {COLORS['dark']};
    width: 12px;
    border-radius: 6px;
}}

QScrollBar::handle:vertical {{
    background-color: {COLORS['border']};
    border-radius: 6px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {COLORS['primary']};
}}

QScrollBar:horizontal {{
    background-color: {COLORS['dark']};
    height: 12px;
    border-radius: 6px;
}}

QScrollBar::handle:horizontal {{
    background-color: {COLORS['border']};
    border-radius: 6px;
    min-width: 30px;
}}

QScrollBar::handle:horizontal:hover {{
    background-color: {COLORS['primary']};
}}

QScrollBar::add-line, QScrollBar::sub-line {{
    height: 0px;
    width: 0px;
}}

/* ========== LABELS ========== */
QLabel {{
    color: {COLORS['text']};
    font-size: 10pt;
}}

QLabel#lblTitle {{
    font-size: 18pt;
    font-weight: bold;
    color: {COLORS['text']};
}}

QLabel#lblSubtitle {{
    font-size: 12pt;
    font-weight: 500;
    color: {COLORS['text_secondary']};
}}

QLabel#lblSectionTitle {{
    font-size: 14pt;
    font-weight: 600;
    color: {COLORS['primary']};
    padding: 10px 0px;
}}

/* ========== FRAMES ========== */
QFrame#cardFrame {{
    background-color: {COLORS['card']};
    border-radius: 12px;
    border: 1px solid {COLORS['border']};
    padding: 20px;
}}

QFrame#sidebarFrame {{
    background-color: {COLORS['dark']};
    border-right: 2px solid {COLORS['border']};
}}

/* ========== MENÚ LATERAL ========== */
QPushButton#sidebarButton {{
    background-color: transparent;
    color: {COLORS['text']};
    text-align: left;
    padding: 15px 20px;
    border: none;
    border-radius: 8px;
    font-size: 11pt;
    font-weight: 500;
}}

QPushButton#sidebarButton:hover {{
    background-color: {COLORS['dark_light']};
}}

QPushButton#sidebarButton:checked {{
    background-color: {COLORS['primary']};
    color: white;
}}

/* ========== TABS ========== */
QTabWidget::pane {{
    border: 2px solid {COLORS['border']};
    border-radius: 8px;
    background-color: {COLORS['card']};
    padding: 10px;
}}

QTabBar::tab {{
    background-color: {COLORS['dark_light']};
    color: {COLORS['text']};
    padding: 12px 24px;
    margin-right: 4px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    font-weight: 500;
}}

QTabBar::tab:selected {{
    background-color: {COLORS['primary']};
    color: white;
}}

QTabBar::tab:hover {{
    background-color: {COLORS['primary_hover']};
}}

/* ========== CHECKBOX Y RADIO ========== */
QCheckBox, QRadioButton {{
    color: {COLORS['text']};
    spacing: 8px;
    font-size: 10pt;
}}

QCheckBox::indicator, QRadioButton::indicator {{
    width: 20px;
    height: 20px;
    border: 2px solid {COLORS['border']};
    border-radius: 4px;
    background-color: {COLORS['card']};
}}

QCheckBox::indicator:checked, QRadioButton::indicator:checked {{
    background-color: {COLORS['primary']};
    border-color: {COLORS['primary']};
}}

/* ========== MENSAJES ========== */
QMessageBox {{
    background-color: {COLORS['card']};
}}

/* ========== MENÚ CONTEXTUAL ========== */
QMenu {{
    background-color: {COLORS['card']};
    border: 2px solid {COLORS['border']};
    border-radius: 8px;
    padding: 8px;
}}

QMenu::item {{
    padding: 10px 20px;
    border-radius: 6px;
}}

QMenu::item:selected {{
    background-color: {COLORS['primary']};
    color: white;
}}

/* ========== PROGRESSBAR ========== */
QProgressBar {{
    border: 2px solid {COLORS['border']};
    border-radius: 8px;
    text-align: center;
    background-color: {COLORS['card']};
    color: {COLORS['text']};
}}

QProgressBar::chunk {{
    background-color: {COLORS['primary']};
    border-radius: 6px;
}}

/* ========== GROUPBOX ========== */
QGroupBox {{
    border: 2px solid {COLORS['border']};
    border-radius: 8px;
    margin-top: 10px;
    padding-top: 20px;
    background-color: {COLORS['card']};
    font-weight: bold;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 5px 10px;
    color: {COLORS['primary']};
    font-size: 11pt;
}}

/* ========== STATUSBAR ========== */
QStatusBar {{
    background-color: {COLORS['dark']};
    color: {COLORS['text']};
    border-top: 2px solid {COLORS['border']};
}}

/* ========== TOOLBAR ========== */
QToolBar {{
    background-color: {COLORS['dark']};
    border-bottom: 2px solid {COLORS['border']};
    spacing: 10px;
    padding: 5px;
}}

QToolButton {{
    background-color: transparent;
    color: {COLORS['text']};
    border: none;
    border-radius: 6px;
    padding: 8px;
}}

QToolButton:hover {{
    background-color: {COLORS['dark_light']};
}}

/* ========== DATEEDIT Y TIMEEDIT ========== */
QDateEdit, QTimeEdit, QDateTimeEdit {{
    background-color: {COLORS['card']};
    border: 2px solid {COLORS['border']};
    border-radius: 6px;
    padding: 8px 12px;
    color: {COLORS['text']};
}}

QDateEdit::drop-down, QTimeEdit::drop-down, QDateTimeEdit::drop-down {{
    border: none;
    width: 30px;
}}

QCalendarWidget {{
    background-color: {COLORS['card']};
    color: {COLORS['text']};
}}

QCalendarWidget QToolButton {{
    color: {COLORS['text']};
    background-color: {COLORS['dark_light']};
    border-radius: 6px;
}}

QCalendarWidget QMenu {{
    background-color: {COLORS['card']};
}}

QCalendarWidget QSpinBox {{
    background-color: {COLORS['dark_light']};
    color: {COLORS['text']};
}}
"""

# Función para crear estilos de tarjetas estadísticas
def get_stat_card_style(color):
    return f"""
        QFrame {{
            background-color: {COLORS['card']};
            border-radius: 12px;
            border-left: 4px solid {color};
            padding: 20px;
        }}
        QLabel#lblValue {{
            font-size: 32pt;
            font-weight: bold;
            color: {color};
        }}
        QLabel#lblTitle {{
            font-size: 11pt;
            color: {COLORS['text_secondary']};
        }}
    """