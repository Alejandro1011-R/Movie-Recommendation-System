#!/bin/bash

# Detiene la ejecución si ocurre un error
set -e

# Activar el entorno virtual si es necesario (descomenta la siguiente línea si tienes un entorno virtual)
# source /path/to/your/venv/bin/activate

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt

# Ejecutar la aplicación Streamlit
echo "Iniciando la aplicación Streamlit..."
streamlit run front.py

