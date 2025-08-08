"""
Gestor de configuración para la aplicación de distribución de leads.
Permite guardar y cargar la configuración de auxiliares para que persista entre sesiones.
"""

import json
import os
from typing import Dict, Any, Optional

class ConfigManager:
    """Maneja la configuración persistente de la aplicación."""
    
    def __init__(self, config_file: str = "config.json"):
        """
        Inicializa el gestor de configuración.
        
        Args:
            config_file: Nombre del archivo de configuración
        """
        self.config_file = config_file
        self.config_path = os.path.join(os.path.dirname(__file__), config_file)
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Carga la configuración desde el archivo JSON.
        
        Returns:
            Diccionario con la configuración cargada o configuración por defecto
        """
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error al cargar configuración: {e}")
        
        # Configuración por defecto
        return {
            "auxiliares_iniciales": {
                "cantidad": 2,
                "nombres": ["Auxiliar 1", "Auxiliar 2"]
            },
            "auxiliares_finales": {
                "cantidad": 1,
                "nombres": ["Auxiliar 1"]
            },
            "opciones_duplicados": {
                "buscar_correo": True,
                "buscar_telefono": True,
                "eliminar_antes": False
            }
        }
    
    def _save_config(self) -> bool:
        """
        Guarda la configuración actual en el archivo JSON.
        
        Returns:
            True si se guardó correctamente, False en caso contrario
        """
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=4, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error al guardar configuración: {e}")
            return False
    
    def get_auxiliares_iniciales(self) -> Dict[str, Any]:
        """
        Obtiene la configuración de auxiliares iniciales.
        
        Returns:
            Diccionario con cantidad y nombres de auxiliares iniciales
        """
        return self._config.get("auxiliares_iniciales", {
            "cantidad": 2,
            "nombres": ["Auxiliar 1", "Auxiliar 2"]
        })
    
    def get_auxiliares_finales(self) -> Dict[str, Any]:
        """
        Obtiene la configuración de auxiliares finales.
        
        Returns:
            Diccionario con cantidad y nombres de auxiliares finales
        """
        return self._config.get("auxiliares_finales", {
            "cantidad": 1,
            "nombres": ["Auxiliar 1"]
        })
    
    def get_opciones_duplicados(self) -> Dict[str, bool]:
        """
        Obtiene la configuración de opciones de duplicados.
        
        Returns:
            Diccionario con las opciones de duplicados
        """
        return self._config.get("opciones_duplicados", {
            "buscar_correo": True,
            "buscar_telefono": True,
            "eliminar_antes": False
        })
    
    def save_auxiliares_iniciales(self, cantidad: int, nombres: list) -> bool:
        """
        Guarda la configuración de auxiliares iniciales.
        
        Args:
            cantidad: Número de auxiliares iniciales
            nombres: Lista con los nombres de los auxiliares
            
        Returns:
            True si se guardó correctamente
        """
        self._config["auxiliares_iniciales"] = {
            "cantidad": cantidad,
            "nombres": nombres[:cantidad]  # Solo guardar los nombres necesarios
        }
        return self._save_config()
    
    def save_auxiliares_finales(self, cantidad: int, nombres: list) -> bool:
        """
        Guarda la configuración de auxiliares finales.
        
        Args:
            cantidad: Número de auxiliares finales
            nombres: Lista con los nombres de los auxiliares
            
        Returns:
            True si se guardó correctamente
        """
        self._config["auxiliares_finales"] = {
            "cantidad": cantidad,
            "nombres": nombres[:cantidad]  # Solo guardar los nombres necesarios
        }
        return self._save_config()
    
    def save_opciones_duplicados(self, buscar_correo: bool, buscar_telefono: bool, eliminar_antes: bool) -> bool:
        """
        Guarda la configuración de opciones de duplicados.
        
        Args:
            buscar_correo: Si buscar duplicados por correo
            buscar_telefono: Si buscar duplicados por teléfono
            eliminar_antes: Si eliminar duplicados antes de distribuir
            
        Returns:
            True si se guardó correctamente
        """
        self._config["opciones_duplicados"] = {
            "buscar_correo": buscar_correo,
            "buscar_telefono": buscar_telefono,
            "eliminar_antes": eliminar_antes
        }
        return self._save_config()
    
    def save_all_config(self, auxiliares_iniciales: Dict, auxiliares_finales: Dict, opciones_duplicados: Dict) -> bool:
        """
        Guarda toda la configuración de una vez.
        
        Args:
            auxiliares_iniciales: Configuración de auxiliares iniciales
            auxiliares_finales: Configuración de auxiliares finales
            opciones_duplicados: Configuración de opciones de duplicados
            
        Returns:
            True si se guardó correctamente
        """
        self._config.update({
            "auxiliares_iniciales": auxiliares_iniciales,
            "auxiliares_finales": auxiliares_finales,
            "opciones_duplicados": opciones_duplicados
        })
        return self._save_config()
