#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicación MODERNA para distribución de leads entre auxiliares
Versión modernizada usando CustomTkinter manteniendo la estructura original.
Permite cargar un archivo Excel, distribuir los leads entre auxiliares
y detectar duplicados por correo y teléfono.
"""
import os
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox
import tkinter as tk
import pandas as pd
import time
import webbrowser
import sys

# Importar módulos propios
import utils
from excel_manager import ExcelManager
from ui_components_modern import ModernUIStyles, ModernUIComponentFactory
from config_manager import ConfigManager


class AplicacionDistribucionLeadsModerna:
    """
    Aplicación MODERNA para la distribución de leads entre auxiliares.
    
    Esta versión utiliza CustomTkinter manteniendo la estructura original:
    - Columna izquierda: Selección archivo, opciones, progreso, botones
    - Columna derecha: Dos listas de auxiliares (inicial y final) lado a lado
    
    Funcionalidades:
    - Cargar un archivo Excel con leads
    - Distribuir los leads entre auxiliares iniciales (2-10) y finales (1-10)
    - Detectar duplicados por correo y teléfono
    - Exportar resultados a un archivo Excel
    - Interfaz moderna con CustomTkinter
    """
    
    def __init__(self, root=None):
        """Inicializa la aplicación moderna."""
        # Configurar tema moderno
        ModernUIStyles.configurar_tema()
        
        # Configuración de la ventana principal
        self.root = root or ctk.CTk()
        self.root.title("SOFASA - Distribución de Leads v3.0 (UI Moderna)")
        self.root.geometry("1000x636")  # Altura ajustada según elección del usuario
        self.root.minsize(1000, 636)
        
        # Configurar icono de la ventana
        self._configurar_icono()
        
        # Inicializar gestor de configuración
        self.config_manager = ConfigManager()
        
        # Variables de la aplicación (igual que la original)
        self._inicializar_variables()
        
        # Crear la interfaz moderna manteniendo estructura original
        self._crear_interfaz_moderna()
        
        # Cargar configuración guardada
        self._cargar_configuracion()
        
        # Configurar el cierre de la aplicación
        self.root.protocol("WM_DELETE_WINDOW", self.salir_aplicacion)
    
    def _configurar_icono(self):
        """Configura el icono de la ventana."""
        try:
            # Buscar el icono de Renault
            icono_path = os.path.join(os.path.dirname(__file__), "ICONOS", "Renault_2021.ico")
            if os.path.exists(icono_path):
                self.root.iconbitmap(icono_path)
            else:
                # Fallback al icono original si existe
                icono_path = os.path.join(os.path.dirname(__file__), "ICONOS", "icono.ico")
                if os.path.exists(icono_path):
                    self.root.iconbitmap(icono_path)
        except Exception as e:
            print(f"No se pudo cargar el icono: {e}")
    
    def _inicializar_variables(self):
        """Inicializa todas las variables de la aplicación (igual que la original)."""
        # Variables para archivo
        self.ruta_archivo = tk.StringVar()
        self.mensaje_estado = tk.StringVar(value="Listo para procesar")
        
        # Cargar configuración inicial
        config_aux_inicial = self.config_manager.get_auxiliares_iniciales()
        config_aux_final = self.config_manager.get_auxiliares_finales()
        config_duplicados = self.config_manager.get_opciones_duplicados()
        
        # Variables para control de auxiliares (igual que la original)
        self.num_aux_inicial = tk.IntVar(value=config_aux_inicial.get("cantidad", 2))
        self.num_aux_final = tk.IntVar(value=config_aux_final.get("cantidad", 1))
        
        # Crear diccionarios para almacenar nombres de auxiliares
        self.nombres_aux_inicial = {}  # Auxiliares que trabajan temprano
        self.nombres_aux_final = {}    # Auxiliares que trabajan tarde
        self.entries_aux_inicial = {}  # Referencias a los entries
        self.entries_aux_final = {}    # Referencias a los entries
        
        # Inicializar con valores por defecto
        for i in range(1, 11):  # Máximo 10 auxiliares por turno
            self.nombres_aux_inicial[i] = tk.StringVar(value=f"Aux Inicial {i}")
            self.nombres_aux_final[i] = tk.StringVar(value=f"Aux Final {i}")
        
        # Cargar nombres guardados si existen
        nombres_inicial_guardados = config_aux_inicial.get("nombres", [])
        nombres_final_guardados = config_aux_final.get("nombres", [])
        
        # Aplicar nombres guardados
        for i, nombre in enumerate(nombres_inicial_guardados, 1):
            if i <= 10 and nombre:
                self.nombres_aux_inicial[i].set(nombre)
        
        for i, nombre in enumerate(nombres_final_guardados, 1):
            if i <= 10 and nombre:
                self.nombres_aux_final[i].set(nombre)
        
        # Variables para controlar búsqueda de duplicados
        self.buscar_duplicados_correo = tk.BooleanVar(value=config_duplicados.get("buscar_correo", True))
        self.buscar_duplicados_telefono = tk.BooleanVar(value=config_duplicados.get("buscar_telefono", True))
        self.eliminar_duplicados_antes = tk.BooleanVar(value=config_duplicados.get("eliminar_antes", False))
        
        # Variables de estado y progreso
        self.progreso = tk.DoubleVar()
        
        # Variables de control
        self.df_cargado = None
        self.procesando = False
        
        # Traces para guardar configuración
        self.buscar_duplicados_correo.trace_add("write", lambda *args: self._guardar_configuracion_auxiliares())
        self.buscar_duplicados_telefono.trace_add("write", lambda *args: self._guardar_configuracion_auxiliares())
        self.eliminar_duplicados_antes.trace_add("write", lambda *args: self._guardar_configuracion_auxiliares())
    
    def _crear_interfaz_moderna(self):
        """Crea la interfaz moderna manteniendo la estructura original."""
        # Crear pie de página PRIMERO (para que aparezca abajo)
        self.footer_frame = ModernUIComponentFactory.crear_footer_moderno(
            self.root,
            self._abrir_changelog,
            self._enviar_correo_desarrollador
        )
        
        # Frame principal
        self.frame_principal = ModernUIComponentFactory.crear_frame_principal(self.root, padding=5)
        
        # Título principal
        ModernUIComponentFactory.crear_titulo(self.frame_principal)
        
        # Crear layout de dos columnas (igual que la original)
        self.frame_izquierdo, self.frame_derecho = ModernUIComponentFactory.crear_layout_columnas(self.frame_principal)
        
        # COLUMNA IZQUIERDA (igual estructura que la original)
        # ----------------
        # Frame para selección de archivo
        self.frame_archivo = ModernUIComponentFactory.crear_frame_archivo(
            self.frame_izquierdo,
            self.ruta_archivo,
            self._seleccionar_archivo,
            self.mensaje_estado
        )
        
        # Frame para opciones de duplicados
        self.frame_opciones = ModernUIComponentFactory.crear_frame_opciones_duplicados(
            self.frame_izquierdo,
            self.buscar_duplicados_correo,
            self.buscar_duplicados_telefono,
            self.eliminar_duplicados_antes
        )
        
        # Frame para progreso y botones
        self.frame_progreso, self.frame_botones = ModernUIComponentFactory.crear_frame_progreso_y_botones(
            self.frame_izquierdo,
            self.progreso,
            self._realizar_distribucion,
            self.salir_aplicacion
        )
        
        # COLUMNA DERECHA (estructura original con dos paneles)
        # ----------------
        # Frame para configuración de auxiliares con dos paneles lado a lado
        componentes_aux = ModernUIComponentFactory.crear_frame_auxiliares_completo(
            self.frame_derecho,
            self.num_aux_inicial,
            self.num_aux_final,
            self.nombres_aux_inicial,
            self.nombres_aux_final,
            self._actualizar_campos_auxiliares_iniciales,
            self._actualizar_campos_auxiliares_finales
        )
        
        # Guardar referencias a los componentes
        self.frame_auxiliares = componentes_aux['frame_auxiliares']
        self.scroll_inicial = componentes_aux['scroll_inicial']
        self.scroll_final = componentes_aux['scroll_final']
        
        # Actualizar campos iniciales
        self._actualizar_campos_auxiliares_iniciales()
        self._actualizar_campos_auxiliares_finales()
    
    def _seleccionar_archivo(self):
        """Permite al usuario seleccionar un archivo Excel y lo valida."""
        try:
            archivo = filedialog.askopenfilename(
                title="Seleccionar archivo Excel",
                filetypes=[
                    ("Archivos Excel", "*.xlsx *.xls"),
                    ("Todos los archivos", "*.*")
                ]
            )
            
            if archivo:
                self.ruta_archivo.set(archivo)
                self._validar_archivo(archivo)
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al seleccionar archivo: {str(e)}")
    
    def _validar_archivo(self, ruta):
        """Valida el archivo Excel seleccionado."""
        try:
            # Cargar archivo usando método estático
            df = ExcelManager.cargar_archivo(ruta)
            
            # Obtener información básica del archivo
            num_filas = len(df)
            num_columnas = len(df.columns)
            
            # Crear mensaje con 4 líneas de información como en la original
            mensaje = f"✅ Archivo válido. {num_filas} registros encontrados."
            
            # Identificar columnas importantes usando utils
            columna_correo = utils.identificar_columna_correo(df)
            columna_fecha = utils.identificar_columna_fecha(df)
            columna_telefono = utils.identificar_columna_telefono(df)
            
            # Agregar información de columnas (4 líneas como en la original)
            if columna_correo:
                mensaje += f"\n📧 Columna de correo: {columna_correo}"
            else:
                mensaje += f"\n📧 No se identificó columna de correo"
                
            if columna_fecha:
                mensaje += f"\n📅 Columna de fecha: {columna_fecha}"
            else:
                mensaje += f"\n📅 No se identificó columna de fecha"
                
            if columna_telefono:
                mensaje += f"\n📱 Columna de teléfono: {columna_telefono}"
            else:
                mensaje += f"\n📱 No se identificó columna de teléfono"
            
            self.mensaje_estado.set(mensaje)
            
            # Guardar referencia al DataFrame para uso posterior
            self.df_cargado = df
            
        except Exception as e:
            self.mensaje_estado.set(f"❌ Error al validar archivo:\n{str(e)}")
            self.df_cargado = None
    
    def _actualizar_campos_auxiliares_iniciales(self):
        """Actualiza los campos de nombres de auxiliares iniciales."""
        num_auxiliares = self.num_aux_inicial.get()
        
        ModernUIComponentFactory.actualizar_auxiliares_iniciales(
            self.scroll_inicial,
            self.nombres_aux_inicial,
            num_auxiliares,
            self.entries_aux_inicial
        )
        
        # Agregar traces para guardar configuración
        for i in range(1, num_auxiliares + 1):
            self.nombres_aux_inicial[i].trace_add("write", lambda *args: self._on_nombre_auxiliar_changed())
        
        # Guardar configuración
        self._guardar_configuracion_auxiliares()
    
    def _actualizar_campos_auxiliares_finales(self):
        """Actualiza los campos de nombres de auxiliares finales."""
        num_auxiliares = self.num_aux_final.get()
        
        ModernUIComponentFactory.actualizar_auxiliares_finales(
            self.scroll_final,
            self.nombres_aux_final,
            num_auxiliares,
            self.entries_aux_final
        )
        
        # Agregar traces para guardar configuración
        for i in range(1, num_auxiliares + 1):
            self.nombres_aux_final[i].trace_add("write", lambda *args: self._on_nombre_auxiliar_changed())
        
        # Guardar configuración
        self._guardar_configuracion_auxiliares()
    
    def _guardar_configuracion_auxiliares(self):
        """Guarda la configuración actual de auxiliares."""
        try:
            # Obtener nombres actuales de auxiliares iniciales
            nombres_inicial = []
            for i in range(1, self.num_aux_inicial.get() + 1):
                if i in self.nombres_aux_inicial:
                    nombres_inicial.append(self.nombres_aux_inicial[i].get())
            
            # Obtener nombres actuales de auxiliares finales
            nombres_final = []
            for i in range(1, self.num_aux_final.get() + 1):
                if i in self.nombres_aux_final:
                    nombres_final.append(self.nombres_aux_final[i].get())
            
            # Guardar configuración de auxiliares iniciales
            self.config_manager.set_auxiliares_iniciales(self.num_aux_inicial.get(), nombres_inicial)
            
            # Guardar configuración de auxiliares finales
            self.config_manager.set_auxiliares_finales(self.num_aux_final.get(), nombres_final)
            
            # Guardar opciones de duplicados
            self.config_manager.set_opciones_duplicados(
                self.buscar_duplicados_correo.get(),
                self.buscar_duplicados_telefono.get(),
                self.eliminar_duplicados_antes.get()
            )
            
            # Guardar archivo de configuración
            self.config_manager.guardar_configuracion()
            
        except Exception as e:
            print(f"Error al guardar configuración: {e}")
    
    def _on_nombre_auxiliar_changed(self):
        """Callback para guardar configuración cuando cambie el nombre de un auxiliar."""
        # Usar after para evitar llamadas excesivas
        if hasattr(self, '_save_timer'):
            self.root.after_cancel(self._save_timer)
        self._save_timer = self.root.after(1000, self._guardar_configuracion_auxiliares)
    
    def _realizar_distribucion(self):
        """Valida las entradas y lanza el proceso de distribución."""
        if self.procesando:
            messagebox.showwarning("Advertencia", "Ya hay un proceso en ejecución.")
            return
        
        # Validaciones
        if not self._validar_datos():
            return
        
        # Iniciar proceso en hilo separado
        self.procesando = True
        thread = threading.Thread(target=self._procesar_distribucion, daemon=True)
        thread.start()
    
    def _validar_datos(self):
        """Valida los datos antes de procesar."""
        if not self.df_cargado:
            messagebox.showerror("Error", "Primero selecciona un archivo Excel válido.")
            return False
        
        # Validar que hay al menos un auxiliar inicial con nombre
        auxiliares_iniciales_validos = 0
        for i in range(1, self.num_aux_inicial.get() + 1):
            if i in self.nombres_aux_inicial and self.nombres_aux_inicial[i].get().strip():
                auxiliares_iniciales_validos += 1
        
        if auxiliares_iniciales_validos == 0:
            messagebox.showerror("Error", "Debe haber al menos un auxiliar inicial con nombre válido.")
            return False
        
        # Validar que hay al menos un auxiliar final con nombre
        auxiliares_finales_validos = 0
        for i in range(1, self.num_aux_final.get() + 1):
            if i in self.nombres_aux_final and self.nombres_aux_final[i].get().strip():
                auxiliares_finales_validos += 1
        
        if auxiliares_finales_validos == 0:
            messagebox.showerror("Error", "Debe haber al menos un auxiliar final con nombre válido.")
            return False
        
        return True
    
    def _procesar_distribucion(self):
        """Procesa la distribución de leads según la configuración seleccionada."""
        try:
            # Actualizar estado
            self.mensaje_estado.set("🔄 Iniciando procesamiento...")
            self.progreso.set(0.1)
            
            # Obtener nombres de auxiliares válidos
            nombres_iniciales = self._obtener_nombres_auxiliares_iniciales()
            nombres_finales = self._obtener_nombres_auxiliares_finales()
            
            # Usar el DataFrame ya cargado
            df = self.df_cargado.copy()
            df_original = self.df_cargado.copy()  # Copia para reportes de duplicados
            
            # Identificar columnas necesarias
            self.mensaje_estado.set("📊 Identificando columnas...")
            self.progreso.set(0.2)
            
            columnas = utils.identificar_columnas(df)
            columna_correo = columnas.get("email", "")
            columna_telefono = columnas.get("phone", "")
            columna_fecha = columnas.get("fecha", "")
            
            # Inicializar DataFrames para duplicados
            df_duplicados_correo = pd.DataFrame()
            df_duplicados_telefono = pd.DataFrame()
            eliminados_principal = pd.DataFrame()
            
            # Procesar eliminación de duplicados si está habilitada
            if self.eliminar_duplicados_antes.get():
                self.mensaje_estado.set("🔄 Procesando duplicados antes de la distribución...")
                self.progreso.set(0.3)
                
                # Eliminar duplicados por correo si está habilitado
                if self.buscar_duplicados_correo.get() and columna_correo and columna_fecha:
                    self.mensaje_estado.set("📧 Eliminando duplicados por correo...")
                    df, eliminados_correo = ExcelManager.eliminar_duplicados(df, columna_correo, columna_fecha)
                    if not eliminados_correo.empty:
                        eliminados_principal = pd.concat([eliminados_principal, eliminados_correo], ignore_index=True)
                
                # Eliminar duplicados por teléfono si está habilitado
                if self.buscar_duplicados_telefono.get() and columna_telefono and columna_fecha:
                    self.mensaje_estado.set("📱 Eliminando duplicados por teléfono...")
                    df, eliminados_telefono = ExcelManager.eliminar_duplicados(df, columna_telefono, columna_fecha)
                    if not eliminados_telefono.empty:
                        eliminados_principal = pd.concat([eliminados_principal, eliminados_telefono], ignore_index=True)
                
                # Eliminar duplicados dentro del DataFrame de eliminados
                if not eliminados_principal.empty:
                    eliminados_principal = eliminados_principal.drop_duplicates().reset_index(drop=True)
            
            # Identificar duplicados para reportes (independientemente de si se eliminaron)
            if self.buscar_duplicados_correo.get() and columna_correo and columna_fecha:
                self.mensaje_estado.set("📧 Identificando duplicados por correo para reporte...")
                self.progreso.set(0.4)
                df_duplicados_correo = ExcelManager.procesar_duplicados_correo(
                    df_original, columna_correo, columna_fecha
                )
            
            if self.buscar_duplicados_telefono.get() and columna_telefono and columna_fecha:
                self.mensaje_estado.set("📱 Identificando duplicados por teléfono para reporte...")
                self.progreso.set(0.5)
                df_duplicados_telefono = ExcelManager.procesar_duplicados_telefono(
                    df_original, columna_telefono, columna_fecha
                )
            
            # Ordenar por fecha (más recientes primero)
            self.mensaje_estado.set("📅 Ordenando datos...")
            self.progreso.set(0.6)
            if columna_fecha:
                df.sort_values(by=columna_fecha, ascending=False, inplace=True)
            
            # Generar distribuciones
            self.mensaje_estado.set("🚀 Generando distribuciones...")
            self.progreso.set(0.7)
            
            df = ExcelManager.generar_distribuciones(
                df,
                len(nombres_iniciales),
                len(nombres_finales),
                nombres_iniciales,
                nombres_finales
            )
            
            # Guardar archivo
            self.mensaje_estado.set("💾 Guardando archivo...")
            self.progreso.set(0.9)
            
            archivo_salida = self._generar_nombre_archivo_salida()
            exito = ExcelManager.exportar_a_excel(
                df, 
                df_duplicados_correo, 
                df_duplicados_telefono, 
                archivo_salida, 
                eliminados_principal
            )
            
            # Completado
            self.progreso.set(1.0)
            self.mensaje_estado.set(f"✅ Proceso completado. Archivo guardado: {os.path.basename(archivo_salida)}")
            
            # Mostrar resumen
            resultado = {
                'total_leads': len(df_original),
                'leads_distribuidos': len(df),
                'duplicados_encontrados': len(df_duplicados_correo) + len(df_duplicados_telefono),
                'distribucion_auxiliares': self._calcular_distribucion_auxiliares(df, nombres_iniciales, nombres_finales)
            }
            
            self._mostrar_resumen_resultado(resultado, archivo_salida)
            
        except Exception as e:
            self.mensaje_estado.set(f"❌ Error durante el procesamiento: {str(e)}")
            messagebox.showerror("Error", f"Error durante el procesamiento:\n{str(e)}")
        
        finally:
            self.procesando = False
    
    def _calcular_distribucion_auxiliares(self, df, nombres_iniciales, nombres_finales):
        """Calcula la distribución de leads por auxiliar."""
        distribucion = {}
        
        # Contar distribución inicial
        if 'Auxiliar Inicial' in df.columns:
            for aux in nombres_iniciales:
                count = len(df[df['Auxiliar Inicial'] == aux])
                if count > 0:
                    distribucion[f"{aux} (Inicial)"] = count
        
        # Contar distribución final
        if 'Auxiliar Final' in df.columns:
            for aux in nombres_finales:
                count = len(df[df['Auxiliar Final'] == aux])
                if count > 0:
                    distribucion[f"{aux} (Final)"] = count
        
        return distribucion
    
    def _obtener_nombres_auxiliares_iniciales(self):
        """Obtiene la lista de nombres de auxiliares iniciales válidos."""
        nombres = []
        for i in range(1, self.num_aux_inicial.get() + 1):
            if i in self.nombres_aux_inicial:
                nombre = self.nombres_aux_inicial[i].get().strip()
                if nombre:
                    nombres.append(nombre)
        return nombres
    
    def _obtener_nombres_auxiliares_finales(self):
        """Obtiene la lista de nombres de auxiliares finales válidos."""
        nombres = []
        for i in range(1, self.num_aux_final.get() + 1):
            if i in self.nombres_aux_final:
                nombre = self.nombres_aux_final[i].get().strip()
                if nombre:
                    nombres.append(nombre)
        return nombres
    
    def _actualizar_progreso(self, valor, mensaje=""):
        """Callback para actualizar el progreso."""
        self.progreso.set(valor)
        if mensaje:
            self.mensaje_estado.set(mensaje)
    
    def _generar_nombre_archivo_salida(self):
        """Genera el nombre del archivo de salida."""
        archivo_original = self.ruta_archivo.get()
        directorio = os.path.dirname(archivo_original)
        nombre_base = os.path.splitext(os.path.basename(archivo_original))[0]
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        nombre_salida = f"{nombre_base}_distribuido_{timestamp}.xlsx"
        
        return os.path.join(directorio, nombre_salida)
    
    def _mostrar_resumen_resultado(self, resultado, archivo_salida):
        """Muestra un resumen del resultado del procesamiento."""
        resumen = f"""
