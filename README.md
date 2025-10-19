# Generador de Certificados SILVOPAT 2025
Descripción

Sistema automatizado para generar certificados digitales para el evento internacional SILVOPAT 2025. Genera certificados en PDF a partir de archivos Excel.

Estructura del Proyecto
generador_certificados/
├── 📁 plantillas_certificados/
│   ├── 🖼️ Plantilla Certificado_Trabajos_page-0001.jpg
│   └── 🖼️ Plantilla Certificado_participacion.jpg
├── 📁 certificados_trabajos_sin_generar/
│   └── 📊 participantes.xlsx
├── 📁 certificados_trabajos_generados/
│   └── 📄 Certificados generados (PDF)
├── 📁 certificados_participacion_sin_generar/
│   └── 📊 participantes_participacion.xlsx
├── 📁 certificados_participacion_generados/
│   └── 📄 Certificados generados (PDF)
├── 🐍 generar_certificados_trabajos.py
├── 🐍 generar_certificados_participacion.py
└── 📖 README.md

Instalación Rápida

1- Descargar el proyecto
# Opción A: Clonar repositorio
  git clone https://github.com/tu-usuario/generador-certificados-silvopat.git

# Opción B: Descargar ZIP
# ⬇️ Hacer clic en "Download ZIP" arriba

2- Instalar dependencias
  pip install Pillow pandas openpyxl

3- Configurar carpetas
  mkdir plantillas_certificados
  mkdir certificados_trabajos_sin_generar
  mkdir certificados_trabajos_generados
  mkdir certificados_participacion_sin_generar
  mkdir certificados_participacion_generados

Uso Rápido

Para Certificados de Trabajos:
  python generar_certificados_trabajos.py
  
Para Certificados de Participación:
  python generar_certificados_participacion.py

Formatos de Excel Requeridos
  Certificados de Trabajos (participantes.xlsx):
    nombre,participacion,titulo
    Ana García,conferencista,Tecnología aplicada a sistemas...
    Carlos López,presentación oral,Análisis comparativo...
  Certificados de Participación (participantes_participacion.xlsx):
    nombre,participacion
    María Rodríguez,Delegado
    Juan Pérez,Comité Organizador

