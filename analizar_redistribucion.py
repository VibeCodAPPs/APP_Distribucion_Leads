#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análisis detallado de la redistribución para entender la diferencia
"""
import pandas as pd
from excel_manager import ExcelManager

def analizar_redistribucion_detallada():
    """Análisis detallado de la redistribución"""
    print("=" * 80)
    print("ANALISIS DETALLADO DE REDISTRIBUCION")
    print("=" * 80)
    
    # Configuración
    auxiliares_iniciales = ['JOSE', 'VICTOR']
    auxiliares_finales = ['ROGER']
    
    try:
        # Cargar y preparar datos
        df_original = ExcelManager.cargar_archivo("21.xlsx")
        df_preparado, columna_correo, columna_fecha = ExcelManager.validar_y_preparar_datos(df_original.copy())
        
        print(f"Total registros: {len(df_preparado)}")
        
        # Generar solo distribución final para analizar el mapeo
        df_con_final, mapeo_aux_finales = ExcelManager.generar_distribucion_final(
            df_preparado.copy(),
            len(auxiliares_iniciales),
            len(auxiliares_finales),
            auxiliares_iniciales,
            auxiliares_finales
        )
        
        # Analizar distribución final
        conteo_final = df_con_final['Distribución final'].value_counts()
        print(f"\nDISTRIBUCION FINAL:")
        for aux, count in conteo_final.items():
            print(f"  {aux}: {count} leads")
        
        print(f"\nLEADS DE ROGER A REDISTRIBUIR: {conteo_final.get('ROGER', 0)}")
        print(f"AUXILIARES INICIALES: {len(auxiliares_iniciales)}")
        
        # Calcular redistribución teórica
        leads_roger = conteo_final.get('ROGER', 0)
        leads_por_inicial = leads_roger // len(auxiliares_iniciales)
        leads_restantes = leads_roger % len(auxiliares_iniciales)
        
        print(f"\nREDISTRIBUCION TEORICA:")
        print(f"  {leads_roger} leads ÷ {len(auxiliares_iniciales)} auxiliares = {leads_por_inicial} cada uno")
        print(f"  Leads restantes: {leads_restantes}")
        print(f"  Distribución esperada:")
        for i, aux in enumerate(auxiliares_iniciales):
            extra = 1 if i < leads_restantes else 0
            esperado = leads_por_inicial + extra
            print(f"    {aux}: {esperado} leads adicionales")
        
        # Analizar el mapeo real
        print(f"\nANALISIS DEL MAPEO:")
        print(f"  Total índices en mapeo: {len(mapeo_aux_finales)}")
        print(f"  Primeros 10 índices: {list(mapeo_aux_finales.keys())[:10]}")
        
        # Verificar que todos los índices del mapeo están en el DataFrame
        indices_validos = 0
        indices_invalidos = 0
        for idx in mapeo_aux_finales:
            if idx in df_con_final.index:
                indices_validos += 1
            else:
                indices_invalidos += 1
        
        print(f"  Índices válidos en DataFrame: {indices_validos}")
        print(f"  Índices inválidos: {indices_invalidos}")
        
        # Generar distribución inicial y analizar
        df_resultado = ExcelManager.generar_distribucion_inicial(
            df_con_final.copy(),
            mapeo_aux_finales,
            auxiliares_iniciales,
            auxiliares_finales
        )
        
        # Analizar resultado final
        conteo_inicial = df_resultado['Distribución inicial'].value_counts()
        print(f"\nDISTRIBUCION INICIAL REAL:")
        for aux, count in conteo_inicial.items():
            print(f"  {aux}: {count} leads")
        
        # Calcular cuántos leads adicionales recibió cada auxiliar inicial
        print(f"\nLEADS ADICIONALES POR AUXILIAR:")
        for aux in auxiliares_iniciales:
            leads_originales = conteo_final.get(aux, 0)
            leads_finales = conteo_inicial.get(aux, 0)
            leads_adicionales = leads_finales - leads_originales
            print(f"  {aux}: {leads_originales} originales + {leads_adicionales} adicionales = {leads_finales} total")
        
        # Verificar diferencia
        diferencia = max(conteo_inicial) - min(conteo_inicial)
        print(f"\nDIFERENCIA MAXIMA: {diferencia}")
        
        if diferencia <= 1:
            print("OK REDISTRIBUCION UNIFORME CORRECTA")
        else:
            print("ERROR REDISTRIBUCION NO UNIFORME - REQUIERE CORRECCION")
            
            # Analizar por qué hay diferencia mayor a 1
            print(f"\nDIAGNOSTICO:")
            leads_totales_adicionales = sum(conteo_inicial.get(aux, 0) - conteo_final.get(aux, 0) for aux in auxiliares_iniciales)
            print(f"  Total leads redistribuidos: {leads_totales_adicionales}")
            print(f"  Leads de ROGER esperados: {leads_roger}")
            
            if leads_totales_adicionales != leads_roger:
                print(f"  ERROR: No coinciden los leads redistribuidos ({leads_totales_adicionales}) con los de ROGER ({leads_roger})")
            else:
                print(f"  OK Cantidad total correcta")
                print(f"  ERROR Problema en la distribución equitativa")
        
        return diferencia <= 1
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    exito = analizar_redistribucion_detallada()
    
    print("\n" + "=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    
    if exito:
        print("La redistribución es uniforme y correcta")
    else:
        print("Se requiere ajuste en la lógica de redistribución")
    
    print("=" * 80)
