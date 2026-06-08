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

Este repositorio incluye los principales artefactos técnicos utilizados en la validación del prototipo:

- **Notebook en Google Colab** para la ejecución experimental del analizador.
- **Script en Python** con la lógica de scoring y procesamiento.
- **Dataset sintético v3** de eventos de login para la validación controlada.

## Estructura del repositorio

```text
analizador_localizacion_login/
│
├── analizador_localizacion_login_v3.py
├── analizador_localizacion_login_v3_tfm.ipynb
├── logins_sinteticos_v3_analizador_localizacion_login.csv
