"""
Módulo de utilidades para procesamiento de datos en la aplicación de distribución de leads.
Contiene funciones para identificar columnas, validar datos y otros procesos auxiliares.
"""
import re
import os
import sys
import pandas as pd
import subprocess
import time


def identificar_columna_correo(df):
    """
    Identifica la columna que contiene correos electrónicos.
    
    Args:
        df (pandas.DataFrame): DataFrame con los datos a analizar.
        
    Returns:
        str: Nombre de la columna que contiene correos electrónicos, o None si no se encuentra.
    """
    # Buscar por nombre de columna primero
    posibles_nombres = ['correo', 'email', 'mail', 'e-mail', 'correo electrónico']
    for nombre in posibles_nombres:
        columnas = [c for c in df.columns if nombre in c.lower()]
        if columnas:
            return columnas[0]
    
    # Buscar por patrón en los datos
    patron_correo = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    for columna in df.columns:
        valores = df[columna].astype(str)
        # Si más del 50% de valores coinciden con el patrón, asumimos que es la columna de correo
        if valores.str.match(patron_correo).mean() > 0.5:
            return columna
    
    return None


def identificar_columna_fecha(df):
    """
    Identifica la columna que contiene fechas.
    
    Args:
        df (pandas.DataFrame): DataFrame con los datos a analizar.
        
    Returns:
        str: Nombre de la columna que contiene fechas, o None si no se encuentra.
    """
    # Buscar por nombre de columna primero
    posibles_nombres = ['fecha', 'date', 'creación', 'created', 'alta', 'registro']
    for nombre in posibles_nombres:
        columnas = [c for c in df.columns if nombre in c.lower()]
        if columnas:
            return columnas[0]
    
    # PRIORIDAD 1: Buscar columnas que YA sean de tipo datetime
    for columna in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[columna]):
            return columna
    
    # PRIORIDAD 2: Intentar convertir cada columna a datetime (solo si no hay columnas datetime nativas)
    for columna in df.columns:
        try:
            # Verificar que no sea una columna de números secuenciales
            if df[columna].dtype in ['int64', 'int32'] and df[columna].nunique() == len(df):
                # Si es una columna de enteros con valores únicos (probablemente IDs), saltar
                continue
            pd.to_datetime(df[columna])
            return columna
        except (ValueError, TypeError):
            continue
    
    return None


def identificar_columna_id(df):
    """
    Identifica la columna que probablemente sea un identificador único.
    
    Args:
        df (pandas.DataFrame): DataFrame con los datos a analizar.
        
    Returns:
        str: Nombre de la columna que contiene IDs, o None si no se encuentra.
    """
    # Buscar por nombre de columna primero
    posibles_nombres = ['id', 'identificador', 'código', 'code', 'folio']
    for nombre in posibles_nombres:
        columnas = [c for c in df.columns if nombre in c.lower()]
        if columnas:
            return columnas[0]
    
    # Buscar columnas con valores únicos (más del 95%)
    for columna in df.columns:
        if df[columna].nunique() / len(df) > 0.95:
            return columna
    
    return None


def identificar_columna_telefono(df):
    """
    Identifica la columna que contiene números telefónicos.
    
    Args:
        df (pandas.DataFrame): DataFrame con los datos a analizar.
        
    Returns:
        str: Nombre de la columna que contiene teléfonos, o None si no se encuentra.
    """
    # Buscar por nombre de columna primero
    posibles_nombres = ['tel', 'tél', 'fono', 'phone', 'móvil', 'celular', 'contacto']
    for nombre in posibles_nombres:
        columnas = [c for c in df.columns if nombre in c.lower()]
        if columnas:
            return columnas[0]
    
    # Buscar por patrón numérico (teléfonos normalmente tienen al menos 7-10 dígitos)
    patron_num = r'^\+?\d{7,}'
    for columna in df.columns:
        valores = df[columna].astype(str)
        # Si más del 50% de valores coinciden con el patrón, asumimos que es la columna de teléfono
        if valores.str.match(patron_num).mean() > 0.5:
            return columna
    
    return None


def identificar_columnas(df):
    """
    Identifica todas las columnas relevantes en el DataFrame.
    
    Args:
        df (pandas.DataFrame): DataFrame con los datos a analizar.
        
    Returns:
        dict: Diccionario con las columnas identificadas (email, fecha, id, phone).
    """
    columnas = {
        "email": identificar_columna_correo(df),
        "fecha": identificar_columna_fecha(df),
        "id": identificar_columna_id(df),
        "phone": identificar_columna_telefono(df)
    }
    
    return columnas


def abrir_archivo(ruta_archivo):
    """
    Abre un archivo con la aplicación predeterminada del sistema.
    
    Args:
        ruta_archivo (str): Ruta completa al archivo a abrir.
    """
    try:
        if os.name == 'nt':  # Windows
            os.startfile(ruta_archivo)
        elif os.name == 'posix':  # macOS y Linux
            subprocess.run(['open' if sys.platform == 'darwin' else 'xdg-open', ruta_archivo])
    except Exception as e:
        print(f"Error al abrir el archivo {ruta_archivo}: {e}")


def obtener_ruta_salida(ruta_entrada):
    """
    Genera una ruta de salida para el archivo procesado.
    Ej: 'C:\path\to\file.xlsx' -> 'C:\path\to\file_distribuido_YYYYMMDD_HHMMSS.xlsx'
    """
    directorio, nombre_archivo = os.path.split(ruta_entrada)
    nombre_base, ext = os.path.splitext(nombre_archivo)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    nuevo_nombre = f"{nombre_base}_distribuido_{timestamp}{ext}"
    return os.path.join(directorio, nuevo_nombre)
