# Tapachula Visionarios AI
Proyecto participante en la Copa FutBotMX 2026, Capítulo Visión por Computadora.

## Categoría
Amateur

## Objetivo
Desarrollar un sistema básico de análisis visual para partidos de fútbol robótico, utilizando herramientas de visión por computadora para detectar elementos del juego, seguir trayectorias y generar visualizaciones comprensibles.

## Enfoque inicial
El proyecto buscará analizar videos de fútbol robótico para identificar robots, balón y zonas de actividad durante el partido.

## Integrantes
- Miguel Angel Hernández Isofo
- Erick Rodrigo Hernandez Isofo

## Tecnologías utilizadas
- Python 3.11
- OpenCV
- NumPy
- GitHub

## Estructura del proyecto

 - Videos/
 - Codigo/
 - Documentos/
 - Imagenes/
 - Resultados/
 - README.md

## Arquitectura de la solución
  1.- Video FutBotMX
  2.- OpenCV
  3.- Detección de movimiento
  4.- Detección de balón
  5.- Tracking de robots
  6.- Visualización de trayectorias
  7.- Video procesado
  8.- Mapa de calor

  ## Requisitos de hardware y software
Hardware utilizado:
- Intel Core i5-10300H
- 16 GB RAM
- NVIDIA GTX 1650 Ti

Software:
- Python 3.11
- OpenCV
- NumPy
- Git

## Instalación
1. Clonar el repositorio: git clone (https://github.com/Okkotsu9/Tapachula-Visionarios-AI)
2. Crear entorno virtual: python -m venv venv
3. Activar entorno virtual: source venv/Scripts/activate
4. Instalar dependencias: pip install opencv-python numpy
5. Ejecutar el sistema principal: python sistema_completo.py

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

Los resultados fueron almacenados dentro de la carpeta de resultados.

## Licencia
Este proyecto se distribuye bajo la licencia MIT.


