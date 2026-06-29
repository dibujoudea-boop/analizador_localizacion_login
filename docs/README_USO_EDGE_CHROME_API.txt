README - USO DEL ANALIZADOR LOCALIZACIÓN DE LOGIN EN EDGE O CHROME
=================================================================

Proyecto: Analizador Localización de Login
Objetivo: probar la API funcional desde el navegador mediante la documentación interactiva de FastAPI.

1. Antes de abrir el navegador
------------------------------
La API debe estar ejecutándose previamente en PowerShell.

En PowerShell debe verse un mensaje similar a:

    Uvicorn running on http://127.0.0.1:8000
    Application startup complete

No cierres PowerShell mientras uses la API. Si lo cierras, el navegador dejará de conectarse al servicio.

2. Abrir la documentación de la API
-----------------------------------
Abre Microsoft Edge o Google Chrome y escribe en la barra de direcciones:

    http://127.0.0.1:8000/docs

Presiona Enter.

Deberías ver una página titulada:

    Analizador Localización de Login

La página corresponde a la documentación Swagger generada automáticamente por FastAPI.

3. Probar el endpoint principal GET /
------------------------------------
Este endpoint sirve para comprobar que la API está activa.

Pasos:

1. Haz clic sobre:

    GET /

2. Pulsa el botón:

    Try it out

3. Pulsa:

    Execute

4. Revisa la respuesta.

Si el servicio funciona, deberías ver un código de respuesta 200.

4. Probar el análisis de un evento de login
------------------------------------------
El endpoint principal del prototipo es:

    POST /login-event

Este endpoint recibe un evento de login en formato JSON, calcula el score de riesgo, asigna un nivel de riesgo, recomienda una acción y devuelve las razones activadas.

Pasos:

1. En la página /docs, abre:

    POST /login-event

2. Pulsa:

    Try it out

3. En el cuadro "Request body", borra el contenido de ejemplo.

4. Pega este JSON de prueba:

{
  "user_id": "u001",
  "timestamp": "2026-05-06T23:30:00",
  "ip": "45.155.205.16",
  "known_location": "Bogota",
  "declared_city": "Moscow",
  "declared_region": "Moscow",
  "declared_country": "Russia",
  "timezone_offset": "+03:00",
  "user_agent": "Tor Browser",
  "device_type": "desktop",
  "network_type": "tor",
  "asn": "AS9009",
  "is_proxy": 1,
  "is_vpn": 0,
  "is_hosting": 1,
  "ip_reputation": "high",
  "is_new_device": 1,
  "country_change": 1,
  "distance_from_prev_km": 10898.4,
  "time_since_prev_min": 20.0,
  "travel_speed_kmh": 32695.2,
  "timezone_mismatch": 1,
  "scenario_type": "suspicious",
  "expected_result": "alto"
}

5. Pulsa:

    Execute

5. Resultado esperado del endpoint /login-event
-----------------------------------------------
Si todo funciona correctamente, el servidor responderá con código 200 y un cuerpo de respuesta similar a:

{
  "user_id": "u001",
  "risk_score": 127,
  "risk_level": "alto",
  "recommended_action": "block_or_review",
  "risk_reasons": [
    "localizacion_distinta_a_la_habitual",
    "cambio_de_pais",
    "nuevo_dispositivo",
    "red_sospechosa:tor",
    "indicador_proxy",
    "indicador_hosting",
    "desajuste_de_zona_horaria",
    "horario_atipico",
    "viaje_imposible",
    "reputacion_ip_alta"
  ],
  "message": "Riesgo alto: se recomienda bloquear preventivamente o escalar el evento para revisión."
}

El resultado esperado es riesgo alto porque el evento simula un acceso desde un país distinto, red Tor, proxy, hosting, reputación IP alta, dispositivo nuevo, desajuste horario y viaje imposible.

6. Consultar eventos recientes
------------------------------
Después de ejecutar el POST /login-event, prueba el endpoint:

    GET /events/recent

Pasos:

1. Abre:

    GET /events/recent

2. Pulsa:

    Try it out

3. En el campo limit, escribe:

    20

4. Pulsa:

    Execute

5. Revisa el resultado.

La respuesta debe mostrar una lista de eventos procesados recientemente. Allí debería aparecer el evento enviado en el paso anterior, junto con su score, nivel de riesgo, acción recomendada y razones activadas.

7. Qué capturas son útiles para el TFM
--------------------------------------
Para documentar la ejecución funcional del prototipo, son útiles estas capturas:

1. Pantalla general de Swagger en:

    http://127.0.0.1:8000/docs

2. Respuesta del endpoint:

    POST /login-event

3. Respuesta del endpoint:

    GET /events/recent

4. Consola de PowerShell mostrando:

    Uvicorn running on http://127.0.0.1:8000
    Código HTTP 200 OK en las peticiones

8. Problemas frecuentes en el navegador
---------------------------------------

Problema: la página http://127.0.0.1:8000/docs no abre
Solución:
- Verifica que PowerShell esté abierto.
- Verifica que el servidor esté ejecutándose.
- Confirma que la URL esté escrita exactamente como http://127.0.0.1:8000/docs.
- No uses https, porque el prototipo local se ejecuta con http.

Problema: aparece "This site can't be reached" o "No se puede acceder a este sitio"
Solución:
- El servidor probablemente no está iniciado.
- Vuelve a PowerShell y ejecuta:

    python -m uvicorn src.api_login_analyzer:app --reload

Problema: el endpoint devuelve error 422
Solución:
- El JSON tiene un campo faltante, un nombre incorrecto o un tipo de dato inválido.
- Copia nuevamente el JSON de prueba completo.
- Revisa que las comillas sean dobles y que no falten comas.

Problema: no aparecen eventos en /events/recent
Solución:
- Primero ejecuta POST /login-event.
- Después ejecuta GET /events/recent.
- Si reiniciaste la aplicación o borraste la base local, puede que no haya eventos almacenados todavía.

9. Cierre de la prueba
----------------------
Cuando termines de probar la API:

1. Vuelve a PowerShell.
2. Presiona:

    Ctrl + C

Esto detiene el servidor local.
