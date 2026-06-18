# Tapachula Visionarios AI
Proyecto participante en la Copa FutBotMX 2026, Capítulo Visión por Computadora.

## Categoría
Amateur

## Objetivo
Desarrollar un sistema básico de análisis visual para partidos de fútbol robótico, utilizando herramientas de visión por computadora para detectar elementos del juego, seguir trayectorias y generar visualizaciones comprensibles.

## Integrantes
- Miguel Angel Hernández Isofo
- Erick Rodrigo Hernandez Isofo

## Enfoque inicial
El proyecto buscará analizar videos de fútbol robótico para identificar robots, balón y zonas de actividad durante el partido.

## Tecnologías utilizadas

- Python 3.11
- OpenCV
- NumPy
- GitHub

## Estructura del proyecto

├── Videos/
├── codigo/
├── documentos/
├── imagenes/
├── resultados/
└── README.md

## Avance 1 - Detección básica de movimiento

Se desarrolló un sistema inicial capaz de:
- Leer videos mediante OpenCV.
- Detectar regiones con movimiento.
- Dibujar cuadros delimitadores.
- Generar un nuevo video con el análisis realizado.

Estado: Funcional.
Próximo objetivo: seguimiento de trayectorias y análisis de desplazamiento.

## Avance 2 - Detección y seguimiento básico del balón

Se implementó un sistema capaz de:

- Detectar el balón mediante segmentación por color.
- Calcular la posición del balón en cada fotograma.
- Dibujar su trayectoria.
- Generar un video procesado con los resultados.

Estado: Funcional.
Próximo objetivo: seguimiento de robots y análisis de trayectorias.

## Avance 3 - Tracking básico de robots

Se implementó un sistema capaz de:

- Detectar múltiples robots.
- Asignar identificadores básicos.
- Dibujar trayectorias individuales.
- Generar un video procesado con seguimiento.

Estado: Funcional.
Próximo objetivo: análisis combinado de robots y balón.

## Avance 4 - Sistema completo de análisis FutBotMX

Se integró un sistema completo de análisis visual capaz de procesar un video de fútbol robótico y generar un resultado con:

- Detección básica del balón.
- Seguimiento visual del balón.
- Detección de robots principales.
- Asignación de identificadores básicos a robots.
- Trayectorias de desplazamiento.
- Panel informativo dentro del video.
- Exportación automática del video procesado.

Archivo principal:

`código/sistema_completo.py`

Resultado generado:

`resultados/resultado_completo.mp4`

Estado: Funcional.

Próximo objetivo: generar mapa de calor y visualización de actividad.

## Avance 5 - Visualización de datos

Mapa de calor generado a partir de la posición detectada del balón durante el partido.

El mapa permite identificar zonas de mayor actividad y permanencia del balón dentro del campo.

## Resultados obtenidos

El proyecto logró implementar un sistema básico de visión por computadora para fútbol robótico capaz de:

- Detectar movimiento dentro del campo.
- Detectar y seguir el balón.
- Detectar robots y asignar identificadores básicos.
- Generar trayectorias visuales.
- Exportar videos procesados automáticamente.
- Generar mapas de calor para análisis espacial.

Los resultados fueron generados utilizando videos de prueba de fútbol robótico y almacenados en la carpeta de resultados.


## Licencia

Este proyecto se distribuye bajo la licencia MIT.


