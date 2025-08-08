#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para debuggear específicamente el problema de redistribución
"""
import pandas as pd
from excel_manager import ExcelManager

def debug_redistribucion_detallado():
    """Debug detallado del problema de redistribución"""
    print("=" * 80)
    print("DEBUG DETALLADO DE REDISTRIBUCION")
    print("=" * 80)
    
    # Configuración exacta del usuario
    auxiliares_iniciales = ['JOSE', 'VICTOR']
    auxiliares_finales = ['ROGER']
    
    print(f"Auxiliares iniciales: {auxiliares_iniciales}")
    print(f"Auxiliares finales: {auxiliares_finales}")
    
    try:
        # Cargar archivo real
        df_original = ExcelManager.cargar_archivo("21.xlsx")
        print(f"\nArchivo cargado: {len(df_original)} registros")
        
        # Validar y preparar datos
        df_preparado, columna_correo, columna_fecha = ExcelManager.validar_y_preparar_datos(df_original.copy())
        print(f"Datos preparados: {len(df_preparado)} registros")
        
        # PASO 1: Generar solo distribución final para analizar el patrón
        print(f"\n--- PASO 1: GENERANDO DISTRIBUCION FINAL ---")
        df_con_final, mapeo_aux_finales = ExcelManager.generar_distribucion_final(
            df_preparado.copy(),
            len(auxiliares_iniciales),
            len(auxiliares_finales), 
            auxiliares_iniciales,
            auxiliares_finales
        )
        
        # Analizar patrón de distribución final
        print(f"\nPATRON DE DISTRIBUCION FINAL (primeros 20):")
        print("Pos | Auxiliar | Esperado | Correcto")
        print("----|----------|----------|----------")
        
        patron_esperado = auxiliares_iniciales + auxiliares_finales  # ['JOSE', 'VICTOR', 'ROGER']
        errores_patron = 0
        
        for i in range(min(20, len(df_con_final))):
            auxiliar_asignado = df_con_final.iloc[i]['Distribución final']
            esperado = patron_esperado[i % len(patron_esperado)]
            correcto = auxiliar_asignado == esperado
            if not correcto:
                errores_patron += 1
            print(f"{i+1:2d}  | {auxiliar_asignado:8s} | {esperado:8s} | {'SI' if correcto else 'NO'}")
        
        print(f"\nErrores en patrón de distribución final: {errores_patron}")
        
        # PASO 2: Analizar mapeo de auxiliares finales
        print(f"\n--- PASO 2: ANALIZANDO MAPEO DE AUXILIARES FINALES ---")
        print(f"Mapeo auxiliares finales (primeros 10): {dict(list(mapeo_aux_finales.items())[:10])}")
        print(f"Total auxiliares finales en mapeo: {len(mapeo_aux_finales)}")
        
        # Verificar que el mapeo coincide con ROGER en distribución final
        roger_en_final = len(df_con_final[df_con_final['Distribución final'] == 'ROGER'])
        print(f"ROGER en distribución final: {roger_en_final}")
        print(f"ROGER en mapeo: {len(mapeo_aux_finales)}")
        
        # PASO 3: Generar distribución inicial manualmente para debug
        print(f"\n--- PASO 3: GENERANDO DISTRIBUCION INICIAL (DEBUG) ---")
        
        # Copiar distribución final como base
        df_debug = df_con_final.copy()
        df_debug['Distribución inicial'] = df_debug['Distribución final'].copy()
        
        # Reset índice
        df_debug_reset = df_debug.reset_index(drop=True)
        
        contador_redistribucion = 0
        cambios_realizados = []
        
        print(f"\nProcesando redistribución lead por lead:")
        print("Pos | Dist.Final | Acción")
        print("----|------------|------------------")
        
        for i in range(min(20, len(df_debug_reset))):
            auxiliar_asignado = df_debug_reset.loc[i, 'Distribución final']
            
            if auxiliar_asignado in auxiliares_finales:
                # Es auxiliar final - redistribuir
                aux_inicial = auxiliares_iniciales[contador_redistribucion % len(auxiliares_iniciales)]
                df_debug_reset.loc[i, 'Distribución inicial'] = aux_inicial
                accion = f"REDISTRIB: {auxiliar_asignado}->{aux_inicial}"
                cambios_realizados.append((i, auxiliar_asignado, aux_inicial))
                contador_redistribucion += 1
            elif auxiliar_asignado in auxiliares_iniciales:
                # Es auxiliar inicial - conservar
                accion = f"CONSERVAR: {auxiliar_asignado}"
            else:
                # No debería pasar
                accion = f"ERROR: {auxiliar_asignado} no reconocido"
            
            print(f"{i+1:2d}  | {auxiliar_asignado:10s} | {accion}")
        
        # Restaurar al DataFrame original
        df_debug['Distribución inicial'] = df_debug_reset['Distribución inicial']
        
        # PASO 4: Comparar con el método original
        print(f"\n--- PASO 4: COMPARANDO CON METODO ORIGINAL ---")
        
        df_metodo_original = ExcelManager.generar_distribuciones(
            df_preparado.copy(),
            len(auxiliares_iniciales),
            len(auxiliares_finales), 
            auxiliares_iniciales,
            auxiliares_finales
        )
        
        print(f"\nComparación (primeros 20):")
        print("Pos | Final | Debug.Inicial | Metodo.Inicial | Coincide")
        print("----|-------|---------------|----------------|----------")
        
        diferencias = 0
        for i in range(min(20, len(df_debug))):
            final = df_debug.iloc[i]['Distribución final']
            debug_inicial = df_debug.iloc[i]['Distribución inicial']
            metodo_inicial = df_metodo_original.iloc[i]['Distribución inicial']
            coincide = debug_inicial == metodo_inicial
            if not coincide:
                diferencias += 1
            
            print(f"{i+1:2d}  | {final:5s} | {debug_inicial:13s} | {metodo_inicial:14s} | {'SI' if coincide else 'NO'}")
        
        print(f"\nDiferencias encontradas: {diferencias}")
        
        if diferencias == 0:
            print("El método funciona correctamente - el problema debe estar en otro lugar")
        else:
            print("Hay diferencias - el método tiene un bug")
        
        return diferencias == 0
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    exito = debug_redistribucion_detallado()
    
    print("\n" + "=" * 80)
    print("RESULTADO DEL DEBUG")
    print("=" * 80)
    
    if exito:
        print("El método de redistribución funciona correctamente")
    else:
        print("Se confirmó un bug en el método de redistribución")
    
    print("=" * 80)
