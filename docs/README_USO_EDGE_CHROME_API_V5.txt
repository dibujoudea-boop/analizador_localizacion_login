README - USO DEL ANALIZADOR LOCALIZACIÓN DE LOGIN V5 EN EDGE O CHROME
================================================================================

Proyecto: Analizador Localización de Login
Objetivo: probar y documentar la API v5 desde la interfaz Swagger de FastAPI.

1. ANTES DE ABRIR EL NAVEGADOR
------------------------------
La API debe estar ejecutándose previamente en PowerShell con:

    python -m uvicorn src.api_e2e:app --reload

En PowerShell debe aparecer:

    Uvicorn running on http://127.0.0.1:8000
    Application startup complete

No cierres PowerShell durante la prueba.

2. ABRIR LA DOCUMENTACIÓN INTERACTIVA
-------------------------------------
Abre Microsoft Edge o Google Chrome y entra a:

    http://127.0.0.1:8000/docs

No utilices https en la ejecución local.

La página debe mostrar cuatro endpoints:

    GET  /
    POST /login-event
    POST /login-event/raw
    GET  /events/recent

3. ACTUALIZAR LA PÁGINA SI MUESTRA UNA VERSIÓN ANTIGUA
------------------------------------------------------
Si aparecen solamente tres endpoints:
1. Verifica que PowerShell esté ejecutando:

    python -m uvicorn src.api_e2e:app --reload

2. En el navegador presiona Ctrl + F5.
3. Si persiste, cierra la pestaña y abre nuevamente /docs.

4. PROBAR GET /
--------------
1. Haz clic en GET /.
2. Pulsa Try it out.
3. Pulsa Execute.
4. Verifica que el código sea HTTP 200.

5. PROBAR POST /login-event/raw
-------------------------------
Este endpoint ejecuta el pipeline funcional v5 a partir de un evento mínimo.

1. Abre POST /login-event/raw.
2. Pulsa Try it out.
3. Borra el contenido de ejemplo.
4. Pega:

{
  "user_id": "demostracion_v5_001"
}

5. Pulsa Execute.
6. Revisa Server response.
7. Confirma que el código sea 200.

La respuesta debe incluir campos semejantes a:

{
  "user_id": "demostracion_v5_001",
  "risk_score": 0,
  "risk_level": "bajo",
  "recommended_action": "allow",
  "risk_reasons": [],
  "message": "..."
}

Los valores concretos pueden variar según la IP observada, el historial disponible y el enriquecimiento realizado.

IMPORTANTE: una ejecución local puede usar 127.0.0.1 o una IP privada. Por tanto, no es obligatorio que el resultado sea de riesgo alto. Esta prueba demuestra que el pipeline recibe, procesa, responde y persiste un evento.

6. PROBAR POST /login-event
---------------------------
Este endpoint permite analizar un evento que ya contiene señales contextuales previamente estructuradas. Se conserva para compatibilidad y validación del motor v4.

Para la documentación final del pipeline v5, la evidencia principal debe corresponder a /login-event/raw.

7. CONSULTAR GET /events/recent
-------------------------------
Después de ejecutar /login-event/raw:
1. Abre GET /events/recent.
2. Pulsa Try it out.
3. En limit escribe 20.
4. Pulsa Execute.
5. Busca demostracion_v5_001.

La respuesta debe mostrar el evento almacenado con su score, nivel de riesgo, acción y razones activadas.

8. CAPTURAS RECOMENDADAS PARA EL TFM
------------------------------------
FIGURA DE SWAGGER
- Contrae todos los endpoints.
- Ajusta el zoom entre 80 % y 90 %.
- Procura que sean visibles los cuatro endpoints.
- Presiona Windows + Shift + S.
- Guarda como:

    figura_6_swagger_cuatro_endpoints_v5.png

Título sugerido:

    Figura 6. Documentación interactiva de la API funcional del Analizador Localización de Login

FIGURA DE /login-event/raw
- Ejecuta el JSON mínimo.
- Incluye endpoint, Request body, código 200 y Response body.
- Guarda como:

    figura_7_respuesta_login_event_raw_v5.png

Título sugerido:

    Figura 7. Respuesta del endpoint /login-event/raw durante la prueba funcional del pipeline v5

FIGURA DE /events/recent
- Ejecuta GET /events/recent.
- Incluye endpoint, código 200 y el evento demostracion_v5_001.
- Guarda como:

    figura_8_eventos_recientes_pipeline_v5.png

Título sugerido:

    Figura 8. Consulta del evento generado por el pipeline v5 mediante /events/recent

FIGURA DE POWERSHELL
La captura debe mostrar:

    python -m uvicorn src.api_e2e:app --reload
    Uvicorn running on http://127.0.0.1:8000
    Application startup complete

Guarda como:

    figura_5_ejecucion_uvicorn_v5.png

9. RECOMENDACIONES PARA CAPTURAS PROFESIONALES
----------------------------------------------
- Oculta la barra de favoritos con Ctrl + Shift + B.
- No incluyas otras pestañas personales.
- No muestres rutas con nombres personales cuando no sean necesarias.
- Utiliza zoom suficiente para que los textos se lean en Word y PDF.
- Recorta espacios vacíos.
- Conserva la relación de aspecto.
- No deformes la imagen al insertarla.
- Usa el ajuste "En línea con el texto" en Word.
- Añade título encima y fuente debajo según la plantilla UNIR.

10. PROBLEMAS FRECUENTES
------------------------
PROBLEMA: No abre http://127.0.0.1:8000/docs
- Verifica que PowerShell siga abierto.
- Confirma que Uvicorn está ejecutándose.
- Usa http, no https.

PROBLEMA: Solo aparecen tres endpoints
- Detén el servidor.
- Ejecuta:

    python -m uvicorn src.api_e2e:app --reload

- Actualiza con Ctrl + F5.

PROBLEMA: Error 422
- Para /login-event/raw utiliza:

{
  "user_id": "demostracion_v5_001"
}

- Usa comillas dobles y no elimines llaves.

PROBLEMA: Error 500
- Revisa PowerShell para identificar el error.
- Confirma dependencias.
- Reinicia el servidor.

PROBLEMA: No aparece el evento en /events/recent
1. Ejecuta primero POST /login-event/raw.
2. Después ejecuta GET /events/recent.
3. Busca el mismo user_id.
4. Si se borró o reinició la base local, genera nuevamente el evento.

11. CIERRE DE LA PRUEBA
-----------------------
1. Vuelve a PowerShell.
2. Presiona Ctrl + C.
3. Cierra el navegador.
4. No subas a GitHub cachés, bases SQLite o resultados que contengan IP reales.
