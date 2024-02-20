import os
import random
from dotenv import load_dotenv
from supabase import create_client

class SuperbaseClient:
    def __init__(self):
        """
        Inicializa el cliente de Superbase.
        """
        # Cargar variables de entorno desde el archivo .env
        load_dotenv()
        # Obtener la URL y la clave de Superbase desde las variables de entorno
        self.url = os.environ.get("SUPERBASE_URL")
        self.key = os.environ.get("SUPERBASE_KEY")
        # Crear el cliente de Superbase
        self.superbase = create_client(self.url, self.key)

    import random

    # Obtiene los datos de la tabla de superbase
    def obtener_multimedia(self, nombre_tabla, emocion):
        emocion = emocion.lower()  # Convertir a minúsculas

        indice = random.randint(1, 10)  # Genera un índice aleatorio entre 1 y 1

        # Aplicar filtros a la consulta
        consulta = self.superbase.table(nombre_tabla).select("imagen", "enlace").eq("emocion", emocion).eq("id", indice)

        # Ejecuta la consulta y obtiene los resultados
        datos = consulta.execute()

        return datos
