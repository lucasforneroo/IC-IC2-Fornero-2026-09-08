"""Cliente HTTP robusto para interactuar con la API REST de Libros.

Implementa los ejercicios de la Parte C:
- C1 y C2: Peticiones GET y POST programáticas con serialización JSON.
- C4: Inspección de códigos de estado (200, 201, 404, 422).
- C5: Operaciones PUT y DELETE.
- C6: Captura de ConnectionError cuando el servidor está caído.
- C7: Configuración de timeout y manejo de Timeout exceptions.
- C8: Reutilización de conexiones TCP mediante requests.Session.
"""

from typing import List, Dict, Any, Optional
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException


class ClienteAPI:
    """Cliente HTTP orientado a objetos con pooling de conexiones y manejo defensivo."""

    def __init__(self, base_url: str = "http://127.0.0.1:8000", timeout: float = 5.0):
        """Inicializa el cliente con una URL base y timeout predeterminado.

        Args:
            base_url: URL raíz del servicio API (sin barra final).
            timeout: Tiempo máximo de espera en segundos por petición (Ejercicio C7).
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        # Reutilización de conexiones persistentes vía Session (Ejercicio C8)
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def close(self) -> None:
        """Cierra la sesión activa liberando sockets y recursos de red."""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def saludar(self) -> Optional[Dict[str, str]]:
        """Verifica la conectividad básica con el endpoint GET / (Ejercicio B1)."""
        url = f"{self.base_url}/"
        try:
            resp = self.session.get(url, timeout=self.timeout)
            if resp.status_code == 200:
                return resp.json()
            print(f"[ERROR] Código inesperado en /: {resp.status_code}")
            return None
        except ConnectionError:
            print("[ERROR C6] No se pudo conectar con la API. ¿Está levantado el servidor Uvicorn?")
            return None
        except Timeout:
            print(f"[ERROR C7] Tiempo de espera agotado ({self.timeout}s) al consultar {url}.")
            return None

    def listar_libros(self, paginas_min: Optional[int] = None) -> List[Dict[str, Any]]:
        """Consulta la lista de libros disponibles en la API (Ejercicio C1).

        Args:
            paginas_min: Filtro opcional de páginas mínimas (Ejercicio B11).

        Returns:
            Lista de diccionarios de libros o lista vacía en caso de error.
        """
        url = f"{self.base_url}/libros"
        params = {"paginas_min": paginas_min} if paginas_min is not None else None

        try:
            resp = self.session.get(url, params=params, timeout=self.timeout)
            if resp.status_code == 200:
                return resp.json()
            print(f"[AVISO C4] Código {resp.status_code}: {resp.text}")
            return []
        except ConnectionError:
            print("[ERROR C6] Servidor no alcanzable. Conexión rechazada.")
            return []
        except Timeout:
            print("[ERROR C7] Timeout al listar libros.")
            return []

    def crear_libro(self, datos_libro: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Envía una petición POST para dar de alta un libro (Ejercicio C2 y C3).

        Args:
            datos_libro: Diccionario con la estructura del libro a crear.

        Returns:
            Diccionario del libro creado o None si la operación falla.
        """
        url = f"{self.base_url}/libros"
        try:
            resp = self.session.post(url, json=datos_libro, timeout=self.timeout)

            # Ejercicio C4: Reaccionar según el código de estado HTTP
            if resp.status_code == 201:
                print(f"[OK 201] Libro creado con éxito: {datos_libro.get('titulo')}")
                return resp.json()
            elif resp.status_code == 422:
                print(f"[VALIDACIÓN 422] Datos inválidos enviados: {resp.json()}")
                return None
            elif resp.status_code == 400:
                print(f"[CONFLICTO 400] Error de negocio: {resp.json().get('detail')}")
                return None
            else:
                print(f"[ERROR {resp.status_code}] Respuesta: {resp.text}")
                return None
        except ConnectionError:
            print("[ERROR C6] No se pudo conectar con el servidor.")
            return None
        except Timeout:
            print("[ERROR C7] Timeout superado al crear libro.")
            return None

    def obtener_libro(self, titulo: str) -> Optional[Dict[str, Any]]:
        url = f"{self.base_url}/libros/{titulo}"
        try:
            resp = self.session.get(url, timeout=self.timeout)
            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code == 404:
                print(f"[NO EXISTE 404] El libro '{titulo}' no fue encontrado.")
                return None
            else:
                print(f"[ERROR {resp.status_code}] {resp.text}")
                return None
        except ConnectionError:
            print("[ERROR C6] Conexión fallida al obtener libro.")
            return None

    def actualizar_libro(self, titulo: str, datos_actualizados: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        url = f"{self.base_url}/libros/{titulo}"
        try:
            resp = self.session.put(url, json=datos_actualizados, timeout=self.timeout)
            if resp.status_code == 200:
                print(f"[OK 200] Libro '{titulo}' actualizado exitosamente.")
                return resp.json()
            elif resp.status_code == 404:
                print(f"[NO EXISTE 404] No se puede actualizar; el libro '{titulo}' no existe.")
                return None
            elif resp.status_code == 422:
                print(f"[VALIDACIÓN 422] Error en datos de actualización: {resp.json()}")
                return None
            return None
        except ConnectionError:
            print("[ERROR C6] Error de conexión al actualizar libro.")
            return None

    def borrar_libro(self, titulo: str) -> bool:
        """Elimina un libro mediante DELETE (Ejercicio C5).

        Args:
            titulo: Título del libro a eliminar.

        Returns:
            True si fue eliminado con éxito (204), False en caso contrario.
        """
        url = f"{self.base_url}/libros/{titulo}"
        try:
            resp = self.session.delete(url, timeout=self.timeout)
            if resp.status_code == 204:
                print(f"[OK 204] Libro '{titulo}' eliminado correctamente.")
                return True
            elif resp.status_code == 404:
                print(f"[NO EXISTE 404] No se puede eliminar; el libro '{titulo}' no existe.")
                return False
            return False
        except ConnectionError:
            print("[ERROR C6] Error de conexión al borrar libro.")
            return False


if __name__ == "__main__":
    print("=== Demo de Consumo Cliente API (Clase 2) ===")
    cliente = ClienteAPI()

    # 1. Probar saludo
    print("\n1. Verificando estado del servidor...")
    saludo = cliente.saludar()
    print(f"Respuesta saludo: {saludo}")

    if saludo:
        # 2. Listar libros iniciales
        print("\n2. Listando libros...")
        libros = cliente.listar_libros()
        for lib in libros:
            print(f"  - {lib.get('titulo')} ({lib.get('paginas')} págs)")

        # 3. Crear un nuevo libro válido
        print("\n3. Creando libro nuevo...")
        nuevo = {
            "titulo": "El Túnel",
            "paginas": 160,
            "autor": "Ernesto Sabato",
            "disponible": True,
            "editorial": {"nombre": "Sur", "pais": "Argentina"},
        }
        cliente.crear_libro(nuevo)

        # 4. Forzar un 422 (páginas inválidas)
        print("\n4. Provocando validación 422 a propósito (páginas = -5)...")
        invalido = {"titulo": "Libro Fallido", "paginas": -5}
        cliente.crear_libro(invalido)

        # 5. Buscar libro existente y no existente
        print("\n5. Consultando libros individuales...")
        cliente.obtener_libro("El Túnel")
        cliente.obtener_libro("LibroFantasma123")

    cliente.close()
