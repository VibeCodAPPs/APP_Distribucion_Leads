#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicación MODERNA para distribución de leads entre auxiliares
Versión modernizada usando CustomTkinter para una interfaz más atractiva.
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
    
    Esta versión utiliza CustomTkinter para una interfaz más moderna y atractiva.
    
    Funcionalidades:
    - Cargar un archivo Excel con leads
    - Distribuir los leads entre 2 o 3 auxiliares
    - Detectar duplicados por correo y teléfono
    - Exportar resultados a un archivo Excel
    - Interfaz moderna y responsive
    """
    
    def __init__(self, root=None):
        """Inicializa la aplicación moderna."""
        # Configurar tema moderno
        ModernUIStyles.configurar_tema()
        
        # Configuración de la ventana principal
        self.root = root or ctk.CTk()
        self.root.title("SOFASA - Distribución de Leads v3.0 (UI Moderna)")
        self.root.geometry("1000x600")  # Tamaño más grande para mejor experiencia
        self.root.minsize(900, 550)
        
        # Configurar icono de la ventana
        self._configurar_icono()
        
        # Inicializar gestor de configuración
        self.config_manager = ConfigManager()
        
        # Variables de la aplicación
        self._inicializar_variables()
        
        # Crear la interfaz moderna
        self._crear_interfaz_moderna()
        
        # Cargar configuración guardada
        self._cargar_configuracion()
        
        # Configurar el cierre de la aplicación
        self.root.protocol("WM_DELETE_WINDOW", self.salir_aplicacion)
        
        # Centrar ventana
        self._centrar_ventana()
    
    def _configurar_icono(self):
        """Configura el icono de la ventana."""
        try:
            icono_path = os.path.join(os.path.dirname(__file__), "ICONOS", "icono.ico")
            if os.path.exists(icono_path):
                self.root.iconbitmap(icono_path)
        except Exception:
            pass  # Si no se puede cargar el icono, continuar sin él
    
    def _inicializar_variables(self):
        """Inicializa todas las variables de la aplicación."""
        # Variables para archivo
        self.archivo_seleccionado = tk.StringVar()
        self.mensaje_estado_archivo = tk.StringVar()
        self.mensaje_estado_archivo.set("No se ha seleccionado ningún archivo")
        
        # Variables para auxiliares
        self.num_auxiliares = tk.IntVar(value=2)
        self.nombre_aux1 = tk.StringVar()
        self.nombre_aux2 = tk.StringVar()
        self.nombre_aux3 = tk.StringVar()
        
        # Variables para opciones de duplicados
        self.detectar_duplicados_correo = tk.BooleanVar(value=True)
        self.detectar_duplicados_telefono = tk.BooleanVar(value=True)
        self.eliminar_duplicados_antes = tk.BooleanVar(value=False)
        
        # Variables para estado y progreso
        self.mensaje_estado = tk.StringVar()
        self.mensaje_estado.set("Listo para procesar archivo Excel")
        self.progreso = tk.DoubleVar()
        
        # Variables de control
        self.excel_manager = None
        self.procesando = False
    
    def _crear_interfaz_moderna(self):
        """Crea la interfaz moderna usando CustomTkinter."""
        # Frame principal con esquinas redondeadas
        self.frame_principal = ModernUIComponentFactory.crear_frame_principal(self.root, padding=20)
        
        # Título principal
        ModernUIComponentFactory.crear_titulo(
            self.frame_principal, 
            "SOFASA - Distribución de Leads"
        )
        
        # Frame para selección de archivo
        self.frame_archivo = ModernUIComponentFactory.crear_frame_archivo(
            self.frame_principal,
            self.archivo_seleccionado,
            self.seleccionar_archivo,
            self.mensaje_estado_archivo
        )
        
        # Frame para configuración de auxiliares
        componentes_aux3 = ModernUIComponentFactory.crear_frame_auxiliares(
            self.frame_principal,
            self.num_auxiliares,
            self.nombre_aux1,
            self.nombre_aux2,
            self.nombre_aux3,
            self.detectar_duplicados_correo,
            self.detectar_duplicados_telefono,
            self.eliminar_duplicados_antes,
            self.actualizar_campos_auxiliares
        )
        
        # Guardar referencias a componentes del auxiliar 3
        self.frame_aux3 = componentes_aux3['frame_aux3']
        self.label_aux3 = componentes_aux3['label_aux3']
        self.entry_aux3 = componentes_aux3['entry_aux3']
        
        # Frame para botones de acción
        self.frame_acciones = ModernUIComponentFactory.crear_frame_acciones(
            self.frame_principal,
            self.distribuir_leads,
            self.salir_aplicacion
        )
        
        # Frame para estado y progreso
        self.frame_estado = ModernUIComponentFactory.crear_frame_estado(
            self.frame_principal,
            self.mensaje_estado,
            self.progreso
        )
        
        # Actualizar campos iniciales
        self.actualizar_campos_auxiliares()
    
    def _centrar_ventana(self):
        """Centra la ventana en la pantalla."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def seleccionar_archivo(self):
        """Abre el diálogo para seleccionar archivo Excel."""
        try:
            archivo = filedialog.askopenfilename(
                title="Seleccionar archivo Excel",
                filetypes=[
                    ("Archivos Excel", "*.xlsx *.xls"),
                    ("Todos los archivos", "*.*")
                ]
            )
            
            if archivo:
                self.archivo_seleccionado.set(archivo)
                self._validar_archivo(archivo)
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al seleccionar archivo: {str(e)}")
    
    def _validar_archivo(self, archivo):
        """Valida el archivo seleccionado."""
        try:
            # Crear ExcelManager para validar
            self.excel_manager = ExcelManager(archivo)
            
            # Obtener información del archivo
            info = self.excel_manager.obtener_info_archivo()
            
            mensaje = f"✅ Archivo válido: {info['filas']} filas, {info['columnas']} columnas"
            self.mensaje_estado_archivo.set(mensaje)
            
            # Actualizar mensaje de estado general
            self.mensaje_estado.set("Archivo cargado correctamente. Listo para distribuir.")
            
        except Exception as e:
            self.mensaje_estado_archivo.set(f"❌ Error: {str(e)}")
            self.mensaje_estado.set("Error al cargar el archivo. Selecciona un archivo válido.")
            self.excel_manager = None
    
    def actualizar_campos_auxiliares(self):
        """Actualiza la visibilidad de los campos según el número de auxiliares."""
        if self.num_auxiliares.get() == 3:
            self.frame_aux3.pack(fill="x", pady=(0, 10))
        else:
            self.frame_aux3.pack_forget()
    
    def distribuir_leads(self):
        """Inicia el proceso de distribución de leads."""
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
        if not self.excel_manager:
            messagebox.showerror("Error", "Primero selecciona un archivo Excel válido.")
            return False
        
        if not self.nombre_aux1.get().strip():
            messagebox.showerror("Error", "Ingresa el nombre del Auxiliar 1.")
            return False
        
        if not self.nombre_aux2.get().strip():
            messagebox.showerror("Error", "Ingresa el nombre del Auxiliar 2.")
            return False
        
        if self.num_auxiliares.get() == 3 and not self.nombre_aux3.get().strip():
            messagebox.showerror("Error", "Ingresa el nombre del Auxiliar 3.")
            return False
        
        return True
    
    def _procesar_distribucion(self):
        """Procesa la distribución de leads en hilo separado."""
        try:
            # Actualizar estado
            self.mensaje_estado.set("🔄 Iniciando procesamiento...")
            self.progreso.set(0.1)
            
            # Configurar parámetros
            nombres_auxiliares = [self.nombre_aux1.get().strip(), self.nombre_aux2.get().strip()]
            if self.num_auxiliares.get() == 3:
                nombres_auxiliares.append(self.nombre_aux3.get().strip())
            
            opciones = {
                'detectar_duplicados_correo': self.detectar_duplicados_correo.get(),
                'detectar_duplicados_telefono': self.detectar_duplicados_telefono.get(),
                'eliminar_duplicados_antes': self.eliminar_duplicados_antes.get()
            }
            
            # Procesar distribución
            self.mensaje_estado.set("📊 Analizando datos...")
            self.progreso.set(0.3)
            
            resultado = self.excel_manager.distribuir_leads(
                nombres_auxiliares,
                opciones,
                callback_progreso=self._actualizar_progreso
            )
            
            # Guardar archivo
            self.mensaje_estado.set("💾 Guardando archivo...")
            self.progreso.set(0.9)
            
            archivo_salida = self._generar_nombre_archivo_salida()
            self.excel_manager.guardar_resultado(archivo_salida)
            
            # Completado
            self.progreso.set(1.0)
            self.mensaje_estado.set(f"✅ Proceso completado. Archivo guardado: {os.path.basename(archivo_salida)}")
            
            # Mostrar resumen
            self._mostrar_resumen_resultado(resultado, archivo_salida)
            
        except Exception as e:
            self.mensaje_estado.set(f"❌ Error durante el procesamiento: {str(e)}")
            messagebox.showerror("Error", f"Error durante el procesamiento:\n{str(e)}")
        
        finally:
            self.procesando = False
    
    def _actualizar_progreso(self, valor, mensaje=""):
        """Callback para actualizar el progreso."""
        self.progreso.set(valor)
        if mensaje:
            self.mensaje_estado.set(mensaje)
    
    def _generar_nombre_archivo_salida(self):
        """Genera el nombre del archivo de salida."""
        archivo_original = self.archivo_seleccionado.get()
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

