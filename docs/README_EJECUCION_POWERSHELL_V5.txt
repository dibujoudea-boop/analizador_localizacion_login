README - EJECUCIÓN DEL ANALIZADOR LOCALIZACIÓN DE LOGIN V5 EN POWERSHELL
================================================================================

Proyecto: Analizador Localización de Login
Versión recomendada: v5
Entorno: Windows + PowerShell + Python + FastAPI/Uvicorn

1. OBJETIVO
-----------
Este documento explica cómo descargar, preparar y ejecutar localmente la versión v5 del Analizador Localización de Login.

La versión v5 incorpora:
- API REST desarrollada con FastAPI.
- Endpoint /login-event para eventos previamente enriquecidos.
- Endpoint /login-event/raw para ejecutar el pipeline extremo a extremo.
- Consulta de eventos mediante /events/recent.
- Persistencia local mediante SQLite.
- Captura de señales HTTP, enriquecimiento, historial y scoring contextual.

2. REQUISITOS PREVIOS
---------------------
Antes de ejecutar el prototipo, confirma que tienes instalado:
- Python 3.10 o superior.
- Git, si vas a clonar el repositorio.
- Microsoft Edge o Google Chrome.
- Conexión a Internet para instalar dependencias la primera vez.

Comprobar Python:

    python --version

Si Windows no reconoce el comando, prueba:

    py --version

Comprobar Git:

    git --version

3. DESCARGAR O ACTUALIZAR EL PROYECTO
-------------------------------------
OPCIÓN A. Descargar como ZIP

1. Abre el repositorio:

    https://github.com/dibujoudea-boop/analizador_localizacion_login

2. Pulsa Code > Download ZIP.
3. Descomprime el archivo.
4. Abre la carpeta principal del proyecto.

OPCIÓN B. Clonar con Git

    git clone https://github.com/dibujoudea-boop/analizador_localizacion_login.git
    cd analizador_localizacion_login

OPCIÓN C. Actualizar una copia ya clonada

    git pull origin main

4. VERIFICAR QUE ES LA VERSIÓN V5
---------------------------------
En la carpeta principal deben existir, como mínimo:

    src/
    data/
    docs/
    figures/
    notebooks/
    outputs/
    README.md
    requirements.txt

Dentro de src/ deben aparecer archivos como:

    api_login_analyzer.py
    api_e2e.py
    capture.py
    enrichment.py
    geo_cache.py
    history.py
    pipeline.py
    risk_engine.py
    schemas.py
    storage.py

Para comprobarlo desde PowerShell:

    Get-ChildItem
    Get-ChildItem .\src

La presencia de src\api_e2e.py es necesaria para ejecutar el endpoint /login-event/raw.

5. ABRIR POWERSHELL EN LA CARPETA DEL PROYECTO
----------------------------------------------
Método recomendado:
1. Abre la carpeta principal del proyecto en el Explorador de archivos.
2. Haz clic en la barra de dirección.
3. Escribe powershell.
4. Presiona Enter.

La línea debe quedar aproximadamente así:

    PS C:\ruta\al\analizador_localizacion_login>

También puedes navegar manualmente:

    cd "C:\ruta\al\analizador_localizacion_login"

6. CREAR EL ENTORNO VIRTUAL
---------------------------
Este paso solo es necesario la primera vez en esa carpeta:

    python -m venv .venv

Si utilizas el lanzador de Python:

    py -m venv .venv

7. ACTIVAR EL ENTORNO VIRTUAL
-----------------------------

    .\.venv\Scripts\Activate.ps1

Si se activa correctamente, verás:

    (.venv) PS C:\ruta\al\analizador_localizacion_login>

Si PowerShell bloquea la ejecución de scripts:

    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

Después vuelve a activar:

    .\.venv\Scripts\Activate.ps1

Esta modificación solo se aplica a la ventana actual.

8. INSTALAR LAS DEPENDENCIAS
----------------------------
Con el entorno virtual activado:

    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt

9. EJECUTAR LA API V5
---------------------
Comando recomendado:

    python -m uvicorn src.api_e2e:app --reload

