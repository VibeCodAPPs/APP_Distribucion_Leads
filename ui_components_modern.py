"""
Módulo con componentes y estilos modernos usando CustomTkinter para la interfaz de usuario.
Mantiene la estructura original con dos listas de auxiliares (inicial y final).
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
    """Clase para crear componentes de UI modernos con CustomTkinter manteniendo la estructura original."""
    
    @staticmethod
    def crear_frame_principal(root, padding=10):
        """
        Crea el frame principal moderno.
        
        Args:
            root (ctk.CTk): Widget padre.
            padding (int): Padding del frame.
            
        Returns:
            ctk.CTkFrame: Frame configurado.
        """
        frame = ctk.CTkFrame(root, corner_radius=0, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=padding, pady=padding)
        return frame
    
    @staticmethod
    def crear_titulo(parent):
        """
        Crea el título principal.
        
        Args:
            parent (ctk.CTkFrame): Widget padre.
            
        Returns:
            ctk.CTkLabel: Título configurado.
        """
        titulo = ctk.CTkLabel(
            parent, 
            text="Distribución de Leads",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=ModernUIStyles.PRIMARY_COLOR
        )
        titulo.pack(pady=(0, 10))
        return titulo
    
    @staticmethod
    def crear_layout_columnas(parent):
        """
        Crea el layout de dos columnas como en la versión original.
        
        Args:
            parent (ctk.CTkFrame): Widget padre.
            
        Returns:
            tuple: (frame_izquierdo, frame_derecho)
        """
        # Frame izquierdo (más estrecho, ancho fijo)
        frame_izquierdo = ctk.CTkFrame(parent, width=400, corner_radius=10)
        frame_izquierdo.pack(side="left", fill="y", expand=False, padx=(0, 10))
        frame_izquierdo.pack_propagate(False)
        
        # Frame derecho (expandible)
        frame_derecho = ctk.CTkFrame(parent, corner_radius=10)
        frame_derecho.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        return frame_izquierdo, frame_derecho
    
    @staticmethod
    def crear_frame_archivo(parent, textvariable, command, mensaje_estado_var):
        """
        Crea un frame moderno para selección de archivo.
        
        Args:
            parent (ctk.CTkFrame): Widget padre.
            textvariable (tk.StringVar): Variable para mostrar ruta del archivo.
            command (function): Función a ejecutar al pulsar el botón "Seleccionar".
            mensaje_estado_var (tk.StringVar): Variable para mostrar estado del archivo.
            
        Returns:
            ctk.CTkFrame: Frame configurado.
        """
        frame = ctk.CTkFrame(parent, corner_radius=8)
        frame.pack(fill="x", padx=10, pady=(10, 5))
        
        # Título de la sección
        titulo = ctk.CTkLabel(
            frame, 
            text="📁 Selección de Archivo",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        titulo.pack(pady=(10, 5))
        
        # Entrada de archivo
        entrada = ctk.CTkEntry(
            frame,
            textvariable=textvariable,
            placeholder_text="Selecciona un archivo Excel...",
            height=35,
            font=ctk.CTkFont(size=11)
        )
        entrada.pack(fill="x", padx=10, pady=(0, 5))
        
        # Botón seleccionar
        boton = ctk.CTkButton(
            frame,
            text="Seleccionar Archivo",
            command=command,
            height=35,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        boton.pack(fill="x", padx=10, pady=(0, 5))
        
        # Mensaje de estado
        estado_label = ctk.CTkLabel(
            frame,
            textvariable=mensaje_estado_var,
            font=ctk.CTkFont(size=11),
            text_color=("gray10", "gray90"),
            wraplength=350,
            justify="left",
            anchor="w"
        )
        estado_label.pack(pady=(5, 10), padx=10, fill="x")
        
        return frame
    
    @staticmethod
    def crear_frame_opciones_duplicados(parent, duplicados_correo_var, duplicados_tel_var, eliminar_antes_var):
        """
        Crea un frame moderno para opciones de duplicados.
        
        Args:
            parent (ctk.CTkFrame): Widget padre.
            duplicados_correo_var (tk.BooleanVar): Variable para duplicados por correo.
            duplicados_tel_var (tk.BooleanVar): Variable para duplicados por teléfono.
            eliminar_antes_var (tk.BooleanVar): Variable para eliminar antes.
            
        Returns:
            ctk.CTkFrame: Frame configurado.
        """
        frame = ctk.CTkFrame(parent, corner_radius=8)
        frame.pack(fill="x", padx=10, pady=5)
        
        # Título
        titulo = ctk.CTkLabel(
            frame, 
            text="🔍 Opciones de Duplicados",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        titulo.pack(pady=(10, 5))
        
        # Checkboxes
        check1 = ctk.CTkCheckBox(
            frame,
            text="Buscar duplicados por correo",
            variable=duplicados_correo_var,
            font=ctk.CTkFont(size=11)
        )
        check1.pack(anchor="w", padx=15, pady=2)
        
        check2 = ctk.CTkCheckBox(
            frame,
            text="Buscar duplicados por teléfono",
            variable=duplicados_tel_var,
            font=ctk.CTkFont(size=11)
        )
        check2.pack(anchor="w", padx=15, pady=2)
        
        check3 = ctk.CTkCheckBox(
            frame,
            text="Eliminar duplicados antes de distribuir",
            variable=eliminar_antes_var,
            font=ctk.CTkFont(size=11)
        )
        check3.pack(anchor="w", padx=15, pady=(2, 10))
        
        return frame
    
    @staticmethod
    def crear_frame_progreso_y_botones(parent, progreso_var, command_distribuir, command_salir):
        """
        Crea frame con barra de progreso y botones de acción.
        
        Args:
            parent (ctk.CTkFrame): Widget padre.
            progreso_var (tk.DoubleVar): Variable para barra de progreso.
            command_distribuir (function): Función para botón distribuir.
            command_salir (function): Función para botón salir.
            
        Returns:
            ctk.CTkFrame: Frame configurado.
        """
        # Frame para progreso
        frame_progreso = ctk.CTkFrame(parent, corner_radius=8)
        frame_progreso.pack(fill="x", padx=10, pady=5)
        
        # Título progreso
        ctk.CTkLabel(
            frame_progreso, 
            text="📊 Progreso:",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(pady=(10, 5))
        
        # Barra de progreso
        progress_bar = ctk.CTkProgressBar(
            frame_progreso,
            variable=progreso_var,
            width=350,
            height=15,
            corner_radius=8
        )
        progress_bar.pack(padx=15, pady=(0, 10))
        
        # Frame para botones
        frame_botones = ctk.CTkFrame(parent, corner_radius=8)
        frame_botones.pack(fill="x", padx=10, pady=5)
        
        # Botón Distribuir
        boton_distribuir = ctk.CTkButton(
            frame_botones,
            text="🚀 Realizar Distribución",
            command=command_distribuir,
            height=40,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        boton_distribuir.pack(fill="x", padx=10, pady=(10, 5))
        
        # Botón Salir
        boton_salir = ctk.CTkButton(
            frame_botones,
            text="❌ Salir",
            command=command_salir,
            height=35,
            font=ctk.CTkFont(size=11),
            fg_color="gray",
            hover_color="darkgray"
        )
        boton_salir.pack(fill="x", padx=10, pady=(0, 10))
        
        return frame_progreso, frame_botones
    
    @staticmethod
    def crear_frame_auxiliares_completo(parent, num_aux_inicial_var, num_aux_final_var, 
                                       nombres_aux_inicial, nombres_aux_final,
                                       callback_inicial, callback_final):
        """
        Crea el frame completo de auxiliares con dos paneles lado a lado.
        
        Args:
            parent (ctk.CTkFrame): Widget padre.
            num_aux_inicial_var (tk.IntVar): Variable número auxiliares iniciales.
            num_aux_final_var (tk.IntVar): Variable número auxiliares finales.
            nombres_aux_inicial (dict): Diccionario con variables de nombres iniciales.
            nombres_aux_final (dict): Diccionario con variables de nombres finales.
            callback_inicial (function): Callback para actualizar auxiliares iniciales.
            callback_final (function): Callback para actualizar auxiliares finales.
            
        Returns:
            dict: Diccionario con referencias a los componentes creados.
        """
        # Frame principal de auxiliares
        frame_auxiliares = ctk.CTkFrame(parent, corner_radius=10)
        frame_auxiliares.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título principal
        titulo = ctk.CTkLabel(
            frame_auxiliares, 
            text="👥 Configuración de Auxiliares",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        titulo.pack(pady=(15, 10))
        
        # Frame para selección de números
        frame_seleccion = ctk.CTkFrame(frame_auxiliares, fg_color="transparent")
        frame_seleccion.pack(fill="x", padx=15, pady=(0, 10))
        
        # Auxiliares iniciales
        ctk.CTkLabel(
            frame_seleccion, 
            text="Auxiliares iniciales:",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(side="left")
        
        # Crear spinbox personalizado para auxiliares iniciales
        frame_spin_inicial = ctk.CTkFrame(frame_seleccion, fg_color="transparent")
        frame_spin_inicial.pack(side="left", padx=(10, 20))
        
        entry_inicial = ctk.CTkEntry(frame_spin_inicial, width=50, textvariable=num_aux_inicial_var)
        entry_inicial.pack(side="left")
        
        frame_botones_inicial = ctk.CTkFrame(frame_spin_inicial, fg_color="transparent")
        frame_botones_inicial.pack(side="left", padx=(2, 0))
        
        def incrementar_inicial():
            val = min(10, num_aux_inicial_var.get() + 1)
            num_aux_inicial_var.set(val)
            callback_inicial()
        
        def decrementar_inicial():
            val = max(2, num_aux_inicial_var.get() - 1)
            num_aux_inicial_var.set(val)
            callback_inicial()
        
        ctk.CTkButton(frame_botones_inicial, text="▲", width=20, height=15, 
                     command=incrementar_inicial, font=ctk.CTkFont(size=8)).pack()
        ctk.CTkButton(frame_botones_inicial, text="▼", width=20, height=15, 
                     command=decrementar_inicial, font=ctk.CTkFont(size=8)).pack()
        
        # Auxiliares finales
        ctk.CTkLabel(
            frame_seleccion, 
            text="Auxiliares finales:",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(side="left")
        
        # Crear spinbox personalizado para auxiliares finales
        frame_spin_final = ctk.CTkFrame(frame_seleccion, fg_color="transparent")
        frame_spin_final.pack(side="left", padx=(10, 0))
        
        entry_final = ctk.CTkEntry(frame_spin_final, width=50, textvariable=num_aux_final_var)
        entry_final.pack(side="left")
        
        frame_botones_final = ctk.CTkFrame(frame_spin_final, fg_color="transparent")
        frame_botones_final.pack(side="left", padx=(2, 0))
        
        def incrementar_final():
            val = min(10, num_aux_final_var.get() + 1)
            num_aux_final_var.set(val)
            callback_final()
        
        def decrementar_final():
            val = max(1, num_aux_final_var.get() - 1)
            num_aux_final_var.set(val)
            callback_final()
        
        ctk.CTkButton(frame_botones_final, text="▲", width=20, height=15, 
                     command=incrementar_final, font=ctk.CTkFont(size=8)).pack()
        ctk.CTkButton(frame_botones_final, text="▼", width=20, height=15, 
                     command=decrementar_final, font=ctk.CTkFont(size=8)).pack()
        
        # Frame contenedor para los dos paneles lado a lado
        frame_contenedor = ctk.CTkFrame(frame_auxiliares, fg_color="transparent")
        frame_contenedor.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Panel izquierdo - Auxiliares iniciales
        frame_inicial = ctk.CTkFrame(frame_contenedor, corner_radius=8)
        frame_inicial.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        titulo_inicial = ctk.CTkLabel(
            frame_inicial,
            text="Auxiliares Distribución Inicial",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        titulo_inicial.pack(pady=(10, 5))
        
        # Frame normal para auxiliares iniciales (sin scroll)
        scroll_inicial = ctk.CTkFrame(frame_inicial, height=286)  
        scroll_inicial.pack(fill="both", expand=True, padx=10, pady=(5, 10))
        
        # Panel derecho - Auxiliares finales
        frame_final = ctk.CTkFrame(frame_contenedor, corner_radius=8)
        frame_final.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        titulo_final = ctk.CTkLabel(
            frame_final, 
            text="Auxiliares Distribución Final",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        titulo_final.pack(pady=(10, 5))
        
        # Frame normal para auxiliares finales (sin scroll)
        scroll_final = ctk.CTkFrame(frame_final, height=286)  
        scroll_final.pack(fill="both", expand=True, padx=10, pady=(5, 10))
        
        return {
            'frame_auxiliares': frame_auxiliares,
            'scroll_inicial': scroll_inicial,
            'scroll_final': scroll_final,
            'nombres_aux_inicial': nombres_aux_inicial,
            'nombres_aux_final': nombres_aux_final
        }
    
    @staticmethod
    def actualizar_auxiliares_iniciales(scroll_frame, nombres_dict, num_auxiliares, entries_dict):
        """
        Actualiza los campos de auxiliares iniciales.
        
        Args:
            scroll_frame: Frame scrollable donde agregar los campos.
            nombres_dict (dict): Diccionario con variables de nombres.
            num_auxiliares (int): Número de auxiliares a mostrar.
            entries_dict (dict): Diccionario para guardar referencias a entries.
        """
        # Limpiar frame actual
        for widget in scroll_frame.winfo_children():
            widget.destroy()
        
        entries_dict.clear()
        
        # Crear campos para cada auxiliar
        for i in range(1, num_auxiliares + 1):
            # Si no existe la variable para este auxiliar, crearla
            if i not in nombres_dict:
                nombres_dict[i] = tk.StringVar(value=f"Auxiliar {i}")
            
            # Frame para cada auxiliar
            frame_aux = ctk.CTkFrame(scroll_frame, fg_color="transparent")
            frame_aux.pack(fill="x", pady=2)
            
            # Etiqueta
            label = ctk.CTkLabel(
                frame_aux, 
                text=f"Auxiliar {i}:",
                font=ctk.CTkFont(size=11),
                width=70
            )
            label.pack(side="left", padx=(5, 10))
            
            # Campo de entrada
            entry = ctk.CTkEntry(
                frame_aux,
                textvariable=nombres_dict[i],
                height=30,
                font=ctk.CTkFont(size=11)
            )
            entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
            
            # Guardar referencia
            entries_dict[i] = entry
    
    @staticmethod
    def actualizar_auxiliares_finales(scroll_frame, nombres_dict, num_auxiliares, entries_dict):
        """
        Actualiza los campos de auxiliares finales.
        
        Args:
            scroll_frame: Frame scrollable donde agregar los campos.
            nombres_dict (dict): Diccionario con variables de nombres.
            num_auxiliares (int): Número de auxiliares a mostrar.
            entries_dict (dict): Diccionario para guardar referencias a entries.
        """
        # Limpiar frame actual
        for widget in scroll_frame.winfo_children():
            widget.destroy()
        
        entries_dict.clear()
        
        # Crear campos para cada auxiliar
        for i in range(1, num_auxiliares + 1):
            # Si no existe la variable para este auxiliar, crearla
            if i not in nombres_dict:
                nombres_dict[i] = tk.StringVar(value=f"Auxiliar {i}")
            
            # Frame para cada auxiliar
            frame_aux = ctk.CTkFrame(scroll_frame, fg_color="transparent")
            frame_aux.pack(fill="x", pady=2)
            
            # Etiqueta
            label = ctk.CTkLabel(
                frame_aux, 
                text=f"Auxiliar {i}:",
                font=ctk.CTkFont(size=11),
                width=70
            )
            label.pack(side="left", padx=(5, 10))
            
            # Campo de entrada
            entry = ctk.CTkEntry(
                frame_aux,
                textvariable=nombres_dict[i],
                height=30,
                font=ctk.CTkFont(size=11)
            )
            entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
            
            # Guardar referencia
            entries_dict[i] = entry

    @staticmethod
    def crear_footer_moderno(parent, callback_changelog, callback_correo):
        """
        Crea un pie de página moderno con información del desarrollador y enlace al historial.
        
        Args:
            parent: Widget padre donde agregar el footer.
            callback_changelog (function): Función para abrir el historial de cambios.
            callback_correo (function): Función para enviar correo al desarrollador.
            
        Returns:
            ctk.CTkFrame: Frame del footer configurado.
        """
        # Frame del footer con color de fondo diferente
        footer_frame = ctk.CTkFrame(parent, height=40, corner_radius=0, fg_color=("gray85", "gray25"))
        footer_frame.pack(fill="x", side="bottom", pady=(5, 0))
        footer_frame.pack_propagate(False)
        
        # Enlace al historial de cambios (lado izquierdo)
        link_changelog = ctk.CTkLabel(
            footer_frame,
            text="Ver Historial de Cambios",
            font=ctk.CTkFont(size=12, underline=True),
            text_color="black",
            cursor="hand2"
        )
        link_changelog.pack(side="left", padx=10, pady=8)
        link_changelog.bind("<Button-1>", lambda e: callback_changelog())
        
        # Información del desarrollador (lado derecho)
        link_desarrollador = ctk.CTkLabel(
            footer_frame,
            text="José Manuel de la Colina (Diseño y desarrollo) - jose.de-la-colina@renault.com",
            font=ctk.CTkFont(size=10, underline=True),
            text_color="black",
            cursor="hand2"
        )
        link_desarrollador.pack(side="right", padx=10, pady=8)
        link_desarrollador.bind("<Button-1>", lambda e: callback_correo())
        
        return footer_frame