👥 Distribución por auxiliar:
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
        try:
            config = self.config_manager.cargar_configuracion()
            
            # Cargar nombres de auxiliares
            if 'auxiliares' in config:
                aux_config = config['auxiliares']
                self.nombre_aux1.set(aux_config.get('auxiliar1', ''))
                self.nombre_aux2.set(aux_config.get('auxiliar2', ''))
                self.nombre_aux3.set(aux_config.get('auxiliar3', ''))
                self.num_auxiliares.set(aux_config.get('num_auxiliares', 2))
            
            # Cargar opciones de duplicados
            if 'opciones' in config:
                opt_config = config['opciones']
                self.detectar_duplicados_correo.set(opt_config.get('detectar_duplicados_correo', True))
                self.detectar_duplicados_telefono.set(opt_config.get('detectar_duplicados_telefono', True))
                self.eliminar_duplicados_antes.set(opt_config.get('eliminar_duplicados_antes', False))
            
            # Actualizar campos
            self.actualizar_campos_auxiliares()
            
        except Exception as e:
            print(f"Error al cargar configuración: {e}")
    
    def _guardar_configuracion(self):
        """Guarda la configuración actual."""
        try:
            config = {
                'auxiliares': {
                    'auxiliar1': self.nombre_aux1.get(),
                    'auxiliar2': self.nombre_aux2.get(),
                    'auxiliar3': self.nombre_aux3.get(),
                    'num_auxiliares': self.num_auxiliares.get()
                },
                'opciones': {
                    'detectar_duplicados_correo': self.detectar_duplicados_correo.get(),
                    'detectar_duplicados_telefono': self.detectar_duplicados_telefono.get(),
                    'eliminar_duplicados_antes': self.eliminar_duplicados_antes.get()
                }
            }
            
            self.config_manager.guardar_configuracion(config)
            
        except Exception as e:
            print(f"Error al guardar configuración: {e}")
    
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
        self._guardar_configuracion()
        
        # Cerrar aplicación
        self.root.quit()
        self.root.destroy()
    
    def ejecutar(self):
        """Inicia el bucle principal de la aplicación."""
        self.root.mainloop()


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