IMPORTANTE: no uses este comando para documentar la versión v5:

    python -m uvicorn src.api_login_analyzer:app --reload

Ese módulo corresponde a la aplicación base y puede mostrar únicamente tres endpoints.
La ejecución con src.api_e2e:app incorpora /login-event/raw.

Si todo funciona, PowerShell mostrará mensajes similares a:

    INFO:     Uvicorn running on http://127.0.0.1:8000
    INFO:     Started server process
    INFO:     Waiting for application startup.
    INFO:     Application startup complete.

No cierres PowerShell mientras utilizas la API.

10. ABRIR SWAGGER EN EL NAVEGADOR
---------------------------------
Con el servidor activo, abre Edge o Chrome y entra a:

    http://127.0.0.1:8000/docs

Deben aparecer cuatro endpoints:

    GET  /
    POST /login-event
    POST /login-event/raw
    GET  /events/recent

11. COMPROBAR EL ESTADO DEL SERVICIO
------------------------------------
En Swagger:
1. Abre GET /.
2. Pulsa Try it out.
3. Pulsa Execute.
4. Comprueba que la respuesta sea HTTP 200.

12. EJECUTAR EL PIPELINE V5
---------------------------
En Swagger:
1. Abre POST /login-event/raw.
2. Pulsa Try it out.
3. Utiliza este cuerpo mínimo:

{
  "user_id": "demostracion_v5_001"
}

4. Pulsa Execute.
5. Comprueba que la respuesta sea HTTP 200.

La respuesta debe contener campos semejantes a:

    user_id
    risk_score
    risk_level
    recommended_action
    risk_reasons
    message

Una ejecución local puede obtener una IP de loopback o privada. Por ello, el resultado no tiene que ser necesariamente de riesgo alto. El objetivo es verificar el funcionamiento integral del pipeline.

13. CONSULTAR EVENTOS RECIENTES
-------------------------------
Después de ejecutar /login-event/raw:
1. Abre GET /events/recent.
2. Pulsa Try it out.
3. Introduce limit = 20.
4. Pulsa Execute.
5. Busca demostracion_v5_001.

La respuesta debe incluir el evento procesado y sus resultados.

14. DETENER EL SERVIDOR
-----------------------
Vuelve a PowerShell y presiona:

    Ctrl + C

15. EJECUCIÓN RÁPIDA EN SESIONES POSTERIORES
--------------------------------------------

    cd "C:\ruta\al\analizador_localizacion_login"
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    .\.venv\Scripts\Activate.ps1
    python -m uvicorn src.api_e2e:app --reload

Después abre:

    http://127.0.0.1:8000/docs

16. ERRORES FRECUENTES
----------------------
ERROR: No module named src
- Confirma que estás en la carpeta principal.
- Ejecuta Get-ChildItem y verifica que aparezca src.

ERROR: Could not import module "src.api_e2e"

    Test-Path .\src\api_e2e.py

Debe devolver True. Si devuelve False, actualiza o descarga nuevamente el repositorio.

ERROR: No module named uvicorn

    python -m pip install -r requirements.txt

ERROR: Swagger solo muestra tres endpoints
1. Detén el servidor con Ctrl + C.
2. Ejecuta:

    python -m uvicorn src.api_e2e:app --reload

3. En el navegador presiona Ctrl + F5.

ERROR: El puerto 8000 está ocupado

    python -m uvicorn src.api_e2e:app --reload --port 8001

Después abre:

    http://127.0.0.1:8001/docs

ERROR: La página /docs no carga
- Verifica que PowerShell siga abierto.
- Confirma que aparezca "Uvicorn running".
- Comprueba que la URL use http y no https.

17. CIERRE DE LA PRUEBA
-----------------------
1. Detén Uvicorn con Ctrl + C.
2. Cierra PowerShell.
3. No publiques bases SQLite, cachés de geolocalización ni archivos con direcciones IP reales.
4. Conserva únicamente capturas y resultados aptos para documentación académica.
