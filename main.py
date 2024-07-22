import streamlit as st
from PyPDF2 import PdfReader
from convert_pdf_to_img import pdf_to_images
from gemini_model import gemini_output_TR, model

# Título de la aplicación
st.title('Reto OCR Asobancaria... ')

# Descripción
st.write('Equipo Banco Davivienda - Reto OCR Auditores Asobancaria')

# Haz el prompt en español
prompt = st.text_input('Construye tu Prompt')

# Carga de un documento
documento = st.file_uploader('Cargar un PDF', type=['pdf'])

if documento is not None:
    archivo_pdf = documento.read()
    
    pdf_name = documento.name
    # Guardar el archivo PDF en el sistema de archivos local (opcional)
    with open(f'files/{pdf_name}', 'wb') as f:
        f.write(archivo_pdf)
        
    pdf_to_images(f'files/{pdf_name}', 'output_images', 'png')
    
    english_prompt = gemini_output_TR(prompt)
    
    model(english_prompt)
    
    
    
