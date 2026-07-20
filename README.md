# Analizador Localización de Login

Repositorio del prototipo desarrollado para el Trabajo Fin de Máster **“Analizador Localización de Login”**, orientado al análisis contextual de eventos de autenticación mediante criterios de autenticación basada en riesgo.

El proyecto combina una validación cuantitativa del motor de scoring con una demostración funcional extremo a extremo capaz de recibir eventos de login, capturar señales técnicas, obtener contexto geográfico, consultar el historial del usuario, calcular el nivel de riesgo y conservar trazabilidad del procesamiento.

## Descripción del proyecto

Este proyecto diseña, implementa y evalúa un analizador capaz de estimar el riesgo contextual de un evento de inicio de sesión a partir de la combinación de señales como:

- localización aproximada del acceso;
- dirección IP observada;
- contexto y tipo de red, cuando están disponibles;
- user agent y entorno técnico del cliente;
- historial reciente del usuario;
- variables temporales;
- distancia respecto al acceso anterior;
- velocidad de desplazamiento estimada;
- reputación de IP;
- uso de proxy, VPN, Tor o servicios de hosting;
- cambio de país o región;
- desajuste de zona horaria.

La idea central del trabajo es que un login puede ser técnicamente válido desde el punto de vista de usuario y contraseña, pero continuar siendo sospechoso cuando su contexto geográfico, técnico o temporal no resulta coherente con el comportamiento previamente observado.

El repositorio conserva dos líneas complementarias de trabajo:

- **Validación cuantitativa v4:** utiliza un dataset sintético de 1.000 eventos de login y 24 campos contextuales y experimentales previamente estructurados. Esta versión genera métricas, tablas, matriz de confusión, histogramas, mapas de calor y demás figuras empleadas para evaluar el comportamiento del motor de scoring.

- **Pipeline funcional v5:** incorpora un flujo extremo a extremo que recibe un evento mínimo mediante una petición HTTP, captura señales observables de la solicitud, obtiene una localización aproximada, consulta el historial reciente del usuario, deriva variables contextuales, aplica el motor de scoring y persiste el resultado en SQLite.

La validación v4 y el pipeline v5 tienen finalidades diferentes. La exactitud global del **93,40 %** corresponde exclusivamente a la evaluación cuantitativa del motor sobre el dataset sintético v4. La versión v5 demuestra la viabilidad funcional del flujo completo, pero no representa una medición estadística integral de la precisión de la geolocalización o del sistema en un entorno productivo.

## Objetivo

Diseñar, implementar y evaluar una propuesta de análisis contextual de eventos de inicio de sesión que permita mejorar la identificación temprana de accesos anómalos o potencialmente fraudulentos.

La solución combina señales geográficas, técnicas, temporales e históricas mediante una lógica interpretable de scoring, capaz de generar un nivel de riesgo, una acción recomendada y las razones que justifican la clasificación.

El objetivo académico no consiste en desarrollar una plataforma preparada para producción, sino en demostrar la viabilidad técnica de un prototipo funcional, documentado, trazable y reproducible.

## Enfoque metodológico

El trabajo se desarrolló siguiendo un enfoque de **Design Science Research (DSR)**, orientado a construir y evaluar un artefacto tecnológico capaz de responder al problema planteado.

Las fases aplicadas fueron:

1. identificar el problema y justificar su relevancia;
2. definir los objetivos, preguntas de investigación y requisitos;
3. diseñar la arquitectura y el flujo funcional del artefacto;
4. construir el prototipo y el motor de scoring;
5. demostrar y evaluar el sistema en un entorno controlado;
6. analizar y comunicar los resultados, limitaciones y líneas de evolución.

La validación cuantitativa del motor se realizó mediante el dataset sintético v4, mientras que la demostración funcional extremo a extremo se desarrolló mediante el pipeline v5.

## Componentes principales del repositorio

Este repositorio incluye los principales artefactos técnicos utilizados para el desarrollo, demostración y validación del prototipo:

- **API REST desarrollada con FastAPI**, que expone los siguientes endpoints:
  - `GET /`, para verificar la disponibilidad del servicio;
  - `POST /login-event`, para analizar eventos previamente enriquecidos;
  - `POST /login-event/raw`, para ejecutar el pipeline funcional v5 a partir de un evento mínimo;
  - `GET /events/recent`, para consultar eventos procesados y verificar su trazabilidad.

