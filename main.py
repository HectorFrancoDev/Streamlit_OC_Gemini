import os
import gc
import shutil
import streamlit as st
from PyPDF2 import PdfReader
from convert_pdf_to_img import pdf_to_images
from gemini_model import gemini_output_TR, model
from googletrans import Translator
from paligemma_model import process_data

# prueba()

files_folder = 'files'
output_folder = 'output_images'
translator = Translator()

# Título de la aplicación
st.image('logo-davivienda.png', caption='Banco Davivienda')

# Descripción
descripcion = '''
## ¡Descubre el poder de la IA generativa para tus auditorías! 

Esta herramienta te ofrece un *nuevo nivel de eficiencia* para extraer información crucial de tus documentos. Gracias a la última tecnología en IA generativa, podrás:

*1. Personalizar tu análisis:*

*Selecciona el modelo que mejor se adapte a tus necesidades:*
    * *Modelo SLM (Small Language Model):*  Extrae información precisa y estructurada como ID, cantidades, teléfonos, fechas, etc. 
      * Ejemplo:  "*Extrae todas las fechas de facturación de este PDF.*"
    * *Modelo LLM (Large Language Model):* Realiza consultas abiertas y genera resúmenes, análisis o interpretaciones. 
      * Ejemplo: "*Resume la información principal del contrato.*"

*2. Carga archivos con facilidad:*

Sube archivos PDF e imágenes directamente a la plataforma para procesar la información que necesitas.

*3. Obtén resultados rápidos y precisos:*

La IA generativa analiza tus archivos y te proporciona la información que necesitas de forma rápida y eficiente.

*¿Listo para revolucionar tus auditorías? ¡Comienza a explorar el poder de la IA generativa hoy!*
'''

st.write(descripcion)

# Opciones para el selectbox
opciones = ["Modelo SLM", "Modelo LLM"]

# Crear el selectbox
seleccion = st.selectbox("Selecciona una opción:", opciones)

# Haz el prompt en español
prompt = st.text_input('Construye tu Prompt')

# Carga de un documento
documento = st.file_uploader('Cargar un archivo', type=['pdf'])

# Haz el prompt en español
keyword = st.text_input('Busca tu palabra clave')

if seleccion == 'Modelo SLM':
    if len(prompt) > 5 and len(keyword) > 0 and documento is not None:
        

        # Traducir el prompt al inglés
        # english_prompt = translator.translate(str(prompt), src='es', dest='en')

        archivo_pdf = documento.read()
        if not os.path.exists(files_folder):
            os.makedirs(files_folder)
        pdf_name = documento.name

        # Guardar el archivo PDF en el sistema de archivos local (opcional)
        with open(f'files/{pdf_name}', 'wb') as f:
            f.write(archivo_pdf)

        result_df = process_data(f'files/{pdf_name}', str(keyword), prompt)
        st.dataframe(result_df)
        shutil.rmtree(files_folder)
        # shutil.rmtree(output_dir)
        gc.collect()


if seleccion == 'Model LLM':

    if len(prompt) > 10 and documento is not None:
        archivo_pdf = documento.read()
        os.mkdir(files_folder)
        
        pdf_name = documento.name
        # Guardar el archivo PDF en el sistema de archivos local (opcional)
        with open(f'files/{pdf_name}', 'wb') as f:
            f.write(archivo_pdf)
            
        pdf_to_images(f'files/{pdf_name}', output_folder, 'png')
        
        # english_prompt = gemini_output_TR(prompt)

        # Traducir el texto al español
        english_prompt = translator.translate(prompt, src='es', dest='en')
        
        st.write(model(english_prompt))
        shutil.rmtree(files_folder)
        shutil.rmtree(output_folder)
        gc.collect()

    
    
    
