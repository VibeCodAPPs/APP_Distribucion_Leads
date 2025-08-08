#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script interactivo para ajustar la altura ideal de la ventana y área de auxiliares.
Permite probar diferentes dimensiones en tiempo real antes de aplicarlas a la aplicación final.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import os
import sys

# Configurar CustomTkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class AjustadorAltura:
    def __init__(self):
        # Ventana principal de control
        self.control_window = tk.Tk()
        self.control_window.title("Ajustador de Altura - UI Moderna")
        self.control_window.geometry("400x300")
        self.control_window.resizable(False, False)
        
        # Variables para las dimensiones
        self.altura_ventana = tk.IntVar(value=700)  # Altura actual
        self.altura_auxiliares = tk.IntVar(value=320)  # Altura actual del área de auxiliares
        
        # Ventana de prueba (se creará después)
        self.test_window = None
        
        self._crear_interfaz_control()
        self._crear_ventana_prueba()
        
    def _crear_interfaz_control(self):
        """Crea la interfaz de control con sliders."""
        # Título
        titulo = ttk.Label(
            self.control_window,
            text="Ajustador de Altura UI Moderna",
            font=("Arial", 14, "bold")
        )
        titulo.pack(pady=20)
        
        # Frame principal
        frame_principal = ttk.Frame(self.control_window)
        frame_principal.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Control de altura de ventana
        ttk.Label(frame_principal, text="Altura de la Ventana:", font=("Arial", 11, "bold")).pack(anchor="w", pady=(0, 5))
        
        frame_ventana = ttk.Frame(frame_principal)
        frame_ventana.pack(fill="x", pady=(0, 15))
        
        self.slider_ventana = ttk.Scale(
            frame_ventana,
            from_=500,
            to=900,
            orient="horizontal",
            variable=self.altura_ventana,
            command=self._actualizar_ventana
        )
        self.slider_ventana.pack(side="left", fill="x", expand=True)
        
        self.label_ventana = ttk.Label(frame_ventana, text="700px", width=8)
        self.label_ventana.pack(side="right", padx=(10, 0))
        
        # Control de altura del área de auxiliares
        ttk.Label(frame_principal, text="Altura del Área de Auxiliares:", font=("Arial", 11, "bold")).pack(anchor="w", pady=(0, 5))
        
        frame_auxiliares = ttk.Frame(frame_principal)
        frame_auxiliares.pack(fill="x", pady=(0, 15))
        
        self.slider_auxiliares = ttk.Scale(
            frame_auxiliares,
            from_=200,
            to=400,
            orient="horizontal",
            variable=self.altura_auxiliares,
            command=self._actualizar_auxiliares
        )
        self.slider_auxiliares.pack(side="left", fill="x", expand=True)
        
        self.label_auxiliares = ttk.Label(frame_auxiliares, text="320px", width=8)
        self.label_auxiliares.pack(side="right", padx=(10, 0))
        
        # Botones de acción
        frame_botones = ttk.Frame(frame_principal)
        frame_botones.pack(fill="x", pady=20)
        
        ttk.Button(
            frame_botones,
            text="Resetear",
            command=self._resetear_valores
        ).pack(side="left", padx=(0, 10))
        
        ttk.Button(
            frame_botones,
            text="Aplicar Cambios",
            command=self._aplicar_cambios
        ).pack(side="right")
        
        # Información actual
        info_frame = ttk.LabelFrame(frame_principal, text="Dimensiones Actuales", padding=10)
        info_frame.pack(fill="x", pady=(10, 0))
        
        self.info_label = ttk.Label(
            info_frame,
            text="Ventana: 1000x700 | Auxiliares: 320px",
            font=("Arial", 9)
        )
        self.info_label.pack()
        
    def _crear_ventana_prueba(self):
        """Crea la ventana de prueba con la UI moderna."""
        self.test_window = ctk.CTk()
        self.test_window.title("Vista Previa - UI Moderna")
        self.test_window.geometry("1000x700")
        self.test_window.minsize(1000, 500)
        
        # Posicionar ventana de prueba a la derecha de la ventana de control
        self.test_window.geometry("+450+100")
        
        # Crear estructura básica de la UI
        self._crear_estructura_prueba()
        
        # Actualizar labels iniciales
        self._actualizar_labels()
        
    def _crear_estructura_prueba(self):
        """Crea la estructura básica de la UI para pruebas."""
        # Footer
        footer_frame = ctk.CTkFrame(self.test_window, height=40, corner_radius=0, fg_color=("gray85", "gray25"))
        footer_frame.pack(fill="x", side="bottom", pady=(5, 0))
        footer_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            footer_frame,
            text="Ver Historial de Cambios",
            font=ctk.CTkFont(size=12, underline=True),
            text_color="black"
        ).pack(side="left", padx=10, pady=8)
        
        ctk.CTkLabel(
            footer_frame,
            text="José Manuel de la Colina (Diseño y desarrollo) - jose.de-la-colina@renault.com",
            font=ctk.CTkFont(size=10, underline=True),
            text_color="black"
        ).pack(side="right", padx=10, pady=8)
        
        # Frame principal
        frame_principal = ctk.CTkFrame(self.test_window)
        frame_principal.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Título
        ctk.CTkLabel(
            frame_principal,
            text="Distribución de Leads (Vista Previa)",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(15, 10))
        
        # Frame de contenido con dos columnas
        frame_contenido = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_contenido.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Columna izquierda (controles)
        frame_izquierdo = ctk.CTkFrame(frame_contenido, width=400)
        frame_izquierdo.pack(side="left", fill="y", padx=(0, 10))
        frame_izquierdo.pack_propagate(False)
        
        ctk.CTkLabel(frame_izquierdo, text="Selección de Archivo", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        ctk.CTkButton(frame_izquierdo, text="Seleccionar archivo Excel", height=35).pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(frame_izquierdo, text="Opciones", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(20, 10))
        ctk.CTkCheckBox(frame_izquierdo, text="Eliminar duplicados por correo").pack(padx=10, pady=2)
        ctk.CTkCheckBox(frame_izquierdo, text="Eliminar duplicados por teléfono").pack(padx=10, pady=2)
        ctk.CTkCheckBox(frame_izquierdo, text="Procesar duplicados").pack(padx=10, pady=2)
        
        # Columna derecha (auxiliares)
        frame_derecho = ctk.CTkFrame(frame_contenido)
        frame_derecho.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Frame de auxiliares
        self.frame_auxiliares = ctk.CTkFrame(frame_derecho, corner_radius=10)
        self.frame_auxiliares.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            self.frame_auxiliares,
            text="Configuración de Auxiliares",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10))
        
        # Frame para las dos columnas de auxiliares
        self.frame_aux_contenedor = ctk.CTkFrame(self.frame_auxiliares, fg_color="transparent")
        self.frame_aux_contenedor.pack(fill="both", expand=True, padx=15, pady=10)
        self.frame_aux_contenedor.grid_columnconfigure(0, weight=1)
        self.frame_aux_contenedor.grid_columnconfigure(1, weight=1)
        
        self._crear_columnas_auxiliares()
        
    def _crear_columnas_auxiliares(self):
        """Crea las columnas de auxiliares con la altura actual."""
        # Limpiar contenedor
        for widget in self.frame_aux_contenedor.winfo_children():
            widget.destroy()
            
        # Columna izquierda - Auxiliares iniciales
        frame_inicial = ctk.CTkFrame(self.frame_aux_contenedor, corner_radius=8)
        frame_inicial.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        ctk.CTkLabel(
            frame_inicial,
            text="Auxiliares Distribución Inicial",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(10, 5))
        
        # Frame scrollable con altura variable
        altura_actual = self.altura_auxiliares.get()
        self.scroll_inicial = ctk.CTkScrollableFrame(frame_inicial, height=altura_actual)
        self.scroll_inicial.pack(fill="both", expand=True, padx=10, pady=(5, 10))
        
        # Agregar 10 auxiliares de ejemplo
        for i in range(1, 11):
            frame_aux = ctk.CTkFrame(self.scroll_inicial, fg_color="transparent")
            frame_aux.pack(fill="x", pady=2)
            
            ctk.CTkLabel(frame_aux, text=f"Auxiliar {i}:", width=70, font=ctk.CTkFont(size=11)).pack(side="left", padx=(5, 10))
            ctk.CTkEntry(frame_aux, height=30, font=ctk.CTkFont(size=11)).pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        # Columna derecha - Auxiliares finales
        frame_final = ctk.CTkFrame(self.frame_aux_contenedor, corner_radius=8)
        frame_final.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
        ctk.CTkLabel(
            frame_final,
            text="Auxiliares Distribución Final",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(10, 5))
        
        # Frame scrollable con altura variable
        self.scroll_final = ctk.CTkScrollableFrame(frame_final, height=altura_actual)
        self.scroll_final.pack(fill="both", expand=True, padx=10, pady=(5, 10))
        
        # Agregar 10 auxiliares de ejemplo
        for i in range(1, 11):
            frame_aux = ctk.CTkFrame(self.scroll_final, fg_color="transparent")
            frame_aux.pack(fill="x", pady=2)
            
            ctk.CTkLabel(frame_aux, text=f"Auxiliar {i}:", width=70, font=ctk.CTkFont(size=11)).pack(side="left", padx=(5, 10))
            ctk.CTkEntry(frame_aux, height=30, font=ctk.CTkFont(size=11)).pack(side="left", fill="x", expand=True, padx=(0, 5))
    
    def _actualizar_ventana(self, value):
        """Actualiza la altura de la ventana de prueba."""
        nueva_altura = int(float(value))
        self.test_window.geometry(f"1000x{nueva_altura}")
        self._actualizar_labels()
        
    def _actualizar_auxiliares(self, value):
        """Actualiza la altura del área de auxiliares."""
        self._crear_columnas_auxiliares()
        self._actualizar_labels()
        
    def _actualizar_labels(self):
        """Actualiza los labels con los valores actuales."""
        altura_v = self.altura_ventana.get()
        altura_a = self.altura_auxiliares.get()
        
        self.label_ventana.config(text=f"{altura_v}px")
        self.label_auxiliares.config(text=f"{altura_a}px")
        self.info_label.config(text=f"Ventana: 1000x{altura_v} | Auxiliares: {altura_a}px")
        
    def _resetear_valores(self):
        """Resetea los valores a los originales."""
        self.altura_ventana.set(600)  # Valor original
        self.altura_auxiliares.set(255)  # Valor original
        self._actualizar_ventana(600)
        self._actualizar_auxiliares(255)
        
    def _aplicar_cambios(self):
        """Aplica los cambios seleccionados a los archivos de la aplicación."""
        altura_v = self.altura_ventana.get()
        altura_a = self.altura_auxiliares.get()
        
        respuesta = messagebox.askyesno(
            "Confirmar Cambios",
            f"¿Aplicar estos cambios a la aplicación moderna?\n\n"
            f"• Altura ventana: 1000x{altura_v}\n"
            f"• Altura auxiliares: {altura_a}px\n\n"
            f"Esto modificará los archivos app_moderna.py y ui_components_modern.py",
            icon='question'
        )
        
        if respuesta:
            try:
                self._modificar_archivos(altura_v, altura_a)
                messagebox.showinfo(
                    "Cambios Aplicados",
                    f"Los cambios se han aplicado correctamente:\n\n"
                    f"• Ventana: 1000x{altura_v}\n"
                    f"• Auxiliares: {altura_a}px\n\n"
                    f"Puedes cerrar este ajustador y probar la aplicación moderna."
                )
            except Exception as e:
                messagebox.showerror("Error", f"Error al aplicar cambios: {str(e)}")
    
    def _modificar_archivos(self, altura_ventana, altura_auxiliares):
        """Modifica los archivos con las nuevas dimensiones."""
        # Modificar app_moderna.py
        app_path = "app_moderna.py"
        if os.path.exists(app_path):
            with open(app_path, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Reemplazar altura de ventana
            contenido = contenido.replace(
                'self.root.geometry("1000x700")',
                f'self.root.geometry("1000x{altura_ventana}")'
            )
            contenido = contenido.replace(
                'self.root.minsize(1000, 700)',
                f'self.root.minsize(1000, {altura_ventana})'
            )
            
            with open(app_path, 'w', encoding='utf-8') as f:
                f.write(contenido)
        
        # Modificar ui_components_modern.py
        ui_path = "ui_components_modern.py"
        if os.path.exists(ui_path):
            with open(ui_path, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Reemplazar altura de auxiliares
            contenido = contenido.replace(
                f'ctk.CTkScrollableFrame(frame_inicial, height=320)',
                f'ctk.CTkScrollableFrame(frame_inicial, height={altura_auxiliares})'
            )
            contenido = contenido.replace(
                f'ctk.CTkScrollableFrame(frame_final, height=320)',
                f'ctk.CTkScrollableFrame(frame_final, height={altura_auxiliares})'
            )
            
            with open(ui_path, 'w', encoding='utf-8') as f:
                f.write(contenido)
    
    def ejecutar(self):
        """Ejecuta el ajustador."""
        # Configurar cierre
        def on_closing():
            if self.test_window:
                self.test_window.destroy()
            self.control_window.destroy()
            
        self.control_window.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Mostrar instrucciones
        messagebox.showinfo(
            "Ajustador de Altura",
            "Usa los controles deslizantes para ajustar:\n\n"
            "• Altura de la ventana (500-900px)\n"
            "• Altura del área de auxiliares (200-400px)\n\n"
            "Los cambios se ven en tiempo real en la ventana de prueba.\n"
            "Cuando encuentres el tamaño ideal, haz clic en 'Aplicar Cambios'."
        )
        
        # Iniciar bucle principal
        self.control_window.mainloop()

def main():
    """Función principal."""
    print("Iniciando Ajustador de Altura UI Moderna...")
    
    try:
        ajustador = AjustadorAltura()
        ajustador.ejecutar()
    except Exception as e:
        print(f"Error: {e}")
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()
