README - EJECUCIÓN DEL ANALIZADOR LOCALIZACIÓN DE LOGIN EN POWERSHELL
======================================================================

Proyecto: Analizador Localización de Login
Versión recomendada: v4
Entorno: Windows + PowerShell + Python + FastAPI/Uvicorn

1. Requisitos previos
---------------------
Antes de ejecutar el prototipo, confirma que tienes instalado:

- Python 3.10 o superior.
- Git, si vas a clonar el repositorio desde GitHub.
- Microsoft Edge o Google Chrome para abrir la documentación de la API.
- Conexión a Internet para instalar dependencias la primera vez.

Para comprobar Python, abre PowerShell y ejecuta:

    python --version

Si Windows no reconoce el comando, prueba:

    py --version

Si ninguno funciona, instala Python desde la web oficial y marca la opción "Add Python to PATH" durante la instalación.

2. Descargar o ubicar el proyecto
---------------------------------
Opción A: si descargaste el repositorio como ZIP desde GitHub:

1. Descomprime el archivo ZIP.
2. Entra a la carpeta principal del proyecto.
3. Verifica que existan estas carpetas y archivos:

    src/
    data/
    docs/
    figures/
    notebooks/
    outputs/
    README.md
    requirements.txt

Opción B: si vas a clonar el repositorio con Git:

    git clone https://github.com/dibujoudea-boop/analizador_localizacion_login.git
    cd analizador_localizacion_login

3. Abrir PowerShell en la carpeta del proyecto
----------------------------------------------
En el Explorador de archivos de Windows:

1. Abre la carpeta principal del proyecto.
2. Haz clic en la barra de dirección.
3. Escribe:

    powershell

4. Presiona Enter.

También puedes abrir PowerShell manualmente y moverte a la carpeta con un comando similar a este:

    cd C:\TFM\analizador_localizacion_login\analizador_localizacion_login-main

Ajusta la ruta según la ubicación real de tu carpeta.

4. Crear el entorno virtual
---------------------------
Dentro de la carpeta principal del proyecto, ejecuta:

    python -m venv .venv

Si usas el lanzador de Python en Windows, también puedes ejecutar:

    py -m venv .venv

Este comando crea una carpeta llamada .venv con el entorno virtual del proyecto.

5. Activar el entorno virtual
-----------------------------
Primero intenta activar el entorno con:

    .venv\Scripts\activate

Si se activa correctamente, verás algo parecido a esto al inicio de la línea:

    (.venv) PS C:\...

6. Corrección del error de política de ejecución en PowerShell
-------------------------------------------------------------
Si aparece un error similar a este:

    No se puede cargar el archivo .venv\Scripts\Activate.ps1
    porque la ejecución de scripts está deshabilitada en este sistema.

No es un error del proyecto. Es una restricción de seguridad de PowerShell.

Para solucionarlo solo en la sesión actual, ejecuta:

    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

Después vuelve a activar el entorno:

    .venv\Scripts\activate

Importante:
- Esta corrección solo aplica a la ventana actual de PowerShell.
- No cambia la política global del equipo.
- Si cierras PowerShell, tendrás que repetirla si vuelve a aparecer el mismo error.

7. Instalar las dependencias
----------------------------
Con el entorno virtual activado, ejecuta:

    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt

Este paso instala FastAPI, Uvicorn, Pandas, Matplotlib, OpenPyXL y las demás librerías necesarias.

Si aparece un error indicando que no existe requirements.txt, confirma que estás ubicado en la carpeta principal del proyecto.

8. Ejecutar la API
------------------
Con el entorno virtual activado y las dependencias instaladas, ejecuta:

    python -m uvicorn src.api_login_analyzer:app --reload

Si todo funciona correctamente, PowerShell mostrará mensajes similares a:

    Uvicorn running on http://127.0.0.1:8000
    Application startup complete

Esto significa que la API está funcionando localmente.

9. Abrir la API en el navegador
-------------------------------
Con PowerShell abierto y el servidor ejecutándose, abre Microsoft Edge o Google Chrome y entra a:

    http://127.0.0.1:8000/docs

Ahí verás la documentación interactiva de FastAPI con los endpoints:

    GET /
    POST /login-event
    GET /events/recent

10. Detener el servidor
-----------------------
Para detener la API, vuelve a PowerShell y presiona:

    Ctrl + C

11. Errores frecuentes y solución
---------------------------------

Error: "No se puede cargar Activate.ps1"
Solución:

    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    .venv\Scripts\activate

Error: "No module named uvicorn"
Solución:

    python -m pip install -r requirements.txt

Error: "No module named src"
Solución:
- Verifica que estás en la carpeta principal del proyecto.
- Debes ejecutar Uvicorn desde la carpeta donde existen src/, data/, docs/, figures/, notebooks/ y outputs/.

Error: la página http://127.0.0.1:8000/docs no carga
Solución:
- Verifica que PowerShell siga abierto.
- Verifica que el servidor muestre "Uvicorn running on http://127.0.0.1:8000".
- No cierres PowerShell mientras estés usando la API.
- Comprueba que la dirección esté escrita exactamente como:

    http://127.0.0.1:8000/docs

12. Comando completo recomendado para una nueva ejecución
--------------------------------------------------------
Cuando el proyecto ya esté descargado y el entorno virtual creado, normalmente bastará con:

    cd C:\TFM\analizador_localizacion_login\analizador_localizacion_login-main
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    .venv\Scripts\activate
    python -m uvicorn src.api_login_analyzer:app --reload

Ajusta la ruta del comando cd según la carpeta real donde tengas el proyecto.