- **Pipeline funcional v5**, encargado de coordinar la captura de señales HTTP, el enriquecimiento geográfico, la consulta del historial, la derivación de variables contextuales, el scoring y la persistencia.
- **Módulo de captura**, utilizado para obtener la dirección IP observada, el user agent, el timestamp y otras señales disponibles en la petición.
- **Módulo de enriquecimiento geográfico**, utilizado para obtener una localización aproximada y otros datos contextuales asociados a la IP.
- **Módulo de historial contextual**, encargado de recuperar eventos anteriores y calcular señales como distancia, tiempo transcurrido, velocidad estimada, cambio de país y novedad del entorno técnico.
- **Motor de scoring contextual implementado en Python**, encargado de evaluar las señales disponibles, acumular las puntuaciones, determinar el nivel de riesgo y generar razones explicativas.
- **Módulo de persistencia en SQLite**, utilizado para almacenar eventos procesados, resultados e información necesaria para el análisis histórico.
- **Módulo batch**, empleado para procesar el dataset sintético completo y generar resultados agregados.
- **Notebook de validación v4**, utilizado para calcular métricas, generar tablas, construir la matriz de confusión y producir las figuras de evaluación cuantitativa.
- **Notebook de demostración v5**, utilizado para verificar el flujo de captura, enriquecimiento, historial, scoring, respuesta y persistencia.
- **Dataset sintético v4**, compuesto por 1.000 eventos de autenticación y 24 campos contextuales y experimentales.
- **Resultados, tablas, métricas, figuras y evidencias**, generados durante la validación y la demostración funcional.
- **Guías de ejecución**, que explican cómo iniciar la API en PowerShell y cómo probarla desde Edge o Chrome.

**Ejecución recomendada de la versión v5**

La aplicación funcional debe iniciarse desde la carpeta principal del repositorio mediante:

python -m uvicorn src.api_e2e:app --reload
Una vez iniciado el servidor, la documentación interactiva estará disponible en: http://127.0.0.1:8000/docs

Para instrucciones detalladas, consulta:

- Guía de ejecución en PowerShell
- Guía de uso en Edge o Chrome

La versión v5 debe ejecutarse mediante src.api_e2e:app, ya que este módulo incorpora el endpoint /login-event/raw.

## Estructura del repositorio

```text
analizador_localizacion_login/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── schemas.py
│   ├── risk_engine.py
│   ├── storage.py
│   ├── api_login_analyzer.py
│   ├── batch_analysis.py
│   ├── capture.py
│   ├── enrichment.py
│   ├── geo_cache.py
│   ├── history.py
│   ├── pipeline.py
│   └── api_e2e.py
│
├── data/
│   └── logins_sinteticos_v4_analizador_localizacion_login.csv
│
├── notebooks/
│   ├── analizador_localizacion_login_v4_tfm.ipynb
│   └── capa_captura.ipynb
│
├── outputs/
│   ├── resultados_detallados_v4.csv
│   ├── resultados_analizador_localizacion_login_v4.xlsx
│   ├── tabla_metricas_v4.csv
│   ├── tabla_riesgo_v4.csv
│   ├── tabla_acciones_v4.csv
│   ├── tabla_comparacion_v4.csv
│   ├── matriz_confusion_v4.csv
│   ├── tabla_escenario_vs_riesgo_v4.csv
│   ├── tabla_heatmap_escenario_riesgo_v4.csv
│   └── tabla_analisis_umbrales_v4.csv
│
├── figures/
│   ├── ilustracion_5_distribucion_riesgo_v4.png
│   ├── ilustracion_6_riesgo_por_escenario_v4.png
│   ├── ilustracion_7_comparacion_esperado_obtenido_v4.png
│   ├── ilustracion_8_matriz_confusion_v4.png
│   ├── ilustracion_9_heatmap_escenario_riesgo_v4.png
│   ├── ilustracion_10_histograma_score_riesgo_v4.png
│   ├── ilustracion_11_comparacion_umbrales_scoring_v4.png
│   └── ilustracion_12_ablacion_localizacion_v4.png
│
└── docs/
    ├── README_EJECUCION_POWERSHELL.txt
    ├── README_USO_EDGE_CHROME_API.txt
    ├── ejemplo_evento_login.json
    ├── ejemplo_respuesta_analizador.json
    ├── evidencia_api_swagger.png
    ├── evidencia_respuesta_riesgo_alto.png
    ├── evidencia_events_recent.png
    └── evidencia_servidor_uvicorn_powershell.png
