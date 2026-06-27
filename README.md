# Analizador Localización de Login

Repositorio del prototipo desarrollado para el Trabajo Fin de Máster **“Analizador Localización de Login”**, orientado al análisis contextual de eventos de autenticación mediante criterios de **autenticación basada en riesgo**.

## Descripción del proyecto

Este proyecto propone y valida un analizador capaz de estimar el riesgo contextual de un evento de inicio de sesión a partir de la combinación de señales como:

- localización aproximada del acceso,
- dirección IP,
- tipo de red,
- dispositivo,
- historial del usuario,
- variables temporales,
- velocidad de desplazamiento estimada,
- reputación de IP,
- y desajuste de zona horaria.

La idea central del trabajo es que un login puede ser técnicamente válido desde el punto de vista de usuario y contraseña, pero seguir siendo **sospechoso** si su contexto geográfico, técnico o temporal no resulta coherente con el comportamiento esperado del usuario.

## Objetivo

Diseñar y evaluar una propuesta de análisis contextual de eventos de inicio de sesión que permita mejorar la identificación temprana de accesos anómalos o potencialmente fraudulentos, manteniendo una lógica **interpretable**, **documentada** y **académicamente reproducible**.

## Enfoque metodológico

El trabajo se desarrolló siguiendo un enfoque de **Design Science Research (DSR)**, orientado a:

1. identificar el problema,
2. definir objetivos y requisitos,
3. diseñar el artefacto,
4. construir un prototipo funcional,
5. validarlo en un entorno controlado,
6. y comunicar los resultados obtenidos.

## Componentes principales del repositorio

Este repositorio incluye los principales artefactos técnicos utilizados en el desarrollo y validación del prototipo funcional:

- API funcional en FastAPI para recibir eventos de login.
- Motor de scoring contextual implementado en Python.
- Módulo de persistencia en SQLite para guardar eventos procesados y resultados.
- Módulo batch para procesar datasets sintéticos completos.
- Notebook en Google Colab para validación experimental y generación de resultados.
- Dataset sintético v4 de eventos de login para validación controlada.
- Tablas, métricas e ilustraciones generadas automáticamente.

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
│   └── batch_analysis.py
│
├── data/
│   └── logins_sinteticos_v4_analizador_localizacion_login.csv
│
├── notebooks/
│   └── analizador_localizacion_login_v4_tfm.ipynb
│
├── outputs/
│   ├── resultados_detallados_v4.csv
│   ├── resultados_analizador_localizacion_login_v4.xlsx
│   ├── tabla_metricas_v4.csv
│   └── tabla_analisis_umbrales_v4.csv
│
├── figures/
│   ├── ilustracion_5_distribucion_riesgo_v4.png
│   ├── ilustracion_6_riesgo_por_escenario_v4.png
│   ├── ilustracion_7_comparacion_esperado_obtenido_v4.png
│   ├── ilustracion_8_matriz_confusion_v4.png
│   ├── ilustracion_9_heatmap_escenario_riesgo_v4.png
│   ├── ilustracion_10_histograma_score_riesgo_v4.png
│   └── ilustracion_11_comparacion_umbrales_scoring_v4.png
│
└── docs/
    ├── ejemplo_evento_login.json
    ├── ejemplo_respuesta_analizador.json
    └── evidencia_api_funcionando.png
