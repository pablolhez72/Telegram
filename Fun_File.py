#solo funciones RAG     

import os # Necesario para interactuar con el sistema operativo, aunque no lo usemos directamente aquí, es buena práctica si después se manejan rutas

def Carga_RAG(nombre_archivo: str) -> str | None:
    """
    Carga el contenido de un archivo de texto en una cadena de texto (string).
    Args:
        nombre_archivo (str): El nombre o la ruta completa del archivo a cargar.
    Returns:
        str: El contenido completo del archivo si se lee correctamente.
        None: Si el archivo no se encuentra o hay un error durante la lectura.
    """
    try:
        with open(nombre_archivo, 'r', encoding='cp1252') as file:
            contenido = file.read()
        print(f"✔️ Contenido del archivo '{nombre_archivo}' cargado exitosamente.")
        return contenido
    except FileNotFoundError:
        print(f"❌ Error: El archivo '{nombre_archivo}' no se encontró. Por favor, verifica la ruta.")
        return None
    except Exception as e:
        print(f"❌ Ocurrió un error inesperado al leer el archivo '{nombre_archivo}': {e}")
        return None