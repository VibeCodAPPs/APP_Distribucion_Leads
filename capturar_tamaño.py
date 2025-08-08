#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para capturar el tamaño ideal de la ventana de la aplicación moderna.
Muestra la aplicación real y permite redimensionarla manualmente para encontrar el tamaño perfecto.
"""

import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import os
import sys
import threading
import time

# Agregar el directorio actual al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar la aplicación moderna
try:
    from app_moderna import AplicacionDistribucionLeadsModerna
except ImportError as e:
    print(f"Error al importar la aplicación moderna: {e}")
    print("Asegúrate de que app_moderna.py esté en el mismo directorio.")
    sys.exit(1)

class CapturadorTamaño:
    def __init__(self):
        self.app_moderna = None
        self.monitor_activo = False
        self.dimensiones_actuales = {"ancho": 1000, "alto": 700}
        
        # Crear ventana de control
        self.control_window = tk.Tk()
        self.control_window.title("Capturador de Tamaño - UI Moderna")
        self.control_window.geometry("350x400")
        self.control_window.resizable(False, False)
        
        # Posicionar ventana de control en la esquina superior izquierda
        self.control_window.geometry("+50+50")
        
        self._crear_interfaz_control()
        
    def _crear_interfaz_control(self):
        """Crea la interfaz de control."""
        # Título
        titulo = tk.Label(
            self.control_window,
            text="Capturador de Tamaño UI Moderna",
            font=("Arial", 14, "bold"),
            fg="blue"
        )
        titulo.pack(pady=20)
        
        # Frame principal
        frame_principal = tk.Frame(self.control_window)
        frame_principal.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Instrucciones
        instrucciones = tk.Label(
            frame_principal,
            text="INSTRUCCIONES:",
            font=("Arial", 11, "bold"),
            fg="darkgreen"
        )
        instrucciones.pack(anchor="w", pady=(0, 5))
        
        texto_instrucciones = tk.Label(
            frame_principal,
            text="1. Haz clic en 'Abrir App Moderna'\n"
                 "2. Redimensiona la ventana arrastrando\n"
                 "   las esquinas hasta que se vea perfecta\n"
                 "3. Haz clic en 'Capturar Tamaño Actual'\n"
                 "4. Confirma para aplicar los cambios",
            font=("Arial", 9),
            justify="left",
            fg="black"
        )
        texto_instrucciones.pack(anchor="w", pady=(0, 15))
        
        # Botón para abrir la aplicación moderna
        self.btn_abrir = tk.Button(
            frame_principal,
            text="🚀 Abrir App Moderna",
            command=self._abrir_app_moderna,
            font=("Arial", 11, "bold"),
            bg="lightgreen",
            fg="black",
            height=2,
            width=25
        )
        self.btn_abrir.pack(pady=10)
        
        # Frame para información en tiempo real
        info_frame = tk.LabelFrame(frame_principal, text="Dimensiones en Tiempo Real", font=("Arial", 10, "bold"))
        info_frame.pack(fill="x", pady=15)
        
        self.label_dimensiones = tk.Label(
            info_frame,
            text="Ventana: No abierta",
            font=("Arial", 10),
            fg="red"
        )
        self.label_dimensiones.pack(pady=10)
        
        # Botón para capturar tamaño
        self.btn_capturar = tk.Button(
            frame_principal,
            text="📏 Capturar Tamaño Actual",
            command=self._capturar_tamaño,
            font=("Arial", 11, "bold"),
            bg="lightblue",
            fg="black",
            height=2,
            width=25,
            state="disabled"
        )
        self.btn_capturar.pack(pady=10)
        
        # Frame para tamaño capturado
        captura_frame = tk.LabelFrame(frame_principal, text="Tamaño Capturado", font=("Arial", 10, "bold"))
        captura_frame.pack(fill="x", pady=15)
        
        self.label_capturado = tk.Label(
            captura_frame,
            text="Ningún tamaño capturado",
            font=("Arial", 10),
            fg="gray"
        )
        self.label_capturado.pack(pady=10)
        
        # Botón para aplicar cambios
        self.btn_aplicar = tk.Button(
            frame_principal,
            text="✅ Aplicar Cambios",
            command=self._aplicar_cambios,
            font=("Arial", 11, "bold"),
            bg="orange",
            fg="black",
            height=2,
            width=25,
            state="disabled"
        )
        self.btn_aplicar.pack(pady=10)
        
        # Botón para cerrar
        btn_cerrar = tk.Button(
            frame_principal,
            text="❌ Cerrar Todo",
            command=self._cerrar_todo,
            font=("Arial", 10),
            bg="lightcoral",
            fg="black",
            width=25
        )
        btn_cerrar.pack(pady=(20, 10))
        
    def _abrir_app_moderna(self):
        """Abre la aplicación moderna real."""
        try:
            # Crear la aplicación moderna
            self.app_moderna = AplicacionDistribucionLeadsModerna()
            
            # Hacer la ventana redimensionable
            self.app_moderna.root.resizable(True, True)
            
            # Posicionar la ventana de la app a la derecha de la ventana de control
            self.app_moderna.root.geometry("1000x700+450+50")
            
            # Actualizar botones
            self.btn_abrir.config(state="disabled", text="✅ App Abierta")
            self.btn_capturar.config(state="normal")
            
            # Iniciar monitoreo de dimensiones
            self.monitor_activo = True
            self._iniciar_monitoreo()
            
            # Configurar cierre de la app
            def on_app_close():
                self.monitor_activo = False
                self.btn_abrir.config(state="normal", text="🚀 Abrir App Moderna")
                self.btn_capturar.config(state="disabled")
                self.label_dimensiones.config(text="Ventana: Cerrada", fg="red")
                self.app_moderna = None
                
            self.app_moderna.root.protocol("WM_DELETE_WINDOW", on_app_close)
            
            # Mostrar mensaje de éxito
            messagebox.showinfo(
                "App Abierta",
                "La aplicación moderna se ha abierto correctamente.\n\n"
                "Ahora puedes redimensionarla arrastrando las esquinas\n"
                "hasta encontrar el tamaño perfecto.\n\n"
                "Las dimensiones se actualizan en tiempo real."
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir la aplicación moderna: {str(e)}")
            
    def _iniciar_monitoreo(self):
        """Inicia el monitoreo de dimensiones en tiempo real."""
        def monitorear():
            while self.monitor_activo and self.app_moderna:
                try:
                    # Obtener dimensiones actuales
                    self.app_moderna.root.update_idletasks()
                    ancho = self.app_moderna.root.winfo_width()
                    alto = self.app_moderna.root.winfo_height()
                    
                    # Actualizar dimensiones
                    self.dimensiones_actuales = {"ancho": ancho, "alto": alto}
                    
                    # Actualizar label
                    self.label_dimensiones.config(
                        text=f"Ventana: {ancho}x{alto}",
                        fg="green"
                    )
                    
                    time.sleep(0.5)  # Actualizar cada 0.5 segundos
                    
                except:
                    break
                    
        # Ejecutar en hilo separado
        thread = threading.Thread(target=monitorear, daemon=True)
        thread.start()
        
    def _capturar_tamaño(self):
        """Captura el tamaño actual de la ventana."""
        if not self.app_moderna:
            messagebox.showerror("Error", "La aplicación moderna no está abierta.")
            return
            
        try:
            # Obtener dimensiones actuales
            self.app_moderna.root.update_idletasks()
            ancho = self.app_moderna.root.winfo_width()
            alto = self.app_moderna.root.winfo_height()
            
            # Actualizar dimensiones capturadas
            self.dimensiones_capturadas = {"ancho": ancho, "alto": alto}
            
            # Actualizar label
            self.label_capturado.config(
                text=f"Capturado: {ancho}x{alto}",
                fg="blue"
            )
            
            # Habilitar botón de aplicar
            self.btn_aplicar.config(state="normal")
            
            # Mostrar confirmación
            messagebox.showinfo(
                "Tamaño Capturado",
                f"Tamaño capturado exitosamente:\n\n"
                f"Ancho: {ancho} píxeles\n"
                f"Alto: {alto} píxeles\n\n"
                f"Haz clic en 'Aplicar Cambios' para guardar\n"
                f"estas dimensiones en la aplicación."
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al capturar tamaño: {str(e)}")
            
    def _aplicar_cambios(self):
        """Aplica los cambios capturados a los archivos."""
        if not hasattr(self, 'dimensiones_capturadas'):
            messagebox.showerror("Error", "No hay dimensiones capturadas.")
            return
            
        ancho = self.dimensiones_capturadas["ancho"]
        alto = self.dimensiones_capturadas["alto"]
        
        # Calcular altura del área de auxiliares proporcionalmente
        # Si la ventana original era 700px con auxiliares de 320px
        # Calcular nueva altura de auxiliares manteniendo proporción
        altura_auxiliares_original = 320
        altura_ventana_original = 700
        proporcion = altura_auxiliares_original / altura_ventana_original
        nueva_altura_auxiliares = int(alto * proporcion)
        
        # Asegurar que esté en un rango razonable
        nueva_altura_auxiliares = max(200, min(400, nueva_altura_auxiliares))
        
        respuesta = messagebox.askyesno(
            "Confirmar Cambios",
            f"¿Aplicar estos cambios a la aplicación moderna?\n\n"
            f"• Ventana: {ancho}x{alto}\n"
            f"• Área auxiliares: {nueva_altura_auxiliares}px\n"
            f"  (calculada proporcionalmente)\n\n"
            f"Esto modificará los archivos:\n"
            f"- app_moderna.py\n"
            f"- ui_components_modern.py",
            icon='question'
        )
        
        if respuesta:
            try:
                self._modificar_archivos(ancho, alto, nueva_altura_auxiliares)
                messagebox.showinfo(
                    "Cambios Aplicados",
                    f"¡Cambios aplicados correctamente!\n\n"
                    f"• Ventana: {ancho}x{alto}\n"
                    f"• Auxiliares: {nueva_altura_auxiliares}px\n\n"
                    f"Puedes cerrar este capturador y probar\n"
                    f"la aplicación moderna con las nuevas dimensiones."
                )
                
                # Deshabilitar botón
                self.btn_aplicar.config(state="disabled")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al aplicar cambios: {str(e)}")
                
    def _modificar_archivos(self, ancho, alto, altura_auxiliares):
        """Modifica los archivos con las nuevas dimensiones."""
        # Modificar app_moderna.py
        app_path = "app_moderna.py"
        if os.path.exists(app_path):
            with open(app_path, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Reemplazar dimensiones de ventana
            import re
            
            # Buscar y reemplazar geometry
            contenido = re.sub(
                r'self\.root\.geometry\("1000x\d+"\)',
                f'self.root.geometry("{ancho}x{alto}")',
                contenido
            )
            
            # Buscar y reemplazar minsize
            contenido = re.sub(
                r'self\.root\.minsize\(1000, \d+\)',
                f'self.root.minsize({ancho}, {alto})',
                contenido
            )
            
            with open(app_path, 'w', encoding='utf-8') as f:
                f.write(contenido)
        
        # Modificar ui_components_modern.py
        ui_path = "ui_components_modern.py"
        if os.path.exists(ui_path):
            with open(ui_path, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Reemplazar altura de auxiliares
            contenido = re.sub(
                r'ctk\.CTkScrollableFrame\(frame_inicial, height=\d+\)',
                f'ctk.CTkScrollableFrame(frame_inicial, height={altura_auxiliares})',
                contenido
            )
            contenido = re.sub(
                r'ctk\.CTkScrollableFrame\(frame_final, height=\d+\)',
                f'ctk.CTkScrollableFrame(frame_final, height={altura_auxiliares})',
                contenido
            )
            
            with open(ui_path, 'w', encoding='utf-8') as f:
                f.write(contenido)
                
    def _cerrar_todo(self):
        """Cierra todo y termina el programa."""
        self.monitor_activo = False
        
        if self.app_moderna:
            try:
                self.app_moderna.root.destroy()
            except:
                pass
                
        self.control_window.destroy()
        
    def ejecutar(self):
        """Ejecuta el capturador."""
        # Configurar cierre
        self.control_window.protocol("WM_DELETE_WINDOW", self._cerrar_todo)
        
        # Mostrar instrucciones iniciales
        messagebox.showinfo(
            "Capturador de Tamaño",
            "¡Bienvenido al Capturador de Tamaño!\n\n"
            "Este script te permite:\n"
            "1. Abrir la aplicación moderna REAL\n"
            "2. Redimensionarla manualmente\n"
            "3. Capturar el tamaño perfecto\n"
            "4. Aplicar los cambios automáticamente\n\n"
            "Haz clic en 'Abrir App Moderna' para comenzar."
        )
        
        # Iniciar bucle principal
        self.control_window.mainloop()

def main():
    """Función principal."""
    print("Iniciando Capturador de Tamaño UI Moderna...")
    
    try:
        capturador = CapturadorTamaño()
        capturador.ejecutar()
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Error Fatal", f"Error al iniciar el capturador: {str(e)}")

if __name__ == "__main__":
    main()
