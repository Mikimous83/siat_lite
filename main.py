from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6.QtGui import QFont, QPalette, QColor
from src.ui.main_window import MainWindow
from src.ui.views.login_view import LoginView
from src.utils.styles import GLOBAL_STYLESHEET
import sys


def setup_application():
    """Configura la aplicación con estilos y tema oscuro"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    font = QFont("Segoe UI", 10)
    app.setFont(font)
    app.setStyleSheet(GLOBAL_STYLESHEET)

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 40))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(220, 220, 220))
    palette.setColor(QPalette.ColorRole.Base, QColor(40, 40, 50))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(45, 45, 55))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(220, 220, 220))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(220, 220, 220))
    palette.setColor(QPalette.ColorRole.Text, QColor(220, 220, 220))
    palette.setColor(QPalette.ColorRole.Button, QColor(50, 50, 60))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(220, 220, 220))
    palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)

    return app


def main():
    """Inicio del sistema con pantalla de login"""
    app = setup_application()

    db_path = r"D:\programacion\python\avanzada\IIICICLO\siatlite\data\siatlite.db"

    # 🔐 Mostrar login antes del sistema principal
    login = LoginView(db_path)
    if login.exec() == QDialog.DialogCode.Accepted:
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