🎉 DISTRIBUCIÓN COMPLETADA

📊 Resumen:
• Total de leads procesados: {resultado.get('total_leads', 0)}
• Leads distribuidos: {resultado.get('leads_distribuidos', 0)}
• Duplicados encontrados: {resultado.get('duplicados_encontrados', 0)}

👥 Distribución:
"""
        
        for aux, cantidad in resultado.get('distribucion_auxiliares', {}).items():
            resumen += f"• {aux}: {cantidad} leads\n"
        
        resumen += f"\n💾 Archivo guardado en:\n{archivo_salida}"
        
        # Preguntar si abrir el archivo
        respuesta = messagebox.askyesno(
            "Distribución Completada",
            resumen + "\n\n¿Deseas abrir el archivo generado?",
            icon='question'
        )
        
        if respuesta:
            try:
                os.startfile(archivo_salida)
            except Exception as e:
                messagebox.showwarning("Advertencia", f"No se pudo abrir el archivo: {str(e)}")
    
    def _cargar_configuracion(self):
        """Carga la configuración guardada."""
        # La configuración ya se carga en _inicializar_variables
        # Solo necesitamos actualizar los campos
        self._actualizar_campos_auxiliares_iniciales()
        self._actualizar_campos_auxiliares_finales()
    
    def salir_aplicacion(self):
        """Maneja el cierre de la aplicación."""
        if self.procesando:
            respuesta = messagebox.askyesno(
                "Confirmar salida",
                "Hay un proceso en ejecución. ¿Estás seguro de que deseas salir?",
                icon='warning'
            )
            if not respuesta:
                return
        
        # Guardar configuración antes de salir
        self._guardar_configuracion_auxiliares()
        
        # Cerrar aplicación
        self.root.quit()
        self.root.destroy()
    
    def ejecutar(self):
        """Inicia el bucle principal de la aplicación."""
        self.root.mainloop()
    
    def _abrir_changelog(self):
        """Abre una ventana con el contenido del changelog."""
        try:
            # Buscar el archivo CHANGELOG.md
            changelog_path = os.path.join(os.path.dirname(__file__), "CHANGELOG.md")
            
            if not os.path.exists(changelog_path):
                messagebox.showerror("Error", f"No se encontró el archivo CHANGELOG.md en la ruta: {changelog_path}")
                return
            
            # Leer el contenido del changelog
            with open(changelog_path, 'r', encoding='utf-8') as file:
                contenido = file.read()
            
            # Crear ventana modal para mostrar el changelog
            ventana_changelog = ctk.CTkToplevel(self.root)
            ventana_changelog.title("Historial de Cambios - SOFASA Distribución de Leads")
            ventana_changelog.geometry("800x600")
            ventana_changelog.resizable(True, True)
            
            # Configurar icono si está disponible
            try:
                icono_path = os.path.join(os.path.dirname(__file__), "ICONOS", "Renault_2021.ico")
                if os.path.exists(icono_path):
                    ventana_changelog.iconbitmap(icono_path)
            except:
                pass
            
            # Frame principal del changelog
            frame_principal = ctk.CTkFrame(ventana_changelog)
            frame_principal.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Título
            titulo = ctk.CTkLabel(
                frame_principal,
                text="📋 Historial de Cambios",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            titulo.pack(pady=(10, 15))
            
            # Área de texto scrollable para el contenido
            texto_scrollable = ctk.CTkScrollableFrame(frame_principal)
            texto_scrollable.pack(fill="both", expand=True, padx=10, pady=(0, 10))
            
            # Mostrar el contenido del changelog
            texto_contenido = ctk.CTkLabel(
                texto_scrollable,
                text=contenido,
                font=ctk.CTkFont(size=11),
                justify="left",
                anchor="nw",
                wraplength=750
            )
            texto_contenido.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Frame para botones
            frame_botones = ctk.CTkFrame(frame_principal, fg_color="transparent")
            frame_botones.pack(fill="x", padx=10, pady=(0, 10))
            
            # Botón cerrar
            btn_cerrar = ctk.CTkButton(
                frame_botones,
                text="Cerrar",
                command=ventana_changelog.destroy,
                width=100
            )
            btn_cerrar.pack(side="right")
            
            # Centrar la ventana y hacerla modal
            ventana_changelog.transient(self.root)
            ventana_changelog.grab_set()
            
            # Centrar en pantalla
            ventana_changelog.update_idletasks()
            x = (ventana_changelog.winfo_screenwidth() // 2) - (800 // 2)
            y = (ventana_changelog.winfo_screenheight() // 2) - (600 // 2)
            ventana_changelog.geometry(f"800x600+{x}+{y}")
            
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró el archivo CHANGELOG.md")
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir el changelog: {str(e)}")
    
    def _enviar_correo_desarrollador(self):
        """Abre el cliente de correo electrónico para enviar un correo al desarrollador."""
        correo = "jose.de-la-colina@renault.com"
        asunto = "Consulta sobre SOFASA Distribución de Leads"
        cuerpo = "Hola José Manuel,\n\n"
        
        # Construir la URL para abrir el cliente de correo electrónico
        url = f"mailto:{correo}?subject={asunto}&body={cuerpo}"
        
        # Abrir el cliente de correo electrónico
        webbrowser.open(url)


def main():
    """Función principal para iniciar la aplicación moderna."""
    try:
        # Crear y ejecutar la aplicación
        app = AplicacionDistribucionLeadsModerna()
        app.ejecutar()
        
    except Exception as e:
        messagebox.showerror("Error Fatal", f"Error al iniciar la aplicación:\n{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
