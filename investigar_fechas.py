#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Investigar las fechas reales en el archivo del usuario
"""
import pandas as pd
from utils import identificar_columna_fecha

def investigar_fechas_archivo():
    """Investiga las fechas reales en el archivo"""
    print("=" * 80)
    print("INVESTIGACION DE FECHAS EN ARCHIVO REAL")
    print("=" * 80)
    
    try:
        # Cargar archivo sin procesar
        df_original = pd.read_excel("21.xlsx")
        print(f"Archivo cargado: {len(df_original)} registros")
        print(f"Columnas disponibles: {list(df_original.columns)}")
        
        # Mostrar información de cada columna
        print(f"\nINFORMACION DE COLUMNAS:")
        for col in df_original.columns:
            print(f"  {col}:")
            print(f"    Tipo: {df_original[col].dtype}")
            print(f"    Valores únicos: {df_original[col].nunique()}")
            print(f"    Primeros 3 valores: {df_original[col].head(3).tolist()}")
            print()
        
        # Identificar columna de fecha usando la función del sistema
        columna_fecha = identificar_columna_fecha(df_original)
        print(f"Columna de fecha identificada por el sistema: {columna_fecha}")
        
        if columna_fecha:
            print(f"\nANALISIS DE LA COLUMNA DE FECHA '{columna_fecha}':")
            col_fecha = df_original[columna_fecha]
            print(f"  Tipo original: {col_fecha.dtype}")
            print(f"  Valores únicos: {col_fecha.nunique()}")
            print(f"  Primeros 10 valores:")
            for i in range(min(10, len(col_fecha))):
                print(f"    {i+1:2d}. {col_fecha.iloc[i]}")
            
            # Intentar convertir a datetime
            print(f"\n  Intentando conversión a datetime...")
            try:
                col_fecha_convertida = pd.to_datetime(col_fecha, errors='coerce')
                print(f"  Conversión exitosa!")
                print(f"  Tipo después de conversión: {col_fecha_convertida.dtype}")
                print(f"  Primeros 10 valores convertidos:")
                for i in range(min(10, len(col_fecha_convertida))):
                    print(f"    {i+1:2d}. {col_fecha_convertida.iloc[i]}")
                
                # Verificar si hay fechas válidas
                fechas_validas = col_fecha_convertida.notna().sum()
                fechas_invalidas = col_fecha_convertida.isna().sum()
                print(f"  Fechas válidas: {fechas_validas}")
                print(f"  Fechas inválidas (NaT): {fechas_invalidas}")
                
                if fechas_validas > 0:
                    fecha_min = col_fecha_convertida.min()
                    fecha_max = col_fecha_convertida.max()
                    print(f"  Fecha más antigua: {fecha_min}")
                    print(f"  Fecha más reciente: {fecha_max}")
                
            except Exception as e:
                print(f"  ERROR en conversión: {str(e)}")
        
        # Buscar manualmente columnas que puedan ser fechas
        print(f"\nBUSQUEDA MANUAL DE COLUMNAS DE FECHA:")
        posibles_fechas = []
        
        for col in df_original.columns:
            # Buscar columnas que contengan palabras relacionadas con fechas
            col_lower = str(col).lower()
            if any(palabra in col_lower for palabra in ['fecha', 'date', 'time', 'created', 'updated', 'timestamp']):
                posibles_fechas.append(col)
                print(f"  Posible columna de fecha: {col}")
        
        if not posibles_fechas:
            print("  No se encontraron columnas obvias de fecha por nombre")
            
            # Buscar por tipo de datos
            print(f"\n  Buscando por tipo de datos...")
            for col in df_original.columns:
                if df_original[col].dtype == 'object':
                    # Verificar si los primeros valores parecen fechas
                    sample_values = df_original[col].dropna().head(5).astype(str).tolist()
                    print(f"    {col} (object): {sample_values}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    investigar_fechas_archivo()
    print("=" * 80)
