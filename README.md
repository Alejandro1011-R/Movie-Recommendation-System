# Sistema de Recomendación Híbrido de Películas

## Descripción
Este proyecto desarrolla un sistema de recomendación híbrido monolítico que integra características colaborativas y de contenido para ofrecer recomendaciones personalizadas y dinámicas. Utilizando la interacción de los usuarios con las películas y los géneros de las películas como datos principales, el sistema ajusta las recomendaciones en función de las preferencias en tiempo real y el historial de visualización. La interfaz, desarrollada con Streamlit, permite a los usuarios buscar películas, calificarlas y obtener recomendaciones de manera intuitiva y efectiva.

## Equipo
- Alejandro Ramírez Trueba
- Ana Melissa Alonso Reina
- Alejandro Lamelas Delgado

## Características
- **Interfaz de usuario interactiva**: Utiliza Streamlit para una experiencia de usuario fluida y dinámica.
- **Recomendaciones personalizadas**: Adapta las recomendaciones en tiempo real basadas en la secuencia de acciones de los usuarios.
- **Adaptabilidad contextual**: Evita recomendar productos repetidos o irrelevantes.

## Origen de los Datos
Las películas utilizadas en este sistema provienen del dataset de MovieLens, proporcionado por GroupLens. Este recurso, ampliamente reconocido y utilizado en la investigación de sistemas de recomendación, incluye detalles sobre películas y calificaciones de usuarios. Puedes acceder y descargar el dataset actualizado desde [MovieLens Latest Dataset](https://grouplens.org/datasets/movielens/latest/).

## Tecnologías Utilizadas
- Streamlit para la creación de la interfaz de usuario.
- Python para el backend y la lógica del sistema de recomendación.
- Pandas para el manejo de datos.

## Instalación
Clona el repositorio y instala las dependencias:
```bash
git clone https://github.com/Alejandro1011-R/Movie-Recommendation-System.git
cd Movie-Recommendation-System
pip install -r requirements.txt
```

## Uso
Para iniciar la aplicación, ejecuta:
```bash
streamlit run front.py
```
Este script iniciará la aplicación Streamlit. Sigue las instrucciones en la interfaz para buscar películas, calificarlas y recibir recomendaciones.
