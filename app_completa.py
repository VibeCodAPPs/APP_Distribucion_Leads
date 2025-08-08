#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicación para distribución de leads entre auxiliares
Permite cargar un archivo Excel, distribuir los leads entre auxiliares
y detectar duplicados por correo y teléfono.
"""
import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import time
import webbrowser
import sys

# Importar módulos propios
import utils  # Importar módulo completo
from excel_manager import ExcelManager
from ui_components import UIStyles, UIComponentFactory
from config_manager import ConfigManager  # AÑADIDO: Importar gestor de configuración


class AplicacionDistribucionLeads:
    """
    Aplicación principal para la distribución de leads entre auxiliares.
    
    Esta aplicación permite:
    - Cargar un archivo Excel con leads
    - Distribuir los leads entre 2 o 3 auxiliares
    - Detectar duplicados por correo y teléfono
    - Exportar resultados a un archivo Excel
    """
    
    def __init__(self, root=None):
        """Inicializa la aplicación."""
        # Configuración de la ventana
        self.root = root or tk.Tk()
        self.root.title("SOFASA - Distribución de Leads v2.5.3")
        self.root.geometry("900x480")  # Ajustada a la altura actual del usuario
        self.root.minsize(900, 480)    # Ajustado tamaño mínimo
        
        # Configurar icono de la ventana
        self._configurar_icono()
        
        # Configurar estilo
        UIStyles.configurar_estilo()
        
        # AÑADIDO: Inicializar gestor de configuración
        self.config_manager = ConfigManager()
        
        # Variables de configuración
        self.ruta_archivo = tk.StringVar()
        
        # AÑADIDO: Cargar configuración guardada
        config_aux_inicial = self.config_manager.get_auxiliares_iniciales()
        config_aux_final = self.config_manager.get_auxiliares_finales()
        config_duplicados = self.config_manager.get_opciones_duplicados()
        
        # Variables para control de auxiliares (con valores cargados)
        self.num_aux_inicial = tk.IntVar(value=config_aux_inicial.get("cantidad", 2))  # Auxiliares de distribución inicial
        self.num_aux_final = tk.IntVar(value=config_aux_final.get("cantidad", 1))    # Auxiliares de distribución final
        
        # Crear diccionarios para almacenar nombres de auxiliares
        self.nombres_aux_inicial = {}  # Auxiliares que trabajan temprano
        self.nombres_aux_final = {}    # Auxiliares que trabajan tarde
        self.entries_aux_inicial = {}  # Referencias a los entries
        self.entries_aux_final = {}    # Referencias a los entries
        
        # Inicializar con valores por defecto
        for i in range(1, 11):  # Máximo 10 auxiliares por turno
            self.nombres_aux_inicial[i] = tk.StringVar(value=f"Aux Inicial {i}")
            self.nombres_aux_final[i] = tk.StringVar(value=f"Aux Final {i}")
        
        # AÑADIDO: Cargar nombres guardados si existen
        nombres_inicial_guardados = config_aux_inicial.get("nombres", [])
        nombres_final_guardados = config_aux_final.get("nombres", [])
        
        # Aplicar nombres guardados
        for i, nombre in enumerate(nombres_inicial_guardados, 1):
            if i <= 10 and nombre:  # Máximo 10 auxiliares y nombre no vacío
                self.nombres_aux_inicial[i].set(nombre)
        
        for i, nombre in enumerate(nombres_final_guardados, 1):
            if i <= 10 and nombre:  # Máximo 10 auxiliares y nombre no vacío
                self.nombres_aux_final[i].set(nombre)
        
        # Variables para controlar búsqueda de duplicados
        self.buscar_duplicados_correo = tk.BooleanVar(value=config_duplicados.get("buscar_correo", True))
        self.buscar_duplicados_telefono = tk.BooleanVar(value=config_duplicados.get("buscar_telefono", True))
        self.eliminar_duplicados_antes = tk.BooleanVar(value=config_duplicados.get("eliminar_antes", False))
        
        # AÑADIDO: Traces para guardar configuración cuando cambien las opciones de duplicados
        self.buscar_duplicados_correo.trace_add("write", lambda *args: self._guardar_configuracion_auxiliares())
        self.buscar_duplicados_telefono.trace_add("write", lambda *args: self._guardar_configuracion_auxiliares())
        self.eliminar_duplicados_antes.trace_add("write", lambda *args: self._guardar_configuracion_auxiliares())
        
        # Variables de estado y progreso
        self.progreso = tk.DoubleVar()
        self.mensaje_estado = tk.StringVar(value="Listo para procesar")
        
        # Crear y configurar la interfaz
        self._configurar_interfaz()
    
    def _configurar_interfaz(self):
        """Configura la interfaz gráfica de la aplicación."""
        # Configurar ventana principal para que tenga un tamaño mínimo razonable
        self.root.minsize(900, 480)  # Ajustado tamaño mínimo
        
        # Crear un estilo específico para el pie de página
        style = ttk.Style()
        style.configure("Footer.TFrame", background="#e0e0e0")
        style.configure("Footer.TLabel", background="#e0e0e0", font=("Segoe UI", 8))
        style.configure("Link.TLabel", background="#e0e0e0", font=("Segoe UI", 8), foreground="#0066cc")
        
        # Pie de página con información del desarrollador (fuera del frame_principal)
        frame_footer = ttk.Frame(self.root, style="Footer.TFrame")
        frame_footer.pack(fill="x", side=tk.BOTTOM, pady=(5, 0))
        
        # Información del desarrollador (lado derecho) - clickeable para enviar correo
        link_desarrollador = ttk.Label(
            frame_footer, 
            text="José Manuel de la Colina (Diseño y desarrollo) - jose.de-la-colina@renault.com",
            style="Link.TLabel",
            cursor="hand2"
        )
        link_desarrollador.pack(side=tk.RIGHT, padx=10, pady=3)
        link_desarrollador.bind("<Button-1>", lambda e: self._enviar_correo_desarrollador())
        
        # Hipervínculo para abrir changelog (lado izquierdo)
        link_changelog = ttk.Label(
            frame_footer, 
            text="Ver Historial de Cambios",
            style="Link.TLabel",
            cursor="hand2"
        )
        link_changelog.pack(side=tk.LEFT, padx=10, pady=3)
        link_changelog.bind("<Button-1>", lambda e: self._abrir_changelog())
        
        # Frame principal
        frame_principal = ttk.Frame(self.root)
        frame_principal.pack(fill="both", expand=True, padx=10, pady=5)  # Reducido el padding vertical
        
        # Título
        ttk.Label(frame_principal, text="Distribución de Leads", 
                 style="Header.TLabel").pack(pady=(0, 10))  # Reducido el padding inferior
        
        # Crear dos frames para layout de dos columnas
        frame_izquierdo = ttk.Frame(frame_principal, width=400)  # Aumentado para dar más espacio al botón
        frame_izquierdo.pack(side=tk.LEFT, fill="y", expand=False, padx=(0, 10))
        frame_izquierdo.pack_propagate(False)  # Evitar que el frame se encoja
        
        frame_derecho = ttk.Frame(frame_principal)
        frame_derecho.pack(side=tk.RIGHT, fill="both", expand=True, padx=(10, 0))
        
        # COLUMNA IZQUIERDA (más estrecha)
        # ----------------
        # Frame para selección de archivo
        UIComponentFactory.crear_frame_archivo(
            frame_izquierdo, self.ruta_archivo, self._seleccionar_archivo, self.mensaje_estado
        )
        
        # Frame para opciones de duplicados
        self._configurar_frame_opciones(frame_izquierdo)
        
        # Barra de progreso separada
        frame_progreso = ttk.Frame(frame_izquierdo)
        frame_progreso.pack(fill="x", pady=(10, 5))  # Reducido el padding vertical
        ttk.Label(frame_progreso, text="Progreso:").pack(side=tk.LEFT, padx=(0, 10))
        progress_bar = ttk.Progressbar(frame_progreso, variable=self.progreso, maximum=100)
        progress_bar.pack(fill="x", expand=True)
        
        # Frame para botones de acción debajo de la barra de progreso
        frame_botones = ttk.Frame(frame_izquierdo)
        frame_botones.pack(fill="x", pady=(5, 0))  # Reducido el padding vertical
        
        button_distribuir = ttk.Button(frame_botones, text="Realizar Distribución", command=self._realizar_distribucion)
        button_distribuir.pack(side=tk.LEFT, padx=(0, 5), fill="x", expand=True)
        
        button_salir = ttk.Button(frame_botones, text="Salir", command=self.root.quit)
        button_salir.pack(side=tk.RIGHT, padx=(5, 0), fill="x", expand=True)
        
        # COLUMNA DERECHA
        # ----------------
        # Frame para configuración de auxiliares en columna derecha
        self._crear_frame_auxiliares(frame_derecho)
    
    def _crear_frame_auxiliares(self, frame_principal):
        """Crea el frame para la configuración de auxiliares."""
        frame_auxiliares = ttk.LabelFrame(frame_principal, text="Configuración de Auxiliares", padding=10)
        frame_auxiliares.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Frame para selección del número de auxiliares
        frame_seleccion = ttk.Frame(frame_auxiliares)
        frame_seleccion.pack(fill="x", pady=(0, 10))
        
        # Spinbox para seleccionar número de auxiliares iniciales (2-10)
        ttk.Label(frame_seleccion, text="Auxiliares iniciales:").pack(side=tk.LEFT, padx=(0, 10))
        spinbox_inicial = ttk.Spinbox(
            frame_seleccion, 
            from_=2, 
            to=10, 
            width=5,
            textvariable=self.num_aux_inicial,
            command=self._actualizar_campos_auxiliares_iniciales
        )
        spinbox_inicial.pack(side=tk.LEFT)
        
        ttk.Label(frame_seleccion, text="Auxiliares finales:").pack(side=tk.LEFT, padx=(20, 10))
        spinbox_final = ttk.Spinbox(
            frame_seleccion, 
            from_=1, 
            to=10, 
            width=5,
            textvariable=self.num_aux_final,
            command=self._actualizar_campos_auxiliares_finales
        )
        spinbox_final.pack(side=tk.LEFT)
        
        # Frame para contener los dos paneles de auxiliares lado a lado
        frame_auxiliares_contenedor = ttk.Frame(frame_auxiliares)
        frame_auxiliares_contenedor.pack(fill="both", expand=True, pady=5)
        
        # Configurar grid para distribución equitativa
        frame_auxiliares_contenedor.columnconfigure(0, weight=1, uniform="panel")
        frame_auxiliares_contenedor.columnconfigure(1, weight=1, uniform="panel")
        
        # Panel izquierdo - Auxiliares iniciales - Usando grid para ancho igual
        frame_col_inicial = ttk.LabelFrame(frame_auxiliares_contenedor, text="Auxiliares Distribución Inicial")
        frame_col_inicial.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        # Panel derecho - Auxiliares finales - Usando grid para ancho igual
        frame_col_final = ttk.LabelFrame(frame_auxiliares_contenedor, text="Auxiliares Distribución Final")
        frame_col_final.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
        # Frame para nombres iniciales con scroll
        self.canvas_inicial = tk.Canvas(frame_col_inicial, highlightthickness=0, height=255)  # Altura reducida
        scrollbar_inicial = ttk.Scrollbar(frame_col_inicial, orient="vertical", command=self.canvas_inicial.yview)
        self.frame_nombres_iniciales = ttk.Frame(self.canvas_inicial)
        
        self.frame_nombres_iniciales.bind(
            "<Configure>",
            lambda e: self.canvas_inicial.configure(scrollregion=self.canvas_inicial.bbox("all"))
        )
        
        self.frame_window_inicial = self.canvas_inicial.create_window((0, 0), window=self.frame_nombres_iniciales, anchor="nw")
        self.canvas_inicial.configure(yscrollcommand=scrollbar_inicial.set)
        
        self.canvas_inicial.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar_inicial.pack(side=tk.RIGHT, fill="y")
        
        # Frame para nombres finales con scroll
        self.canvas_final = tk.Canvas(frame_col_final, highlightthickness=0, height=255)  # Altura reducida
        scrollbar_final = ttk.Scrollbar(frame_col_final, orient="vertical", command=self.canvas_final.yview)
        self.frame_nombres_finales = ttk.Frame(self.canvas_final)
        
        self.frame_nombres_finales.bind(
            "<Configure>",
            lambda e: self.canvas_final.configure(scrollregion=self.canvas_final.bbox("all"))
        )
        
        self.frame_window_final = self.canvas_final.create_window((0, 0), window=self.frame_nombres_finales, anchor="nw")
        self.canvas_final.configure(yscrollcommand=scrollbar_final.set)
        
        self.canvas_final.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar_final.pack(side=tk.RIGHT, fill="y")
        
        # Actualizar campos de auxiliares
        self._actualizar_campos_auxiliares_iniciales()
        self._actualizar_campos_auxiliares_finales()
        
        # Vincular eventos de redimensionamiento
        self.canvas_inicial.bind("<Configure>", self._resize_canvas_inicial)
        self.canvas_final.bind("<Configure>", self._resize_canvas_final)
    
    def _actualizar_campos_auxiliares_iniciales(self):
        """Actualiza los campos de nombres de auxiliares según el número seleccionado."""
        # Limpiar frame actual
        for widget in self.frame_nombres_iniciales.winfo_children():
            widget.destroy()
        
        # Mostrar campos para cada auxiliar
        num_auxiliares = self.num_aux_inicial.get()
        self.entries_aux_inicial = {}  # Reiniciar diccionario de entries
        
        for i in range(1, num_auxiliares + 1):
            # Si no existe la variable para este auxiliar, crearla
            if i not in self.nombres_aux_inicial:
                self.nombres_aux_inicial[i] = tk.StringVar(value=f"Auxiliar {i}")
            
            # Crear frame para cada auxiliar
            frame_aux = ttk.Frame(self.frame_nombres_iniciales)
            frame_aux.pack(fill="x", pady=2)
            
            # Etiqueta y campo de entrada
            lbl_auxiliar = ttk.Label(frame_aux, text=f"Auxiliar {i}:")
            lbl_auxiliar.pack(side=tk.LEFT, padx=(5, 10))
            
            entry_auxiliar = ttk.Entry(frame_aux, textvariable=self.nombres_aux_inicial[i], width=30)
            entry_auxiliar.pack(side=tk.LEFT, fill="x", expand=True)
            
            # AÑADIDO: Trace para guardar configuración cuando cambie el nombre
            self.nombres_aux_inicial[i].trace_add("write", lambda *args, i=i: self._on_nombre_auxiliar_changed())
            
            # Guardar referencia al entry
            self.entries_aux_inicial[i] = entry_auxiliar
        
        # AÑADIDO: Guardar configuración cuando cambien los auxiliares
        self._guardar_configuracion_auxiliares()
    
    def _actualizar_campos_auxiliares_finales(self):
        """Actualiza los campos de nombres de auxiliares según el número seleccionado."""
        # Limpiar frame actual
        for widget in self.frame_nombres_finales.winfo_children():
            widget.destroy()
        
        # Mostrar campos para cada auxiliar
        num_auxiliares = self.num_aux_final.get()
        self.entries_aux_final = {}  # Reiniciar diccionario de entries
        
        for i in range(1, num_auxiliares + 1):
            # Si no existe la variable para este auxiliar, crearla
            if i not in self.nombres_aux_final:
                self.nombres_aux_final[i] = tk.StringVar(value=f"Auxiliar {i}")
            
            # Crear frame para cada auxiliar
            frame_aux = ttk.Frame(self.frame_nombres_finales)
            frame_aux.pack(fill="x", pady=2)
            
            # Etiqueta y campo de entrada
            lbl_auxiliar = ttk.Label(frame_aux, text=f"Auxiliar {i}:")
            lbl_auxiliar.pack(side=tk.LEFT, padx=(5, 10))
            
            entry_auxiliar = ttk.Entry(frame_aux, textvariable=self.nombres_aux_final[i], width=30)
            entry_auxiliar.pack(side=tk.LEFT, fill="x", expand=True)
            
            # AÑADIDO: Trace para guardar configuración cuando cambie el nombre
            self.nombres_aux_final[i].trace_add("write", lambda *args, i=i: self._on_nombre_auxiliar_changed())
            
            # Guardar referencia al entry
            self.entries_aux_final[i] = entry_auxiliar
        
        # AÑADIDO: Guardar configuración cuando cambien los auxiliares
        self._guardar_configuracion_auxiliares()
    
    def _guardar_configuracion_auxiliares(self):
        """Guarda la configuración actual de auxiliares en el archivo de configuración."""
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
            
            # Guardar configuración
            self.config_manager.save_auxiliares_iniciales(self.num_aux_inicial.get(), nombres_inicial)
            self.config_manager.save_auxiliares_finales(self.num_aux_final.get(), nombres_final)
            self.config_manager.save_opciones_duplicados(
                self.buscar_duplicados_correo.get(),
                self.buscar_duplicados_telefono.get(),
                self.eliminar_duplicados_antes.get()
            )
        except Exception as e:
            print(f"Error al guardar configuración: {e}")
    
    def _on_nombre_auxiliar_changed(self):
        """Callback para guardar configuración cuando cambie el nombre de un auxiliar."""
        self._guardar_configuracion_auxiliares()
    
    def _seleccionar_archivo(self):
        """Permite al usuario seleccionar un archivo Excel y lo valida."""
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=(("Archivos Excel", "*.xlsx *.xls"), ("Todos los archivos", "*.*"))
        )
        if archivo:
            self.ruta_archivo.set(archivo)
            self._validar_archivo(archivo)
    
    def _validar_archivo(self, ruta):
        """
        Valida el archivo Excel seleccionado.
        
        Args:
            ruta (str): Ruta al archivo a validar.
        """
        try:
            # Cargar y validar el archivo
            excel_manager = ExcelManager()
            df = excel_manager.cargar_archivo(ruta)
            
            # Verificar la estructura
            num_filas = len(df)
            df_validado, columna_correo, columna_fecha = excel_manager.validar_y_preparar_datos(df)
            
            # Identificar la columna de teléfono
            columna_telefono = utils.identificar_columna_telefono(df)
            
            # Mostrar resultados de la validación
            mensaje = f"Archivo válido. {num_filas} registros encontrados."
            if columna_correo:
                mensaje += f"\nColumna de correo: {columna_correo}"
            if columna_fecha:
                mensaje += f"\nColumna de fecha: {columna_fecha}"
            if columna_telefono:
                mensaje += f"\nColumna de teléfono: {columna_telefono}"
            else:
                mensaje += "\nNo se identificó columna de teléfono."
            
            self.mensaje_estado.set(mensaje)
        except Exception as e:
            messagebox.showerror("Error", f"Error al validar el archivo: {str(e)}")
            self.mensaje_estado.set("Error al validar archivo")
    
    def _configurar_frame_opciones(self, frame_principal):
        """Configura el frame de opciones de la aplicación."""
        frame_opciones = ttk.LabelFrame(frame_principal, text="Opciones de Duplicados", padding=(10, 8))  # Mismo padding que archivo
        frame_opciones.pack(fill="x", pady=3)  # Mismo espaciado que archivo
        
        # Checkbox para buscar duplicados por correo
        chk_duplicados_correo = ttk.Checkbutton(
            frame_opciones,
            text="Buscar duplicados por correo",
            variable=self.buscar_duplicados_correo
        )
        chk_duplicados_correo.pack(anchor="w", pady=2)
        
        # Checkbox para buscar duplicados por teléfono
        chk_duplicados_tel = ttk.Checkbutton(
            frame_opciones,
            text="Buscar duplicados por teléfono",
            variable=self.buscar_duplicados_telefono
        )
        chk_duplicados_tel.pack(anchor="w", pady=2)
        
        # Checkbox para eliminar duplicados antes de distribuir
        chk_eliminar_antes = ttk.Checkbutton(
            frame_opciones,
            text="Eliminar duplicados antes de distribuir (conservando solo padres)",
            variable=self.eliminar_duplicados_antes
        )
        chk_eliminar_antes.pack(anchor="w", pady=2)
    
    def _realizar_distribucion(self):
        """Valida las entradas y lanza el proceso de distribución en un hilo separado."""
        # Validar entradas
        archivo = self.ruta_archivo.get()
        nombres_auxiliares_iniciales = [self.nombres_aux_inicial[i].get().strip() for i in range(1, self.num_aux_inicial.get() + 1)]
        nombres_auxiliares_finales = [self.nombres_aux_final[i].get().strip() for i in range(1, self.num_aux_final.get() + 1)]
        
        if not archivo:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un archivo Excel")
            return
        
        if not all(nombres_auxiliares_iniciales):
            messagebox.showwarning("Advertencia", "Por favor, complete los nombres de todos los auxiliares iniciales")
            return
        
        if not all(nombres_auxiliares_finales):
            messagebox.showwarning("Advertencia", "Por favor, complete los nombres de todos los auxiliares finales")
            return
        
        # Lanzar proceso en un hilo separado para no bloquear la interfaz
        hilo = threading.Thread(target=self._procesar_distribucion)
        hilo.daemon = True
        hilo.start()
    
    def _procesar_distribucion(self):
        """Procesa la distribución de leads según la configuración seleccionada."""
        try:
            self.progreso.set(10)
            self.mensaje_estado.set("Cargando archivo...")
            self.root.update_idletasks()
            
            # Obtener configuración
            archivo = self.ruta_archivo.get()
            nombres_auxiliares_iniciales = self._obtener_nombres_auxiliares_iniciales()
            nombres_auxiliares_finales = self._obtener_nombres_auxiliares_finales()
            
            # Crear instancia del gestor de Excel
            excel_manager = ExcelManager()
            
            # Cargar y validar archivo Excel
            self.mensaje_estado.set("Validando archivo Excel...")
            self.progreso.set(20)
            self.root.update_idletasks()
            df = excel_manager.cargar_archivo(archivo)
            
            # Guardar una copia de los datos originales antes de cualquier modificación
            df_original = df.copy()
            
            # Identificar columnas necesarias
            self.mensaje_estado.set("Identificando columnas...")
            self.progreso.set(30)
            self.root.update_idletasks()
            columnas = utils.identificar_columnas(df)
            columna_correo = columnas.get("email", "")
            columna_telefono = columnas.get("phone", "")
            columna_fecha = columnas.get("fecha", "")
            
            df_duplicados_correo = pd.DataFrame()
            df_duplicados_telefono = pd.DataFrame()
            eliminados_principal = pd.DataFrame()  # Para almacenar registros eliminados
            
            if self.eliminar_duplicados_antes.get():
                self.mensaje_estado.set("Procesando duplicados antes de la distribución...")
                self.progreso.set(40)
                self.root.update_idletasks()
                
                # La identificación de duplicados para el reporte se hará más adelante
                # Aquí solo nos enfocamos en la eliminación si la opción está marcada
                
                # Aplicar eliminación de duplicados por correo si esa opción está marcada
                if self.buscar_duplicados_correo.get() and columna_correo and columna_fecha:
                    self.mensaje_estado.set("Eliminando duplicados por correo...")
                    self.root.update_idletasks()
                    df, eliminados_correo = excel_manager.eliminar_duplicados(df, columna_correo, columna_fecha)
                    # Agregar eliminados por correo al DataFrame de eliminados principal
                    if not eliminados_correo.empty:
                        eliminados_principal = pd.concat([eliminados_principal, eliminados_correo], ignore_index=True)
                
                # Aplicar eliminación de duplicados por teléfono si esa opción está marcada
                if self.buscar_duplicados_telefono.get() and columna_telefono and columna_fecha:
                    self.mensaje_estado.set("Eliminando duplicados por teléfono...")
                    self.root.update_idletasks()
                    df, eliminados_telefono = excel_manager.eliminar_duplicados(df, columna_telefono, columna_fecha)
                    # Agregar eliminados por teléfono al DataFrame de eliminados principal
                    if not eliminados_telefono.empty:
                        eliminados_principal = pd.concat([eliminados_principal, eliminados_telefono], ignore_index=True)
                
                # Eliminar duplicados dentro del propio DataFrame de eliminados si los hay
                if not eliminados_principal.empty:
                    eliminados_principal = eliminados_principal.drop_duplicates().reset_index(drop=True)
            
            # Ahora, independientemente de si se eliminaron o no, identificamos los duplicados
            # del dataframe original para los reportes.
            if self.buscar_duplicados_correo.get() and columna_correo and columna_fecha:
                self.mensaje_estado.set("Identificando duplicados por correo para reporte...")
                self.root.update_idletasks()
                df_duplicados_correo = excel_manager.procesar_duplicados_correo(
                    df_original, columna_correo, columna_fecha
                )

            if self.buscar_duplicados_telefono.get() and columna_telefono and columna_fecha:
                self.mensaje_estado.set("Identificando duplicados por teléfono para reporte...")
                self.root.update_idletasks()
                df_duplicados_telefono = excel_manager.procesar_duplicados_telefono(
                    df_original, columna_telefono, columna_fecha
                )

            # Ordenar por fecha (más recientes primero) el DF principal para la distribución
            self.mensaje_estado.set("Ordenando datos...")
            self.progreso.set(50)
            self.root.update_idletasks()
            if columna_fecha:
                df.sort_values(by=columna_fecha, ascending=False, inplace=True)
            
            # Generar distribuciones (inicial y final)
            self.mensaje_estado.set("Generando distribuciones...")
            self.progreso.set(55)
            self.root.update_idletasks()
            
            # Usar el nuevo método generar_distribuciones que implementa la lógica actualizada
            df = excel_manager.generar_distribuciones(
                df, 
                len(nombres_auxiliares_iniciales),
                len(nombres_auxiliares_finales),
                nombres_auxiliares_iniciales,
                nombres_auxiliares_finales
            )
            
            # Exportar resultados
            self.mensaje_estado.set("Exportando resultados...")
            self.progreso.set(90)
            self.root.update_idletasks()
            
            # Proponer un nombre de archivo de salida y abrir el diálogo para guardar
            nombre_base = os.path.splitext(os.path.basename(self.ruta_archivo.get()))[0]
            nombre_salida_sugerido = f"{nombre_base}_distribuido.xlsx"
            
            ruta_salida = filedialog.asksaveasfilename(
                initialfile=nombre_salida_sugerido,
                defaultextension=".xlsx",
                filetypes=[("Archivos de Excel", "*.xlsx"), ("Todos los archivos", "*.*")])

            # Si el usuario cancela, detener el proceso
            if not ruta_salida:
                self.mensaje_estado.set("Exportación cancelada.")
                self.progreso.set(0)
                return

            exito = ExcelManager.exportar_a_excel(df, df_duplicados_correo, df_duplicados_telefono, ruta_salida, eliminados_principal)
            
            self.progreso.set(100)
            self.mensaje_estado.set(f"¡Proceso completado! Archivo guardado.")
            
            # Preguntar al usuario si desea abrir el archivo exportado
            respuesta = messagebox.askquestion(
                "Proceso Completado",
                f"La distribución ha finalizado con éxito.\nArchivo guardado como: {ruta_salida}\n\n¿Desea abrir el archivo ahora?",
                icon="info"
            )
            
            if respuesta == "yes":
                utils.abrir_archivo(ruta_salida)
                
        except Exception as e:
            messagebox.showerror("Error en la distribución", str(e))
    
    def _obtener_nombres_auxiliares_iniciales(self):
        """Obtiene la lista de nombres de auxiliares iniciales."""
        nombres = []
        for i in range(1, self.num_aux_inicial.get() + 1):
            nombre = self.nombres_aux_inicial[i].get().strip()
            if nombre:
                nombres.append(nombre)
        return nombres
        
    def _obtener_nombres_auxiliares_finales(self):
        """Obtiene la lista de nombres de auxiliares finales."""
        nombres = []
        for i in range(1, self.num_aux_final.get() + 1):
            nombre = self.nombres_aux_final[i].get().strip()
            if nombre:
                nombres.append(nombre)
        return nombres
    
    def _resize_canvas_inicial(self, event):
        """Ajusta el tamaño del canvas de auxiliares iniciales."""
        canvas_width = event.width
        self.canvas_inicial.itemconfig(self.frame_window_inicial, width=canvas_width)
    
    def _resize_canvas_final(self, event):
        """Ajusta el tamaño del canvas de auxiliares finales."""
        canvas_width = event.width
        self.canvas_final.itemconfig(self.frame_window_final, width=canvas_width)

    def _abrir_changelog(self):
        """Abre una ventana con el contenido del changelog."""
        try:
            # Determinar la ruta correcta del archivo CHANGELOG.md
            if getattr(sys, 'frozen', False):
                # Si estamos en un ejecutable empaquetado
                base_path = sys._MEIPASS
                changelog_path = os.path.join(base_path, 'CHANGELOG.md')
            else:
                # Si estamos ejecutando desde código fuente
                changelog_path = "CHANGELOG.md"
            
            # Leer el contenido del archivo
            with open(changelog_path, "r", encoding="utf-8") as file:
                contenido = file.read()
            
            # Crear ventana secundaria
            ventana_changelog = tk.Toplevel(self.root)
            ventana_changelog.title("Historial de Cambios - SOFASA Distribución de Leads")
            ventana_changelog.geometry("800x600")
            ventana_changelog.minsize(600, 400)
            
            # Configurar icono (mismo que la ventana principal si existe)
            try:
                ventana_changelog.iconbitmap(self.root.iconbitmap())
            except:
                pass  # Si no hay icono, continuar sin él
            
            # Frame principal con scrollbar
            frame_principal = ttk.Frame(ventana_changelog)
            frame_principal.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Crear Text widget con scrollbar
            text_widget = tk.Text(
                frame_principal,
                wrap=tk.WORD,
                font=("Consolas", 10),
                bg="white",
                fg="black",
                padx=10,
                pady=10
            )
            
            # Scrollbar vertical
            scrollbar = ttk.Scrollbar(frame_principal, orient="vertical", command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
            
            # Empaquetar widgets
            scrollbar.pack(side="right", fill="y")
            text_widget.pack(side="left", fill="both", expand=True)
            
            # Insertar contenido
            text_widget.insert("1.0", contenido)
            text_widget.config(state="disabled")  # Solo lectura
            
            # Frame para botones
            frame_botones = ttk.Frame(ventana_changelog)
            frame_botones.pack(fill="x", padx=10, pady=(0, 10))
            
            # Botón cerrar
            btn_cerrar = ttk.Button(
                frame_botones,
                text="Cerrar",
                command=ventana_changelog.destroy
            )
            btn_cerrar.pack(side="right")
            
            # Centrar la ventana
            ventana_changelog.transient(self.root)  # Mantener encima de la ventana principal
            ventana_changelog.grab_set()  # Modal
            
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró el archivo CHANGELOG.md en la ruta: {changelog_path if 'changelog_path' in locals() else 'CHANGELOG.md'}")
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

    def _configurar_icono(self):
        """Configura el icono de la ventana principal."""
        try:
            # Determinar la ruta correcta del archivo icono
            if getattr(sys, 'frozen', False):
                # Si estamos en un ejecutable empaquetado
                base_path = sys._MEIPASS
                icono_path = os.path.join(base_path, 'ICONOS', 'Renault_2021.ico')
            else:
                # Si estamos ejecutando desde código fuente
                icono_path = os.path.join("ICONOS", "Renault_2021.ico")
            
            # Configurar icono
            self.root.iconbitmap(icono_path)
        except Exception as e:
            print(f"No se pudo cargar el icono: {e}")  # Para debug
            pass  # Si no hay icono, continuar sin él


def main():
    """Función principal para iniciar la aplicación."""
    try:
        root = tk.Tk()
        app = AplicacionDistribucionLeads(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error crítico", f"Error al iniciar la aplicación: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
