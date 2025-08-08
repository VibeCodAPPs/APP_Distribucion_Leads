#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simple para redimensionar la aplicación moderna y capturar el tamaño ideal.
Ejecuta la app moderna con capacidad de redimensionamiento y captura las dimensiones.
"""

import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys
import time
import threading
import re

class RedimensionadorApp:
    def __init__(self):
        self.proceso_app = None
        self.dimensiones_capturadas = None
        
        # Crear ventana de control
        self.control_window = tk.Tk()
        self.control_window.title("Redimensionador App Moderna")
        self.control_window.geometry("400x500")
        self.control_window.resizable(False, False)
        
        # Posicionar en esquina superior izquierda
        self.control_window.geometry("+50+50")
        
        self._crear_interfaz()
        
    def _crear_interfaz(self):
        """Crea la interfaz de control."""
        # Título
        titulo = tk.Label(
            self.control_window,
            text="Redimensionador App Moderna",
            font=("Arial", 16, "bold"),
            fg="blue"
        )
        titulo.pack(pady=20)
        
        # Frame principal
        frame_principal = tk.Frame(self.control_window)
        frame_principal.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Instrucciones detalladas
        instrucciones_frame = tk.LabelFrame(frame_principal, text="INSTRUCCIONES", font=("Arial", 11, "bold"))
        instrucciones_frame.pack(fill="x", pady=(0, 20))
        
        instrucciones_text = tk.Text(
            instrucciones_frame,
            height=8,
            width=45,
            font=("Arial", 9),
            wrap=tk.WORD,
            bg="lightyellow"
        )
        instrucciones_text.pack(padx=10, pady=10)
        
        instrucciones_content = """1. Haz clic en 'Abrir App Moderna'

2. Se abrirá la aplicación moderna REAL

3. Redimensiona la ventana arrastrando las esquinas hasta que:
   • Los 10 auxiliares se vean sin scroll
   • La ventana no se vea muy alta
   • Todo se vea proporcionado

4. Anota las dimensiones que aparecen en el título de la ventana

5. Ingresa esas dimensiones aquí y aplica los cambios"""
        
        instrucciones_text.insert("1.0", instrucciones_content)
        instrucciones_text.config(state="disabled")
        
        # Botón para abrir app
        self.btn_abrir = tk.Button(
            frame_principal,
            text="🚀 Abrir App Moderna",
            command=self._abrir_app_moderna,
            font=("Arial", 12, "bold"),
            bg="lightgreen",
            fg="black",
            height=2,
            width=30
        )
        self.btn_abrir.pack(pady=15)
        
        # Frame para capturar dimensiones
        captura_frame = tk.LabelFrame(frame_principal, text="CAPTURAR DIMENSIONES", font=("Arial", 11, "bold"))
        captura_frame.pack(fill="x", pady=15)
        
        tk.Label(captura_frame, text="Ingresa las dimensiones que veas en el título:", font=("Arial", 10)).pack(pady=(10, 5))
        
        # Frame para entrada de dimensiones
        entrada_frame = tk.Frame(captura_frame)
        entrada_frame.pack(pady=10)
        
        tk.Label(entrada_frame, text="Ancho:", font=("Arial", 10)).grid(row=0, column=0, padx=5)
        self.entry_ancho = tk.Entry(entrada_frame, width=10, font=("Arial", 10))
        self.entry_ancho.grid(row=0, column=1, padx=5)
        self.entry_ancho.insert(0, "1000")
        
        tk.Label(entrada_frame, text="Alto:", font=("Arial", 10)).grid(row=0, column=2, padx=5)
        self.entry_alto = tk.Entry(entrada_frame, width=10, font=("Arial", 10))
        self.entry_alto.grid(row=0, column=3, padx=5)
        self.entry_alto.insert(0, "700")
        
        # Botón para aplicar
        btn_aplicar = tk.Button(
            captura_frame,
            text="✅ Aplicar Estas Dimensiones",
            command=self._aplicar_dimensiones,
            font=("Arial", 11, "bold"),
            bg="orange",
            fg="black",
            height=2,
            width=30
        )
        btn_aplicar.pack(pady=15)
        
        # Estado actual
        estado_frame = tk.LabelFrame(frame_principal, text="ESTADO ACTUAL", font=("Arial", 11, "bold"))
        estado_frame.pack(fill="x", pady=15)
        
        self.label_estado = tk.Label(
            estado_frame,
            text="Dimensiones actuales: 1000x700",
            font=("Arial", 10),
            fg="blue"
        )
        self.label_estado.pack(pady=10)
        
        # Botón cerrar
        btn_cerrar = tk.Button(
            frame_principal,
            text="❌ Cerrar",
            command=self._cerrar_todo,
            font=("Arial", 10),
            bg="lightcoral",
            fg="black",
            width=30
        )
        btn_cerrar.pack(pady=(20, 10))
        
    def _abrir_app_moderna(self):
        """Abre la aplicación moderna con redimensionamiento habilitado."""
        try:
            # Crear script temporal que habilite redimensionamiento
            script_temp = """
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app_moderna import AplicacionDistribucionLeadsModerna

