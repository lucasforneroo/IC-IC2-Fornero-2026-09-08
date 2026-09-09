# Conceptos de HTTP y REST — Clase 2

**Materia:** Ingeniería en Computación 2  
**Guía:** Clase 2 — Parte A: Entender HTTP antes de escribir código

---

## A1. Métodos HTTP para Operaciones con Libros

- **Consultar una lista de libros:** `GET /libros`  
  *Justificación:* Operación de solo lectura para obtener la representación del recurso.
- **Agregar un libro nuevo:** `POST /libros`  
  *Justificación:* Crea un nuevo recurso subordinado dentro de la colección.
- **Modificar el título de un libro:** `PATCH /libros/{id}` (o `PUT /libros/{id}`)  
  *Justificación:* `PATCH` se utiliza para modificaciones parciales (solo el campo `titulo`), mientras que `PUT` se utiliza si se envía el objeto completo para reemplazarlo.
- **Eliminar un libro:** `DELETE /libros/{id}`  
  *Justificación:* Solicita la eliminación del recurso identificado por su ID.

---

## A2. Idempotencia y el Método GET

- **¿Qué significa que una operación sea idempotente?**  
  Una operación es idempotente si ejecutarla una o múltiples veces consecutivas produce exactamente el mismo efecto sobre el estado del servidor.
- **¿Por qué GET debe ser idempotente?**  
  `GET` es un método seguro y de solo lectura. Realizar 1 o 100 consultas `GET /libros` no debe alterar ni mutar los datos en el servidor, lo que garantiza reintentos seguros ante fallas de red y permite el almacenamiento en caché.

---

## A3. Códigos de Estado HTTP

- **200 OK:** Todo salió bien y la respuesta incluye contenido (ej. lista de libros obtenida con `GET`).
- **201 Created:** Se creó exitosamente un nuevo recurso en el servidor (ej. respuesta a un `POST /libros`).
- **404 Not Found:** El recurso solicitado no existe en el servidor (ej. `GET /libros/999`).
- **422 Unprocessable Entity:** El body enviado tiene sintaxis JSON válida pero contiene errores de validación o tipos de datos incompatibles (ej. `"paginas": "muchas"` en FastAPI/Pydantic).  
  *(Nota: `400 Bad Request` se reserva para sintaxis malformada, como un JSON roto).*

---

## A4. Header de Formato del Body

- **Header requerido:** `Content-Type: application/json`
- **Función:** Informa al servidor cómo debe interpretar y deserializar los bytes recibidos en el cuerpo (*body*) de la petición. Si se omite, el servidor no sabrá que recibe un JSON y rechazará la solicitud (típicamente con error `422` o `415 Unsupported Media Type`).

---

## A5. Diferencia entre Path Param y Query Param

- **Path Param (Parámetro de Ruta):**  
  Forma parte de la ruta de la URL y se usa para **identificar unívocamente un recurso específico**.  
  *Ejemplo:* `GET /libros/42` (el `42` identifica al libro puntual).
- **Query Param (Parámetro de Consulta):**  
  Aparece luego del signo `?` en la URL y se usa para **filtrar, ordenar o paginar** resultados sin cambiar la identidad del recurso base.  
  *Ejemplo:* `GET /libros?paginas_min=200&orden=asc` (`paginas_min` y `orden` modifican la vista/filtro).

---

## A6. POST a un Endpoint que solo Acepta GET

- **¿Qué pasa?** El servidor reconoce que la URL existe pero rechaza la petición porque el método `POST` no está soportado para ese recurso.
- **Código de estado esperado:** `405 Method Not Allowed`.  
  *(El estándar HTTP exige además que el servidor envíe el header `Allow` indicando los métodos permitidos, ej. `Allow: GET, HEAD`).*

---

## A7. ¿Por qué es una Mala Práctica Usar GET para Eliminar un Recurso?

Usar `GET /libros/123/eliminar` viola la semántica HTTP y genera graves problemas:
1. **Web Crawlers e Indexadores:** Motores de búsqueda (Googlebot, Bing) siguen automáticamente todos los enlaces `<a href="...">` con peticiones `GET`, borrando la base de datos al indexar.
2. **Prefetching de Navegadores:** Los navegadores descargan enlaces en segundo plano de manera preventiva para acelerar la navegación, ejecutando el borrado sin que el usuario haga clic.
3. **Caché y Proxies:** Los intermediarios (CDNs, proxies) almacenan en caché las respuestas `GET` o repiten peticiones de lectura, generando inconsistencias.
4. **Ataques CSRF Triviales:** Un atacante puede incrustar una etiqueta `<img src="https://api.com/libros/123/eliminar" />` en cualquier sitio web; el navegador de la víctima ejecutará el borrado automáticamente usando su sesión activa.
