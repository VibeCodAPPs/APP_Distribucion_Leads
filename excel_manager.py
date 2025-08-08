"""
Módulo para la gestión de operaciones con archivos Excel en la aplicación de distribución de leads.
Contiene funciones para cargar, procesar y exportar datos a Excel.
"""
import pandas as pd
from utils import identificar_columna_correo, identificar_columna_fecha, identificar_columna_telefono


class ExcelManager:
    """Clase para gestionar operaciones con archivos Excel."""
    
    @staticmethod
    def cargar_archivo(ruta_archivo):
        """
        Carga un archivo Excel en un DataFrame de pandas.
        
        Args:
            ruta_archivo (str): Ruta al archivo Excel.
            
        Returns:
            pandas.DataFrame: DataFrame con los datos del archivo.
            
        Raises:
            Exception: Si hay algún error al cargar el archivo.
        """
        try:
            return pd.read_excel(ruta_archivo)
        except Exception as e:
            raise Exception(f"Error al cargar archivo: {str(e)}")
    
    @staticmethod
    def validar_y_preparar_datos(df):
        """
        Valida que el DataFrame tenga las columnas necesarias y prepara los datos.
        
        Args:
            df (pandas.DataFrame): DataFrame a validar y preparar.
            
        Returns:
            tuple: (DataFrame preparado, columna_correo, columna_fecha)
            
        Raises:
            Exception: Si faltan columnas necesarias.
        """
        # Identificar columnas clave
        columna_correo = identificar_columna_correo(df)
        columna_fecha = identificar_columna_fecha(df)
        
        # Validar columnas necesarias
        if not columna_correo:
            raise Exception("No se pudo identificar una columna de correos electrónicos")
        if not columna_fecha:
            raise Exception("No se pudo identificar una columna de fechas")
        
        # Preparar datos
        df[columna_fecha] = pd.to_datetime(df[columna_fecha], errors='coerce')
        df.sort_values(by=columna_fecha, ascending=False, inplace=True)
        
        return df, columna_correo, columna_fecha
    
    @staticmethod
    def eliminar_duplicados(df, columna_criterio, columna_fecha):
        """
        Elimina los duplicados del dataframe (por correo o teléfono), dejando solo los registros padre (los más antiguos).
        Excluye del análisis los registros con valores vacíos o inválidos en la columna criterio.
        
        Args:
            df (DataFrame): DataFrame con los datos
            columna_criterio (str): Nombre de la columna para identificar duplicados (correo o teléfono)
            columna_fecha (str): Nombre de la columna de fecha para ordenar
            
        Returns:
            tuple: (DataFrame sin duplicados, DataFrame con registros eliminados)
        """
        # Filtrar para trabajar solo con registros que tienen un valor válido en la columna criterio
        df_validos = df[
            df[columna_criterio].notna() & \
            (df[columna_criterio].astype(str).str.strip() != '') & \
            (df[columna_criterio].astype(str).str.strip() != '-')
        ].copy()

        # Mantener los registros que fueron filtrados (inválidos) para añadirlos al final
        df_invalidos = df[
            df[columna_criterio].isna() | \
            (df[columna_criterio].astype(str).str.strip() == '') | \
            (df[columna_criterio].astype(str).str.strip() == '-')
        ].copy()
        
        # Identificar duplicados solo dentro de los registros válidos
        df_con_duplicados = df_validos[df_validos.duplicated(subset=columna_criterio, keep=False)].copy()
        
        if df_con_duplicados.empty:
            # No hay duplicados en los registros válidos, devolver todos los registros (válidos e inválidos)
            df_sin_duplicados = pd.concat([df_validos, df_invalidos]).reset_index(drop=True)
            df_eliminados = pd.DataFrame()  # DataFrame vacío para eliminados
            return df_sin_duplicados, df_eliminados
        
        # Encontrar los registros padre (los más antiguos) de los duplicados
        padres = df_con_duplicados.sort_values(
            by=[columna_criterio, columna_fecha], 
            ascending=[True, True]
        ).drop_duplicates(subset=columna_criterio, keep='first')
        
        # Identificar los registros eliminados (duplicados que NO son padres)
        df_eliminados = df_con_duplicados[~df_con_duplicados.index.isin(padres.index)].copy()
        df_eliminados = df_eliminados.sort_values(by=columna_fecha, ascending=False).reset_index(drop=True)
        
        # Filtrar el DataFrame de válidos: mantener registros únicos + padres de duplicados
        registros_unicos_validos = df_validos[~df_validos.duplicated(subset=columna_criterio, keep=False)]
        
        # Combinar únicos válidos, padres de duplicados y los registros inválidos originales
        df_final = pd.concat([registros_unicos_validos, padres, df_invalidos])
        
        # Restaurar el orden original basado en fecha
        df_final = df_final.sort_values(by=columna_fecha)
        
        # CRÍTICO: Resetear índices para que sean secuenciales (0, 1, 2, 3...)
        df_final = df_final.reset_index(drop=True)
        
        return df_final, df_eliminados
    
    @staticmethod
    def generar_distribucion_final(df, num_auxiliares_iniciales, num_auxiliares_finales, 
                                  nombres_auxiliares_iniciales, nombres_auxiliares_finales):
        """
        Genera el patrón de distribución final, distribuyendo los leads entre todos los auxiliares
        en un orden secuencial: PRIMERO todos los auxiliares iniciales, DESPUÉS todos los finales.
        
        Args:
            df (pandas.DataFrame): DataFrame con los leads a distribuir (YA ORDENADO POR FECHA).
            num_auxiliares_iniciales (int): Número de auxiliares iniciales.
            num_auxiliares_finales (int): Número de auxiliares finales.
            nombres_auxiliares_iniciales (list): Lista de nombres de auxiliares iniciales.
            nombres_auxiliares_finales (list): Lista de nombres de auxiliares finales.
            
        Returns:
            pandas.DataFrame: DataFrame con las columnas de distribución agregadas.
            dict: Mapeo de índices a auxiliares finales (para uso en distribución inicial).
        """
        # Validar parámetros
        if num_auxiliares_iniciales < 2 or num_auxiliares_iniciales > 10:
            raise ValueError("El número de auxiliares iniciales debe estar entre 2 y 10")
            
        if num_auxiliares_finales < 1 or num_auxiliares_finales > 10:
            raise ValueError("El número de auxiliares finales debe estar entre 1 y 10")
            
        if len(nombres_auxiliares_iniciales) != num_auxiliares_iniciales:
            raise ValueError(f"Se esperaban {num_auxiliares_iniciales} nombres de auxiliares iniciales")
            
        if len(nombres_auxiliares_finales) != num_auxiliares_finales:
            raise ValueError(f"Se esperaban {num_auxiliares_finales} nombres de auxiliares finales")
        
        total_registros = len(df)
        total_auxiliares = num_auxiliares_iniciales + num_auxiliares_finales
        
        # IMPORTANTE: El DataFrame ya viene ordenado por fecha descendente desde validar_y_preparar_datos
        # Aplicamos la distribución directamente sobre este orden
        
        # Generar patrón de distribución: PRIMERO todos los iniciales, DESPUÉS todos los finales
        patron_distribucion = []
        mapeo_aux_finales = {}
        
        for i in range(total_registros):
            # Calcular la posición dentro del ciclo completo (iniciales + finales)
            posicion_en_ciclo = i % total_auxiliares
            
            if posicion_en_ciclo < num_auxiliares_iniciales:
                # Estamos en la parte de auxiliares iniciales
                auxiliar = nombres_auxiliares_iniciales[posicion_en_ciclo]
            else:
                # Estamos en la parte de auxiliares finales
                posicion_final = posicion_en_ciclo - num_auxiliares_iniciales
                auxiliar = nombres_auxiliares_finales[posicion_final]
                # Guardar en el mapeo para distribución inicial (usando índice original del DataFrame)
                mapeo_aux_finales[df.index[i]] = auxiliar
            
            patron_distribucion.append(auxiliar)
        
        # Aplicar la distribución final directamente al DataFrame ordenado
        df['Distribución final'] = patron_distribucion
        
        return df, mapeo_aux_finales
    
    @staticmethod
    def generar_distribucion_inicial(df, mapeo_aux_finales, nombres_auxiliares_iniciales, nombres_auxiliares_finales):
        """
        Genera la distribución inicial donde los leads que corresponderían a auxiliares finales
        son repartidos equitativamente entre los auxiliares iniciales, mientras que los leads
        de auxiliares iniciales conservan su asignación.
        
        Args:
            df (pandas.DataFrame): DataFrame con los leads a distribuir con distribución final ya aplicada.
            mapeo_aux_finales (dict): Mapeo de índices originales a auxiliares finales.
            nombres_auxiliares_iniciales (list): Lista de nombres de auxiliares iniciales.
            nombres_auxiliares_finales (list): Lista de nombres de auxiliares finales.
            
        Returns:
            pandas.DataFrame: DataFrame con la columna de distribución inicial agregada.
        """
        # Verificar que ya exista la distribución final
        if 'Distribución final' not in df.columns:
            raise ValueError("Debe existir la columna 'Distribución final' para generar la distribución inicial")
        
        # Primero, copiar la distribución final como base
        df['Distribución inicial'] = df['Distribución final'].copy()
        
        # Si no hay auxiliares iniciales, mostrar un error
        num_aux_iniciales = len(nombres_auxiliares_iniciales)
        if num_aux_iniciales == 0:
            raise ValueError("Debe haber al menos un auxiliar inicial para generar la distribución inicial")
        
        # Contador para distribuir equitativamente los leads de auxiliares finales
        contador_redistribucion = 0
        
        # Redistribuir SOLO los leads que están en el mapeo de auxiliares finales
        # Esto asegura que solo se redistribuyan los leads que realmente fueron asignados a auxiliares finales
        for idx_original in mapeo_aux_finales:
            if idx_original in df.index:
                # Seleccionar el auxiliar inicial para reasignar este lead
                aux_inicial = nombres_auxiliares_iniciales[contador_redistribucion % num_aux_iniciales]
                # Asignar este lead al auxiliar inicial seleccionado
                df.loc[idx_original, 'Distribución inicial'] = aux_inicial
                # Incrementar contador para el próximo lead
                contador_redistribucion += 1
        
        return df
    
    @staticmethod
    def generar_distribuciones(df, num_auxiliares_iniciales, num_auxiliares_finales, 
                              nombres_auxiliares_iniciales, nombres_auxiliares_finales):
        """
        Método principal para generar ambas distribuciones (inicial y final).
        
        Args:
            df (pandas.DataFrame): DataFrame con los leads a distribuir.
            num_auxiliares_iniciales (int): Número de auxiliares iniciales.
            num_auxiliares_finales (int): Número de auxiliares finales.
            nombres_auxiliares_iniciales (list): Lista de nombres de auxiliares iniciales.
            nombres_auxiliares_finales (list): Lista de nombres de auxiliares finales.
            
        Returns:
            pandas.DataFrame: DataFrame con ambas distribuciones aplicadas.
        """
        # Primero generar la distribución final
        df, mapeo_aux_finales = ExcelManager.generar_distribucion_final(
            df, 
            num_auxiliares_iniciales, 
            num_auxiliares_finales, 
            nombres_auxiliares_iniciales, 
            nombres_auxiliares_finales
        )
        
        # Luego generar la distribución inicial basada en la final
        df = ExcelManager.generar_distribucion_inicial(
            df,
            mapeo_aux_finales,
            nombres_auxiliares_iniciales,
            nombres_auxiliares_finales
        )
        
        # Reorganizar columnas para mostrar primero la distribución inicial
        columnas = [col for col in df.columns if col != 'Distribución inicial' and col != 'Distribución final']
        columnas_ordenadas = columnas + ['Distribución inicial', 'Distribución final']
        
        return df[columnas_ordenadas]
    
    @staticmethod
    def procesar_duplicados_correo(df, columna_correo, columna_fecha):
        """
        Procesa los duplicados por correo para el reporte, excluyendo registros inválidos.
        Identifica duplicados, marca al padre (más antiguo) y ordena por fecha descendente.
        """
        if not columna_correo or columna_correo not in df.columns:
            return pd.DataFrame()

        # Filtrar registros con correos válidos
        df_validos = df[
            df[columna_correo].notna() & \
            (df[columna_correo].astype(str).str.strip() != '') & \
            (df[columna_correo].astype(str).str.strip() != '-')
        ].copy()

        # Identificar duplicados solo en los registros válidos
        duplicados = df_validos[df_validos.duplicated(subset=columna_correo, keep=False)].copy()
        if duplicados.empty:
            return pd.DataFrame()

        # Marcar al padre (registro más antiguo)
        duplicados['Padre'] = duplicados.groupby(columna_correo)[columna_fecha].transform('min')
        duplicados['Es Padre'] = duplicados[columna_fecha] == duplicados['Padre']
        duplicados.drop(columns=['Padre'], inplace=True)
        
        # Ordenar para el reporte
        return duplicados.sort_values(by=[columna_correo, columna_fecha], ascending=[True, True])

    @staticmethod
    def procesar_duplicados_telefono(df, columna_telefono, columna_fecha):
        """
        Procesa los duplicados por teléfono para el reporte, excluyendo registros inválidos.
        Identifica duplicados, marca al padre (más antiguo) y ordena por fecha descendente.
        """
        if not columna_telefono or columna_telefono not in df.columns:
            return pd.DataFrame()

        # Filtrar registros con teléfonos válidos
        df_validos = df[
            df[columna_telefono].notna() & \
            (df[columna_telefono].astype(str).str.strip() != '') & \
            (df[columna_telefono].astype(str).str.strip() != '-')
        ].copy()

        # Identificar duplicados solo en los registros válidos
        duplicados = df_validos[df_validos.duplicated(subset=columna_telefono, keep=False)].copy()
        if duplicados.empty:
            return pd.DataFrame()

        # Marcar al padre (registro más antiguo)
        duplicados['Padre'] = duplicados.groupby(columna_telefono)[columna_fecha].transform('min')
        duplicados['Es Padre'] = duplicados[columna_fecha] == duplicados['Padre']
        duplicados.drop(columns=['Padre'], inplace=True)

        # Ordenar para el reporte
        return duplicados.sort_values(by=[columna_telefono, columna_fecha], ascending=[True, True])

    @staticmethod
    def exportar_a_excel(df_principal, duplicados_por_correo, duplicados_por_telefono, file_path, eliminados_principal=None):
        """
        Exporta los DataFrames a un archivo Excel con múltiples pestañas.
        
        Args:
            df_principal: DataFrame principal con leads distribuidos
            duplicados_por_correo: DataFrame con duplicados por correo
            duplicados_por_telefono: DataFrame con duplicados por teléfono  
            file_path: Ruta del archivo de salida
            eliminados_principal: DataFrame con registros eliminados de la lista principal (opcional)
        """
        try:
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                # Exportar hoja principal
                df_principal.to_excel(writer, sheet_name='Leads Distribuidos', index=False)
                
                def procesar_duplicados(duplicados_df, sheet_name):
                    if not duplicados_df.empty:
                        # Verificar si existe la columna 'Padre' o 'Es Padre'
                        padre_col = 'Padre' if 'Padre' in duplicados_df.columns else 'Es Padre'
                        
                        # Si no existe ninguna de las dos columnas, usar el DataFrame completo
                        if padre_col not in duplicados_df.columns:
                            padres_df = duplicados_df.copy()
                        else:
                            # Obtener solo los padres, ordenados por fecha descendente
                            padres_df = duplicados_df[duplicados_df[padre_col]].copy()
                        
                        # Ordenar por fecha si existe la columna
                        if 'Fecha' in padres_df.columns:
                            padres_df = padres_df.sort_values(by='Fecha', ascending=False)
                        
                        # Remover columnas de control antes de exportar
                        for col in ['Padre', 'Es Padre']:
                            if col in padres_df.columns:
                                padres_df = padres_df.drop(columns=[col])
                        
                        padres_df.to_excel(writer, sheet_name=sheet_name, index=False)
                    else:
                        # Si no hay duplicados, crear una hoja con mensaje informativo
                        empty_df = pd.DataFrame({'Información': ['No se encontraron duplicados']})
                        empty_df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # Procesar duplicados por correo y teléfono
                procesar_duplicados(duplicados_por_correo, 'Duplicados por Correo')
                procesar_duplicados(duplicados_por_telefono, 'Duplicados por Teléfono')
                
                # Exportar registros eliminados de la lista principal
                if eliminados_principal is not None:
                    if not eliminados_principal.empty:
                        eliminados_principal.to_excel(writer, sheet_name='Eliminado de Principal', index=False)
                    else:
                        # Si no hay registros eliminados, crear una hoja con mensaje informativo
                        empty_df = pd.DataFrame({'Información': ['No se eliminaron registros de la lista principal']})
                        empty_df.to_excel(writer, sheet_name='Eliminado de Principal', index=False)
                
            return True
        except Exception as e:
            print(f"Error al exportar a Excel: {e}")
            return False

    @staticmethod
    def encontrar_duplicados(df, campos):
        """
        Identifica duplicados en el DataFrame basado en los campos especificados.
        Devuelve un DataFrame con los duplicados y una columna 'Padre' que indica el registro padre.
        """
        try:
            # Identificar duplicados manteniendo el primer registro (padre) como True
            duplicados = df[df.duplicated(subset=campos, keep=False)].copy()
            
            # Marcar padres (primer registro de cada grupo)
            duplicados['Padre'] = ~duplicados.duplicated(subset=campos, keep='first')
            
            # Ordenar por campos y fecha para tener juntos los grupos
            duplicados = duplicados.sort_values(by=campos + ['Fecha'])
            
            return duplicados
        except Exception as e:
            print(f"Error al buscar duplicados: {e}")
            return pd.DataFrame()
