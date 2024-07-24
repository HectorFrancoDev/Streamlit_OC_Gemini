# Importar OS
import os

from dotenv import load_dotenv

# Importa la clase time
import time

# Gemini SDK
import google.generativeai as genai


# Path Library
from pathlib import Path
import mimetypes

from googletrans import Translator
translator = Translator()


load_dotenv()  # take environment variables from .env.

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key = GEMINI_API_KEY)

MODEL_CONFIG = {
    "temperature": 0.2,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096
}

SAFETY_SETTINGS = [
    {
        "category": "HARM_CATEGORY_DANGEROUS",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]


# Modelo de Traducción de Español a Inglés
model_TR = genai.GenerativeModel(model_name = 'gemini-pro',
                                 generation_config = MODEL_CONFIG,
                                 safety_settings = SAFETY_SETTINGS )

# Modelo de Optical Character Recognition (OCR)
model_OCR = genai.GenerativeModel(model_name='gemini-1.5-flash',
                                  generation_config = MODEL_CONFIG,
                                  safety_settings = SAFETY_SETTINGS)

system_prompt_TR = """
                You are a real-time language translator.
                Your task is to translate the input text from Spanish language to English language.
                Please refrain from adding any words or sentences after you
                finish the translation, your role is to translate only, please don't complete any sentence or word.
                """

system_prompt_OCR = """
               You're a virtual asistent that works for the Auditor Interal Vice Presidency of Davivienda Bank in Colombia.
               You are a specialist in comprehending structured data from receipts, tables and column/rows data.
               Input images in the form of receipts, tables and column/rows will be provided to you.
               Your task is to answer the questions I ask you based on the content of the input image.
               """

def open_image(image_path):
    '''
    Procesa y retorna la data de una imagen PNG ingresada.
    '''
    img = Path(image_path)

    if not img.exists():
        raise FileNotFoundError(f"No se pudo encontrar la imagen: {img}")

    # Validar que el archivo sea de tipo PNG
    mime_type, _ = mimetypes.guess_type(img)
    if mime_type != "image/png":
        raise ValueError(f"El archivo no es un PNG válido: {img}")

    # Leer los bytes de la imagen
    image_parts = [{
       "mime_type": mime_type,
       "data": img.read_bytes()
    }]

    return image_parts

def gemini_output_TR(user_prompt):
    '''
    Realiza la traducción de Español a Inglés
    '''
    input_prompt = [system_prompt_TR, user_prompt]
    response = model_TR.generate_content(input_prompt)
    return response.text


def gemini_output_OCR(image_path, user_prompt):
    '''
    Realiza la salida del procesamiento de OCR de las imagenes ingresadas
    '''
    image_info = open_image(image_path)
    input_prompt = [system_prompt_OCR , image_info[0], user_prompt]
    response = model_OCR.generate_content(input_prompt)
    return response.text


def model(prompt):

  data_list = []
  # Recorrer
  for nombre_carpeta, _, archivos in os.walk('output_images'):
      for archivo in archivos:
          #time.sleep(0.5)
          if archivo.endswith((".jpg", ".jpeg", ".png")):  # Cambiar extensiones según sea necesario
              ruta_imagen = os.path.join(nombre_carpeta, archivo)
              data = gemini_output_OCR(ruta_imagen, prompt)
              data_list.append(data)
  
  return data_list