from PyQt6.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt6.QtGui import QFont, QPalette, QColor
from src.ui.main_window import MainWindow
from src.ui.views.login_view import LoginView
from src.utils.styles import GLOBAL_STYLESHEET
import sys


def setup_application():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    app.setStyleSheet(GLOBAL_STYLESHEET)

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 40))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(220, 220, 220))
    palette.setColor(QPalette.ColorRole.Base, QColor(40, 40, 50))
    palette.setColor(QPalette.ColorRole.Button, QColor(50, 50, 60))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(220, 220, 220))
    app.setPalette(palette)
    return app


def main():
    app = setup_application()
    db_path = r"D:\programacion\python\avanzada\IIICICLO\siatlite\data\siatlite.db"

    login = LoginView(db_path)
    result = login.exec()  # Espera que el usuario cierre el login

    print("🧭 [DEBUG] Resultado del exec():", result)

    if result == QDialog.DialogCode.Accepted:
        print("✅ Login aceptado, abriendo MainWindow...")
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    else:
        print("❌ Login cancelado o fallido.")
        sys.exit(0)


if __name__ == '__main__':
    main()