def main():
    app = AplicacionDistribucionLeadsModerna()
    
    # FORZAR redimensionamiento - múltiples métodos
    app.root.resizable(True, True)
    app.root.minsize(800, 400)  # Tamaño mínimo más pequeño
    app.root.maxsize(1600, 1200)  # Tamaño máximo más grande
    
    # Remover restricciones de tamaño fijo si existen
    try:
        app.root.geometry("")  # Limpiar geometry fijo
    except:
        pass
    
    # Configurar ventana para ser completamente redimensionable
    app.root.wm_resizable(True, True)
    
    # Función para mostrar dimensiones en el título
    def actualizar_titulo():
        try:
            app.root.update_idletasks()
            ancho = app.root.winfo_width()
            alto = app.root.winfo_height()
            app.root.title(f"SOFASA - UI Moderna - {ancho}x{alto} - REDIMENSIONABLE")
            app.root.after(500, actualizar_titulo)  # Actualizar cada 0.5 segundos
        except:
            pass
    
    # Configurar ventana inicial
    app.root.geometry("1000x700+500+50")
    
    # Asegurar que sea redimensionable después de crear la interfaz
    app.root.after(100, lambda: app.root.resizable(True, True))
    app.root.after(200, lambda: app.root.wm_resizable(True, True))
    
    # Iniciar actualización de título
    app.root.after(1000, actualizar_titulo)
    
    # Mostrar mensaje de ayuda
    import tkinter.messagebox as mb
    app.root.after(2000, lambda: mb.showinfo(
        "Redimensionamiento Habilitado",
        "¡La ventana ya es redimensionable!\\n\\n"
        "• Arrastra las ESQUINAS para redimensionar\\n"
        "• Las dimensiones aparecen en el TÍTULO\\n"
        "• Si no puedes redimensionar, intenta:\\n"
        "  - Arrastrar desde las esquinas\\n"
        "  - Usar Alt + clic derecho y arrastrar\\n"
        "  - Maximizar y luego restaurar la ventana"
    ))
    
    # Ejecutar
    app.ejecutar()

if __name__ == "__main__":
    main()
