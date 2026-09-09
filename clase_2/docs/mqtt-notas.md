# Notas y Respuestas Conceptuales — MQTT (D1 a D8)

Guía de Ejercicios — Clase 2

---

### D1: Rol del broker en MQTT y comunicación entre clientes
**Respuesta:**  
El broker actúa como servidor central intermediario encargado de recibir todos los mensajes de los publicadores, filtrar los topics y distribuirlos a los clientes que se hayan suscrito a ellos. Los clientes **nunca** se comunican directamente entre sí; toda comunicación pasa exclusivamente a través del broker.

---

### D2: Evaluación de suscripciones ante publicación en `casa/cocina/temperatura`
**Respuesta:**  
Ante un mensaje publicado en `casa/cocina/temperatura`, la evaluación de cada suscripción es:

- **a) `casa/+/temperatura` (SÍ):** Coincide porque el comodín `+` reemplaza exactamente un único nivel intermedio (`cocina`).
- **b) `casa/cocina/#` (SÍ):** Coincide porque `#` abarca todos los subniveles a partir de `casa/cocina/` (en este caso `temperatura`).
- **c) `casa/#` (SÍ):** Coincide porque `#` abarca cualquier cantidad de niveles sucesivos después de `casa/` (`cocina/temperatura`).
- **d) `casa/+/+` (SÍ):** Coincide porque utiliza dos comodines de nivel simple para cubrir exactamente los dos niveles restantes (`cocina` y `temperatura`).
- **e) `+/+/temperatura` (SÍ):** Coincide porque los dos primeros niveles son cubiertos por sendos `+` (`casa` y `cocina`) y el último coincide con `temperatura`.
- **f) `casa/living/temperatura` (NO):** No coincide porque el segundo nivel especifica `living` y el mensaje se publicó en `cocina`.

---

### D3: Diferencia entre wildcards `+` y `#`
**Respuesta:**  
- **`+` (Nivel individual):** Coincide con **un solo nivel jerárquico**. Puede utilizarse en cualquier posición del topic (inicio, medio o fin) y repetirse varias veces dentro de la ruta (ej. `casa/+/temperatura`, `+/+/luz`).
- **`#` (Multinivel):** Coincide con **cero o más niveles jerárquicos**. Solo puede ubicarse obligatoriamente al **final** del topic precedido por una barra `/` (ej. `casa/#`, `casa/cocina/#`).

---

### D4: Diferencias entre QoS 0, QoS 1 y QoS 2
**Respuesta:**  
- **QoS 0 (At most once / A lo sumo una vez):** "Disparar y olvidar". El mensaje se envía sin confirmación de recepción ni reintentos; puede perderse si hay inestabilidad en la red.  
  *Caso de uso:* Lecturas periódicas de sensores de temperatura cada 5 segundos (perder una muestra no es crítico, pues el dato se refresca enseguida).
- **QoS 1 (At least once / Al menos una vez):** Garantiza la entrega del mensaje requiriendo confirmación (`PUBACK`). Si no se recibe la confirmación a tiempo, se reintenta el envío, lo que puede provocar mensajes duplicados.  
  *Caso de uso:* Alerta por fuga de gas o evento crítico de seguridad (es fundamental que llegue, siendo preferible un duplicado antes que perder la alarma).
- **QoS 2 (Exactly once / Exactamente una vez):** Garantiza que el mensaje se reciba una y solo una vez mediante un handshake de cuatro pasos (`PUBLISH`, `PUBREC`, `PUBREL`, `PUBCOMP`), eliminando pérdidas y duplicados a costa de mayor tráfico y latencia.  
  *Caso de uso:* Transacción de pago o comandos no idempotentes críticos donde una duplicación generaría inconsistencias graves.

---

### D5: Mensajes "retained" en MQTT
**Respuesta:**  
- **Qué es:** Es un mensaje publicado con la bandera `retain=True`.
- **Para qué sirve:** Indica al broker que debe almacenar en memoria el último valor recibido para ese topic específico, en lugar de descartarlo tras enviarlo a los suscriptores activos.
- **Qué recibe un suscriptor nuevo:** Al suscribirse al topic, el nuevo cliente recibe de forma **inmediata** el último mensaje retenido, conociendo el último estado disponible sin tener que esperar a que el publicador emita una nueva lectura.

---

### D6: Ventajas de MQTT sobre HTTP para dispositivos IoT con batería
**Respuesta:**  
1. **Mínimo overhead de red:** Los paquetes MQTT tienen cabeceras fijas de apenas **2 bytes**, en contraste con las cabeceras HTTP en texto plano que consumen cientos de bytes por petición.
2. **Conexión TCP persistente:** Se mantiene un socket abierto reutilizable, eliminando el consumo energético de reabrir conexiones TCP y renegociar sesiones TLS en cada reporte.
3. **Modelo Push vs. Polling:** Los datos se transmiten únicamente cuando ocurren eventos o cambios de estado, evitando que el dispositivo a batería deba consultar periódicamente al servidor.

---

### D7: Comparación Request-Response vs. Publish-Subscribe
**Respuesta:**  
- **Request-Response (HTTP):** Modelo punto a punto acoplado. El cliente debe conocer la dirección exacta del servidor y ambos deben estar activos simultáneamente para completar el ciclo de petición y respuesta.
- **Publish-Subscribe (MQTT):** Modelo mediado por un broker que ofrece **desacoplamiento espacial** (el emisor no conoce la identidad, dirección ni cantidad de receptores) y **desacoplamiento temporal** (los clientes no necesitan estar conectados en el mismo instante si se emplean sesiones persistentes o mensajes retenidos).

---

### D8: Comparación de carga y conexiones (Cálculo numérico)
**Respuesta:**  
Para un escenario con **100 sensores** reportando cada 1 segundo:

- **HTTP (Polling / Peticiones individuales):**  
  Cada sensor genera 60 peticiones por minuto.  
  $$\text{Total} = 100 \text{ sensores} \times 60 \text{ req/min} = 6.000 \text{ peticiones/conexiones por minuto al servidor.}$$
- **MQTT (Conexión persistente):**  
  Se mantienen únicamente **100 conexiones TCP persistentes y abiertas en total**, sobre las cuales los sensores transmiten sus datos en tiempo real con una sobrecarga de red mínima.
