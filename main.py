#!/usr/bin/env python3
"""
SIAT-Lite - Sistema de Información de Accidentes de Tránsito
Archivo principal de la aplicación
"""

import sys
import os

# Agregar src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.controllers.main_controller import MainController

def main():
    """Función principal"""
    try:
        app = MainController()
        app.iniciar_aplicacion()
    except Exception as e:
        print(f"Error fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()