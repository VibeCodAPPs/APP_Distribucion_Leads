#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para generar el ejecutable de la aplicación de distribución de leads en un solo archivo.
"""
import os
import subprocess
import sys
from pathlib import Path

def build_executable():
    """Construye el ejecutable de la aplicación en un solo archivo."""
    print("Iniciando generación del ejecutable en un solo archivo...")
    
    # Obtener el directorio del escritorio
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    
    # Directorio actual donde se encuentra este script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Ruta al icono
    icon_path = os.path.join(current_dir, "ICONOS", "Renault_2021.ico")
    
    # Verificar que el icono existe
    if not os.path.exists(icon_path):
        print(f"ERROR: No se encontró el icono en la ruta: {icon_path}")
        return False
    
    # Ruta al script principal
    main_script = os.path.join(current_dir, "app_completa.py")
    
    # Nombre del ejecutable
    output_name = "SOFASA_Distribucion_Leads"
    
    # Construir el comando de PyInstaller usando lista para evitar problemas con espacios y caracteres especiales
    # Usamos --onefile para crear un solo ejecutable
    pyinstaller_cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onefile",  # Esta es la opción clave para un solo archivo
        "--windowed",
        f"--icon={icon_path}",
        f"--name={output_name}",
        f"--add-data={os.path.join(current_dir, 'ICONOS')};ICONOS",
        f"--add-data={os.path.join(current_dir, 'CHANGELOG.md')};.",
        "--hidden-import=excel_manager",
        "--hidden-import=ui_components",
        "--hidden-import=utils",
        "--hidden-import=config_manager",
        "--hidden-import=cleanup",
        f"--distpath={desktop_path}",
        main_script
    ]
    
    # Ejecutar el comando
    print(f"Ejecutando PyInstaller para generar un solo archivo ejecutable...")
    try:
        result = subprocess.run(pyinstaller_cmd, check=True)
        success = result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"ERROR al ejecutar PyInstaller: {str(e)}")
        return False
    except Exception as e:
        print(f"ERROR inesperado: {str(e)}")
        return False
    
    # Verificar si se generó el ejecutable
    exe_path = os.path.join(desktop_path, f"{output_name}.exe")
    if os.path.exists(exe_path):
        print(f"Ejecutable creado con éxito en: {exe_path}")
        print(f"Tamaño del archivo: {os.path.getsize(exe_path) / (1024*1024):.2f} MB")
        return True
    else:
        print(f"ERROR: No se pudo encontrar el ejecutable generado en: {exe_path}")
        return False

if __name__ == "__main__":
    success = build_executable()
    if success:
        print("¡Proceso completado con éxito!")
        input("Presione Enter para cerrar...")
        sys.exit(0)
    else:
        print("El proceso de generación del ejecutable ha fallado.")
        input("Presione Enter para cerrar...")
        sys.exit(1)
