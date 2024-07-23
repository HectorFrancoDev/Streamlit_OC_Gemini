import os
import shutil
import streamlit as st
from PyPDF2 import PdfReader
from convert_pdf_to_img import pdf_to_images
from gemini_model import gemini_output_TR, model
# from paligemma_model import start
# start()


files_folder = 'files'
output_folder = 'output_images'

# Título de la aplicación
# st.logo('logo-davivienda.png', link="https://daviviendateam.streamlit.app", icon_image='logo-davivienda.png')
st.image('logo-davivienda.png', caption='Banco Davivienda')
st.title('Reto OCR Asobancaria... ')

# Descripción
st.write('Equipo Banco Davivienda - Reto OCR Auditores Asobancaria')

# Haz el prompt en español
prompt = st.text_input('Construye tu Prompt')

# Carga de un documento
documento = st.file_uploader('Cargar un archivo', type=['pdf'])

if len(prompt) > 10 and documento is not None:
    archivo_pdf = documento.read()
    os.mkdir(files_folder)
    
    pdf_name = documento.name
    # Guardar el archivo PDF en el sistema de archivos local (opcional)
    with open(f'files/{pdf_name}', 'wb') as f:
        f.write(archivo_pdf)
        
    pdf_to_images(f'files/{pdf_name}', output_folder, 'png')
    
    english_prompt = gemini_output_TR(prompt)
    
    st.write(model(english_prompt))
    shutil.rmtree(files_folder)
    shutil.rmtree(output_folder)

    
    
    