"""
            
            # Escribir script temporal
            with open("temp_app_redimensionable.py", "w", encoding="utf-8") as f:
                f.write(script_temp)
            
            # Ejecutar la aplicación
            self.proceso_app = subprocess.Popen([sys.executable, "temp_app_redimensionable.py"])
            
            # Actualizar interfaz
            self.btn_abrir.config(state="disabled", text="✅ App Abierta", bg="lightblue")
            
            messagebox.showinfo(
                "App Abierta",
                "¡La aplicación moderna se ha abierto!\n\n"
                "IMPORTANTE:\n"
                "• Redimensiona la ventana arrastrando las esquinas\n"
                "• Las dimensiones aparecen en el TÍTULO de la ventana\n"
                "• Anota esas dimensiones cuando esté perfecta\n"
                "• Ingresa las dimensiones aquí y aplica los cambios\n\n"
                "El título se actualiza cada 0.5 segundos."
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir la aplicación: {str(e)}")
            
    def _aplicar_dimensiones(self):
        """Aplica las dimensiones ingresadas."""
        try:
            ancho = int(self.entry_ancho.get())
            alto = int(self.entry_alto.get())
            
            if ancho < 800 or alto < 400:
                messagebox.showerror("Error", "Las dimensiones son demasiado pequeñas.\nMínimo: 800x400")
                return
                
            if ancho > 1500 or alto > 1000:
                messagebox.showerror("Error", "Las dimensiones son demasiado grandes.\nMáximo: 1500x1000")
                return
            
            # Calcular altura de auxiliares proporcionalmente
            altura_auxiliares = max(200, min(400, int(alto * 0.45)))
            
            respuesta = messagebox.askyesno(
                "Confirmar Cambios",
                f"¿Aplicar estos cambios?\n\n"
                f"• Ventana: {ancho}x{alto}\n"
                f"• Área auxiliares: {altura_auxiliares}px\n\n"
                f"Esto modificará:\n"
                f"- app_moderna.py\n"
                f"- ui_components_modern.py"
            )
            
            if respuesta:
                self._modificar_archivos(ancho, alto, altura_auxiliares)
                
                # Actualizar estado
                self.label_estado.config(
                    text=f"¡Aplicado! Nuevas dimensiones: {ancho}x{alto}",
                    fg="green"
                )
                
                messagebox.showinfo(
                    "¡Cambios Aplicados!",
                    f"Las dimensiones se han aplicado correctamente:\n\n"
                    f"• Ventana: {ancho}x{alto}\n"
                    f"• Auxiliares: {altura_auxiliares}px\n\n"
                    f"Puedes cerrar este redimensionador y probar\n"
                    f"la aplicación moderna con las nuevas dimensiones."
                )
                
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa números válidos para las dimensiones.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al aplicar cambios: {str(e)}")
            
    def _modificar_archivos(self, ancho, alto, altura_auxiliares):
        """Modifica los archivos con las nuevas dimensiones."""
        # Modificar app_moderna.py
        app_path = "app_moderna.py"
        if os.path.exists(app_path):
            with open(app_path, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Reemplazar dimensiones
            contenido = re.sub(
                r'self\.root\.geometry\("\d+x\d+"\)',
                f'self.root.geometry("{ancho}x{alto}")',
                contenido
            )
            contenido = re.sub(
                r'self\.root\.minsize\(\d+, \d+\)',
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
        """Cierra todo."""
        # Cerrar proceso de la app si existe
        if self.proceso_app:
            try:
                self.proceso_app.terminate()
            except:
                pass
                
        # Limpiar archivo temporal
        try:
            if os.path.exists("temp_app_redimensionable.py"):
                os.remove("temp_app_redimensionable.py")
        except:
            pass
            
        self.control_window.destroy()
        
    def ejecutar(self):
        """Ejecuta el redimensionador."""
        self.control_window.protocol("WM_DELETE_WINDOW", self._cerrar_todo)
        
        messagebox.showinfo(
            "Redimensionador App Moderna",
            "¡Bienvenido al Redimensionador!\n\n"
            "Este script te permite:\n"
            "1. Abrir la aplicación moderna REAL\n"
            "2. Redimensionarla manualmente\n"
            "3. Ver las dimensiones en el título\n"
            "4. Aplicar esas dimensiones automáticamente\n\n"
            "¡Comencemos!"
        )
        
        self.control_window.mainloop()

def main():
    """Función principal."""
    print("Iniciando Redimensionador App Moderna...")
    
    try:
        redimensionador = RedimensionadorApp()
        redimensionador.ejecutar()
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Error Fatal", f"Error: {str(e)}")

if __name__ == "__main__":
    main()
