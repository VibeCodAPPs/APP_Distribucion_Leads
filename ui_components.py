"""
Módulo con componentes y estilos para la interfaz de usuario de la aplicación.
"""
import tkinter as tk
from tkinter import ttk


class UIStyles:
    """Clase para gestionar los estilos de la interfaz de usuario."""
    
    # Colores de la interfaz
    PRIMARY_COLOR = "#3498db"      # Azul principal
    SECONDARY_COLOR = "#2c3e50"    # Azul oscuro
    BACKGROUND_COLOR = "#ecf0f1"   # Gris claro
    SUCCESS_COLOR = "#2ecc71"      # Verde
    ERROR_COLOR = "#e74c3c"        # Rojo
    BUTTON_TEXT = "#ffffff"        # Texto blanco para botones
    BUTTON_BG = "#000000"          # Fondo negro para botones
    BUTTON_HOVER = "#333333"       # Gris oscuro para hover
    
    @staticmethod
    def configurar_estilo():
        """Configura el estilo de la interfaz de usuario."""
        estilo = ttk.Style()
        estilo.theme_use('clam')
        
        # Configuraciones generales - asegurar que todo usa el mismo color de fondo
        estilo.configure(".", background=UIStyles.BACKGROUND_COLOR)
        estilo.configure("TFrame", background=UIStyles.BACKGROUND_COLOR)
        estilo.configure("TLabelframe", background=UIStyles.BACKGROUND_COLOR)
        estilo.configure("TLabelframe.Label", background=UIStyles.BACKGROUND_COLOR, foreground=UIStyles.SECONDARY_COLOR)
        estilo.configure("TLabel", background=UIStyles.BACKGROUND_COLOR, foreground=UIStyles.SECONDARY_COLOR)
        estilo.configure("TCheckbutton", background=UIStyles.BACKGROUND_COLOR, foreground=UIStyles.SECONDARY_COLOR)
        
        # Configuración de botones con mejor contraste - ahora en negro con texto blanco y negrita
        estilo.configure("TButton", 
                         background=UIStyles.BUTTON_BG, 
                         foreground=UIStyles.BUTTON_TEXT,
                         font=("Segoe UI", 9, "bold"))
        
        # Configuración específica para cuando el mouse pasa sobre los botones
        estilo.map("TButton",
                  foreground=[('active', UIStyles.BUTTON_TEXT),
                             ('pressed', UIStyles.BUTTON_TEXT)],
                  background=[('active', UIStyles.BUTTON_HOVER),
                             ('pressed', UIStyles.BUTTON_HOVER)])
        
        # Encabezados y subencabezados
        estilo.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), foreground=UIStyles.SECONDARY_COLOR)
        estilo.configure("Subheader.TLabel", font=("Segoe UI", 11), foreground=UIStyles.SECONDARY_COLOR)
        
        # Barra de progreso
        estilo.configure("TProgressbar", thickness=8, background=UIStyles.PRIMARY_COLOR)
        
        # Estados específicos
        estilo.configure("Success.TLabel", foreground=UIStyles.SUCCESS_COLOR)
        estilo.configure("Error.TLabel", foreground=UIStyles.ERROR_COLOR)


