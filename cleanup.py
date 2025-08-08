#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para limpiar archivos innecesarios del proyecto
"""
import os
import shutil
from pathlib import Path

def cleanup_project():
    """Elimina archivos innecesarios del proyecto para hacer los ejecutables más livianos"""
    print("Iniciando limpieza del proyecto...")
    
    # Directorio actual
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Archivos esenciales que debemos mantener
    essential_files = [
        'app_completa.py',      # Archivo principal de la aplicación
        'excel_manager.py',     # Gestor de Excel
        'ui_components.py',     # Componentes de UI
        'utils.py',             # Utilidades
        'requirements.txt',     # Dependencias
        'build_exe_onefile.py', # Script para crear el ejecutable
        'cleanup.py'            # Este script
    ]
    
    # Directorios esenciales que debemos mantener
    essential_dirs = [
        'ICONOS'                # Contiene iconos necesarios
    ]
    
    # Directorios a eliminar completamente
    dirs_to_remove = [
        '__pycache__',          # Archivos de caché de Python
        'build',                # Archivos temporales de compilación
        '.idea'                 # Archivos de configuración de IDE
    ]
    
    # Eliminar directorios completos
    for dir_name in dirs_to_remove:
        dir_path = os.path.join(current_dir, dir_name)
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            print(f"Eliminando directorio: {dir_name}")
            try:
                shutil.rmtree(dir_path)
            except Exception as e:
                print(f"Error al eliminar {dir_name}: {str(e)}")
    
    # Eliminar archivos individuales innecesarios
    for item in os.listdir(current_dir):
        item_path = os.path.join(current_dir, item)
        
        # Mantener directorios esenciales
        if os.path.isdir(item_path) and item in essential_dirs:
            continue
        
        # Mantener archivos esenciales
        if os.path.isfile(item_path) and item in essential_files:
            continue
        
        # Mantener dist solo si contiene archivos (por si el usuario ya generó un ejecutable)
        if item == 'dist' and os.path.isdir(item_path):
            if not os.listdir(item_path):  # Si está vacío
                print(f"Eliminando directorio vacío: {item}")
                shutil.rmtree(item_path)
            continue
        
        # Eliminar archivos .spec (generados por PyInstaller)
        if os.path.isfile(item_path) and item.endswith('.spec'):
            print(f"Eliminando archivo .spec: {item}")
            os.remove(item_path)
            continue
            
        # Eliminar archivos de Excel generados
        if os.path.isfile(item_path) and item.endswith('.xlsx'):
            print(f"Eliminando archivo Excel: {item}")
            os.remove(item_path)
            continue
            
        # Eliminar scripts de compilación antiguos
        if os.path.isfile(item_path) and (
            item.startswith('build_exe') and 
            item != 'build_exe_onefile.py'
        ):
            print(f"Eliminando script de compilación antiguo: {item}")
            os.remove(item_path)
            continue
            
        # Eliminar otros archivos Python no esenciales
        if os.path.isfile(item_path) and item.endswith('.py') and item not in essential_files:
            # Verificar si es un módulo no utilizado por app_completa.py
            is_unused = True
            with open(os.path.join(current_dir, 'app_completa.py'), 'r', encoding='utf-8') as f:
                content = f.read()
                module_name = item[:-3]  # Quitar la extensión .py
                if f'import {module_name}' in content or f'from {module_name}' in content:
                    is_unused = False
            
            if is_unused:
                print(f"Eliminando módulo Python no utilizado: {item}")
                os.remove(item_path)
    
    print("\nLimpieza completada.")
    print("\nArchivos mantenidos:")
    for root, dirs, files in os.walk(current_dir):
        rel_path = os.path.relpath(root, current_dir)
        if rel_path == '.':
            for file in files:
                print(f"- {file}")
        else:
            print(f"- {rel_path}/")

if __name__ == "__main__":
    cleanup_project()
    input("\nPresione Enter para cerrar...")
