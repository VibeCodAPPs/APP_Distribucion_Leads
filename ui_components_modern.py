"""
Módulo con componentes y estilos modernos usando CustomTkinter para la interfaz de usuario.
"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
import tkinter as tk


class ModernUIStyles:
    """Clase para gestionar los estilos modernos de la interfaz de usuario."""
    
    # Configuración de tema y colores
    THEME_MODE = "light"  # "light" o "dark"
    COLOR_THEME = "blue"  # "blue", "green", "dark-blue"
    
    # Colores personalizados
    PRIMARY_COLOR = "#1f538d"      # Azul SOFASA
    SECONDARY_COLOR = "#2c3e50"    # Azul oscuro
    SUCCESS_COLOR = "#2ecc71"      # Verde
    ERROR_COLOR = "#e74c3c"        # Rojo
    WARNING_COLOR = "#f39c12"      # Naranja
    
    @staticmethod
    def configurar_tema():
        """Configura el tema moderno de CustomTkinter."""
        ctk.set_appearance_mode(ModernUIStyles.THEME_MODE)
        ctk.set_default_color_theme(ModernUIStyles.COLOR_THEME)


class ModernUIComponentFactory:
    """Clase para crear componentes de UI modernos con CustomTkinter."""
    
    @staticmethod
    def crear_frame_principal(root, padding=20):
        """
        Crea un frame principal moderno.
        
        Args:
            root (ctk.CTk): Widget padre.
            padding (int): Padding del frame.
            
        Returns:
            ctk.CTkFrame: Frame configurado.
        """
        frame = ctk.CTkFrame(root, corner_radius=15)
        frame.pack(fill="both", expand=True, padx=padding, pady=padding)
        return frame
    
    @staticmethod
    def crear_titulo(parent, texto):
        """
        Crea un título moderno.
        
        Args:
            parent (ctk.CTkFrame): Widget padre.
            texto (str): Texto del título.
            
        Returns:
            ctk.CTkLabel: Título configurado.
        """
        titulo = ctk.CTkLabel(
            parent, 
            text=texto,
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=ModernUIStyles.PRIMARY_COLOR
        )
        titulo.pack(pady=(0, 20))
        return titulo
    
    @staticmethod
    def crear_frame_archivo(parent, textvariable, command, mensaje_estado_var=None):
        """
        Crea un frame moderno para selección de archivo.
        
        Args:
            parent (ctk.CTkFrame): Widget padre.
            textvariable (tk.StringVar): Variable para mostrar ruta del archivo.
            command (function): Función a ejecutar al pulsar el botón "Seleccionar".
            mensaje_estado_var (tk.StringVar, optional): Variable para mostrar estado del archivo.
            
        Returns:
            ctk.CTkFrame: Frame configurado.
        """
        frame = ctk.CTkFrame(parent, corner_radius=10)
        frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Título de la sección
        titulo = ctk.CTkLabel(
            frame, 
            text="📁 Seleccionar Archivo Excel",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        titulo.pack(pady=(15, 10))
        
        # Frame para entrada y botón
        entrada_frame = ctk.CTkFrame(frame, fg_color="transparent")
        entrada_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        # Entrada de archivo
        entrada = ctk.CTkEntry(
            entrada_frame,
            textvariable=textvariable,
            placeholder_text="Selecciona un archivo Excel...",
            height=40,
            font=ctk.CTkFont(size=12)
        )
        entrada.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Botón seleccionar
        boton = ctk.CTkButton(
            entrada_frame,
            text="Seleccionar",
            command=command,
            width=120,
            height=40,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        boton.pack(side="right")
        
        # Mensaje de estado si se proporciona
        if mensaje_estado_var:
            estado_label = ctk.CTkLabel(
                frame,
                textvariable=mensaje_estado_var,
                font=ctk.CTkFont(size=11),
                text_color="gray"
            )
            estado_label.pack(pady=(0, 15))
        
        return frame
    
    @staticmethod
    def crear_frame_auxiliares(parent, num_auxiliares_var, nombre_aux1_var, 
                              nombre_aux2_var, nombre_aux3_var, 
                              duplicados_var, duplicados_tel_var,
                              eliminar_duplicados_var, command_actualizar):
        """
        Crea un frame moderno para configuración de auxiliares.
        
        Args:
            parent (ctk.CTkFrame): Widget padre.
            num_auxiliares_var (tk.IntVar): Variable para selección de número de auxiliares.
            nombre_aux1_var (tk.StringVar): Variable para nombre del auxiliar 1.
            nombre_aux2_var (tk.StringVar): Variable para nombre del auxiliar 2.
            nombre_aux3_var (tk.StringVar): Variable para nombre del auxiliar 3.
            duplicados_var (tk.BooleanVar): Variable para checkbox de duplicados por correo.
            duplicados_tel_var (tk.BooleanVar): Variable para checkbox de duplicados por teléfono.
            eliminar_duplicados_var (tk.BooleanVar): Variable para checkbox de eliminación de duplicados.
            command_actualizar (function): Función para actualizar campos según número de auxiliares.
            
        Returns:
            dict: Diccionario con los componentes creados para auxiliar 3.
        """
        frame = ctk.CTkFrame(parent, corner_radius=10)
        frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Título de la sección
        titulo = ctk.CTkLabel(
            frame, 
            text="👥 Configuración de Auxiliares",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        titulo.pack(pady=(15, 15))
        
        # Frame para número de auxiliares
        num_frame = ctk.CTkFrame(frame, fg_color="transparent")
        num_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(
            num_frame, 
            text="Número de auxiliares:",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(side="left")
        
        # Segmented button para número de auxiliares
        segmented_button = ctk.CTkSegmentedButton(
            num_frame,
            values=["2", "3"],
            command=lambda value: [num_auxiliares_var.set(int(value)), command_actualizar()],
            font=ctk.CTkFont(size=12)
        )
        segmented_button.pack(side="right")
        segmented_button.set("2")  # Valor por defecto
        
        # Frame para nombres de auxiliares
        nombres_frame = ctk.CTkFrame(frame, fg_color="transparent")
        nombres_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Auxiliar 1
        aux1_frame = ctk.CTkFrame(nombres_frame, fg_color="transparent")
        aux1_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            aux1_frame, 
            text="Auxiliar 1:",
            font=ctk.CTkFont(size=12),
            width=80
        ).pack(side="left")
        
        entry_aux1 = ctk.CTkEntry(
            aux1_frame,
            textvariable=nombre_aux1_var,
            placeholder_text="Nombre del auxiliar 1",
            height=35
        )
        entry_aux1.pack(side="left", fill="x", expand=True, padx=(10, 0))
        
        # Auxiliar 2
        aux2_frame = ctk.CTkFrame(nombres_frame, fg_color="transparent")
        aux2_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            aux2_frame, 
            text="Auxiliar 2:",
            font=ctk.CTkFont(size=12),
            width=80
        ).pack(side="left")
        
        entry_aux2 = ctk.CTkEntry(
            aux2_frame,
            textvariable=nombre_aux2_var,
            placeholder_text="Nombre del auxiliar 2",
            height=35
        )
        entry_aux2.pack(side="left", fill="x", expand=True, padx=(10, 0))
        
        # Auxiliar 3 (inicialmente oculto)
        aux3_frame = ctk.CTkFrame(nombres_frame, fg_color="transparent")
        
        label_aux3 = ctk.CTkLabel(
            aux3_frame, 
            text="Auxiliar 3:",
            font=ctk.CTkFont(size=12),
            width=80
        )
        label_aux3.pack(side="left")
        
        entry_aux3 = ctk.CTkEntry(
            aux3_frame,
            textvariable=nombre_aux3_var,
            placeholder_text="Nombre del auxiliar 3",
            height=35
        )
        entry_aux3.pack(side="left", fill="x", expand=True, padx=(10, 0))
        
        # Frame para opciones de duplicados
        duplicados_frame = ctk.CTkFrame(frame, fg_color="transparent")
        duplicados_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(
            duplicados_frame, 
            text="🔍 Opciones de Duplicados:",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(anchor="w", pady=(0, 10))
        
        # Checkboxes modernos
        check1 = ctk.CTkCheckBox(
            duplicados_frame,
            text="Detectar duplicados por correo electrónico",
            variable=duplicados_var,
            font=ctk.CTkFont(size=11)
        )
        check1.pack(anchor="w", pady=(0, 5))
        
        check2 = ctk.CTkCheckBox(
            duplicados_frame,
            text="Detectar duplicados por teléfono",
            variable=duplicados_tel_var,
            font=ctk.CTkFont(size=11)
        )
        check2.pack(anchor="w", pady=(0, 5))
        
        check3 = ctk.CTkCheckBox(
            duplicados_frame,
            text="Eliminar duplicados antes de distribuir",
            variable=eliminar_duplicados_var,
            font=ctk.CTkFont(size=11)
        )
        check3.pack(anchor="w", pady=(0, 15))
        
        return {
            'frame_aux3': aux3_frame,
            'label_aux3': label_aux3,
            'entry_aux3': entry_aux3
        }
    
    @staticmethod
    def crear_frame_acciones(parent, command_distribuir, command_salir):
        """
        Crea un frame moderno con botones de acción.
        
        Args:
            parent (ctk.CTkFrame): Widget padre.
            command_distribuir (function): Función para botón Distribuir.
            command_salir (function): Función para botón Salir.
            
        Returns:
            ctk.CTkFrame: Frame con botones de acción.
        """
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Botón Distribuir (principal)
        boton_distribuir = ctk.CTkButton(
            frame,
            text="🚀 Distribuir Leads",
            command=command_distribuir,
            width=200,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=10
        )
        boton_distribuir.pack(side="left", padx=(0, 10))
        
        # Botón Salir (secundario)
        boton_salir = ctk.CTkButton(
            frame,
            text="❌ Salir",
            command=command_salir,
            width=100,
            height=45,
            font=ctk.CTkFont(size=12),
            fg_color="gray",
            hover_color="darkgray",
            corner_radius=10
        )
        boton_salir.pack(side="right")
        
        return frame
    
    @staticmethod
    def crear_frame_estado(parent, mensaje_var, progreso_var):
        """
        Crea un frame moderno para mostrar el estado y progreso.
        
        Args:
            parent (ctk.CTkFrame): Widget padre.
            mensaje_var (tk.StringVar): Variable para mensaje de estado.
            progreso_var (tk.DoubleVar): Variable para barra de progreso.
            
        Returns:
            ctk.CTkFrame: Frame con indicadores de estado.
        """
        frame = ctk.CTkFrame(parent, corner_radius=10)
        frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Mensaje de estado
        mensaje_label = ctk.CTkLabel(
            frame,
            textvariable=mensaje_var,
            font=ctk.CTkFont(size=12),
            wraplength=800
        )
        mensaje_label.pack(pady=(15, 10))
        
        # Barra de progreso moderna
        progress_bar = ctk.CTkProgressBar(
            frame,
            variable=progreso_var,
            width=400,
            height=20,
            corner_radius=10
        )
        progress_bar.pack(pady=(0, 15))
        
        return frame