class UIComponentFactory:
    """
    Clase para crear componentes de UI consistentes.
    Utiliza el patrón Factory para crear widgets con estilos predefinidos.
    """
    
    @staticmethod
    def crear_frame(parent, padding=(0, 0)):
        """
        Crea un frame básico.
        
        Args:
            parent (tk.Widget): Widget padre.
            padding (tuple): Padding del frame (x, y).
            
        Returns:
            ttk.Frame: Frame configurado.
        """
        frame = ttk.Frame(parent, padding=padding)
        return frame
    
    @staticmethod
    def crear_label(parent, texto, estilo=None):
        """
        Crea una etiqueta.
        
        Args:
            parent (tk.Widget): Widget padre.
            texto (str): Texto a mostrar.
            estilo (str, optional): Estilo de la etiqueta. Default None.
            
        Returns:
            ttk.Label: Etiqueta configurada.
        """
        if estilo:
            label = ttk.Label(parent, text=texto, style=estilo)
        else:
            label = ttk.Label(parent, text=texto)
        return label
    
    @staticmethod
    def crear_checkbox(parent, texto, variable):
        """
        Crea un checkbox.
        
        Args:
            parent (tk.Widget): Widget padre.
            texto (str): Texto a mostrar.
            variable (tk.BooleanVar): Variable asociada.
            
        Returns:
            ttk.Checkbutton: Checkbox configurado.
        """
        checkbox = ttk.Checkbutton(parent, text=texto, variable=variable)
        return checkbox
    
    @staticmethod
    def crear_frame_principal(root, padding=20):
        """
        Crea un frame principal con padding estándar.
        
        Args:
            root (tk.Widget): Widget padre.
            padding (int): Padding del frame.
            
        Returns:
            ttk.Frame: Frame configurado.
        """
        frame = ttk.Frame(root, padding=padding)
        frame.pack(fill=tk.BOTH, expand=True)
        return frame
    
    @staticmethod
    def crear_frame_archivo(parent, textvariable, command, mensaje_estado_var=None):
        """
        Crea un frame para selección de archivo.
        
        Args:
            parent (tk.Widget): Widget padre.
            textvariable (tk.StringVar): Variable para mostrar ruta del archivo.
            command (function): Función a ejecutar al pulsar el botón "Seleccionar".
            mensaje_estado_var (tk.StringVar, optional): Variable para mostrar estado del archivo.
            
        Returns:
            ttk.LabelFrame: Frame configurado.
        """
        frame = ttk.LabelFrame(parent, text="Archivo de Leads", padding=(5, 8), height=180)  
        frame.pack(fill=tk.X, pady=3)
        frame.pack_propagate(False)  
        
        frame_contenido = ttk.Frame(frame)
        frame_contenido.pack(fill="both", expand=True)  
        
        # Frame superior para el selector de archivo
        frame_archivo = ttk.Frame(frame_contenido)
        frame_archivo.pack(fill=tk.X, pady=(2, 5))  
        
        button = ttk.Button(frame_archivo, text="Seleccionar Archivo", command=command, width=18)  
        button.pack(side=tk.RIGHT, pady=2)  
        
        entry = ttk.Entry(frame_archivo, textvariable=textvariable, width=30, state="readonly")  
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True)  
        
        # Frame inferior para el estado
        if mensaje_estado_var:
            frame_estado = ttk.Frame(frame_contenido)
            frame_estado.pack(fill="both", expand=True, pady=(5, 0))  
            
            ttk.Label(frame_estado, text="Estado:", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, anchor="w")  
            estado_label = ttk.Label(frame_estado, textvariable=mensaje_estado_var, wraplength=280, justify="left", font=("Segoe UI", 9))  
            estado_label.pack(side=tk.LEFT, fill="both", expand=True, padx=(5, 5), anchor="w")  
        
        return frame
    
    @staticmethod
    def crear_frame_auxiliares(parent, num_auxiliares_var, nombre_aux1_var, 
                              nombre_aux2_var, nombre_aux3_var, 
                              duplicados_var, duplicados_tel_var,
                              eliminar_duplicados_var,
                              command_actualizar):
        """
        Crea un frame para configuración de auxiliares y opciones de duplicados.
        
        Args:
            parent (tk.Widget): Widget padre.
            num_auxiliares_var (tk.IntVar): Variable para selección de número de auxiliares.
            nombre_aux1_var (tk.StringVar): Variable para nombre del auxiliar 1.
            nombre_aux2_var (tk.StringVar): Variable para nombre del auxiliar 2.
            nombre_aux3_var (tk.StringVar): Variable para nombre del auxiliar 3.
            duplicados_var (tk.BooleanVar): Variable para checkbox de duplicados por correo.
            duplicados_tel_var (tk.BooleanVar): Variable para checkbox de duplicados por teléfono.
            eliminar_duplicados_var (tk.BooleanVar): Variable para checkbox de eliminación de duplicados antes de distribuir.
            command_actualizar (function): Función para actualizar campos según número de auxiliares.
            
        Returns:
            dict: Diccionario con los componentes creados para auxiliar 3.
        """
        frame = ttk.LabelFrame(parent, text="Configuración de Auxiliares", padding=10)
        frame.pack(fill=tk.X, pady=10)
        
        # Número de auxiliares
        ttk.Label(frame, text="Número de auxiliares:").grid(row=0, column=0, sticky=tk.W, pady=5)
        frame_radio = ttk.Frame(frame)
        frame_radio.grid(row=0, column=1, sticky=tk.W)
        ttk.Radiobutton(frame_radio, text="2 Auxiliares", variable=num_auxiliares_var, 
                       value=2, command=command_actualizar).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(frame_radio, text="3 Auxiliares", variable=num_auxiliares_var, 
                       value=3, command=command_actualizar).pack(side=tk.LEFT)
        
        # Nombres de auxiliares
        ttk.Label(frame, text="Auxiliar 1:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(frame, textvariable=nombre_aux1_var, width=30).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(frame, text="Auxiliar 2:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(frame, textvariable=nombre_aux2_var, width=30).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        label_aux3 = ttk.Label(frame, text="Auxiliar 3:")
        entry_aux3 = ttk.Entry(frame, textvariable=nombre_aux3_var, width=30)
        
        # Checks de duplicados
        ttk.Checkbutton(frame, text="Buscar duplicados por correo", 
                       variable=duplicados_var).grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=5)
        ttk.Checkbutton(frame, text="Buscar duplicados por teléfono", 
                       variable=duplicados_tel_var).grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=5)
        ttk.Checkbutton(frame, text="Eliminar duplicados antes de distribuir", 
                       variable=eliminar_duplicados_var).grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        return {"label": label_aux3, "entry": entry_aux3}
    
    @staticmethod
    def crear_frame_acciones(parent, command_distribuir, command_salir, progreso_var=None):
        """
        Crea un frame con botones de acción.
        
        Args:
            parent (tk.Widget): Widget padre.
            command_distribuir (function): Función para botón Distribuir.
            command_salir (function): Función para botón Salir.
            progreso_var (tk.DoubleVar, optional): Variable para barra de progreso.
            
        Returns:
            ttk.Frame: Frame con botones de acción.
        """
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(frame, text="Realizar Distribución", command=command_distribuir).pack(side=tk.LEFT, padx=5)
        
        # Barra de progreso en el centro
        if progreso_var is not None:
            # Centro - Barra de progreso
            progressbar = ttk.Progressbar(frame, variable=progreso_var, mode='determinate', length=300)
            progressbar.pack(side=tk.LEFT, padx=20, fill="x", expand=True)
        
        ttk.Button(frame, text="Salir", command=command_salir).pack(side=tk.RIGHT, padx=5)
        
        return frame
    
    @staticmethod
    def crear_frame_estado(parent, mensaje_var, progreso_var):
        """
        Crea un frame para mostrar el estado y progreso.
        
        Args:
            parent (tk.Widget): Widget padre.
            mensaje_var (tk.StringVar): Variable para mensaje de estado.
            progreso_var (tk.DoubleVar): Variable para barra de progreso.
            
        Returns:
            ttk.Frame: Frame con indicadores de estado.
        """
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, side=tk.BOTTOM, pady=10)
        
        frame_estado = ttk.Frame(frame)
        frame_estado.pack(fill="x")
        
        ttk.Label(frame_estado, text="Estado:", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, anchor="w")  
        ttk.Label(frame_estado, textvariable=mensaje_var).pack(side=tk.LEFT, padx=5, anchor="w")
        
        ttk.Progressbar(frame, variable=progreso_var, mode='determinate', length=200).pack(side=tk.RIGHT, padx=5)
        
        return frame
