from dotenv import load_dotenv
import os
import uuid
from PIL import Image
import pymupdf
import torch
from datetime import datetime
from transformers import AutoProcessor, PaliGemmaForConditionalGeneration
import pandas as pd
from tqdm import tqdm
from huggingface_hub import login

load_dotenv()  # take environment variables from .env.
HUGGING_FACE_API_KEY = os.getenv('HUGGING_FACE_API_KEY')
login(token=HUGGING_FACE_API_KEY)
# Inicializar el modelo y procesador
model_id = "google/paligemma-3b-mix-224"
dtype = torch.bfloat16
# Define si usar CUDA o CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# Inicializar el modelo y procesador
model = PaliGemmaForConditionalGeneration.from_pretrained(
    model_id,
    torch_dtype=dtype,
    device_map=device,
    revision="bfloat16",
).eval()
processor = AutoProcessor.from_pretrained(model_id)


def extract_and_convert_pages_with_keyword(pdf_path, keyword):
    """
    Extrae y convierte a imágenes las páginas de un PDF que contienen una palabra clave.

    Args:
        pdf_path (str): Ruta al archivo PDF.
        keyword (str): Palabra clave a buscar en las páginas del PDF.

    Returns:
        tuple: Ruta de la carpeta de salida con las imágenes y una lista de diccionarios con el número de página y el link de la imagen.
    """
    # Generar un nombre único para la carpeta de salida usando la fecha y hora
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(os.getcwd(), f'Pages_with_{keyword}_{timestamp}')
    os.makedirs(output_dir, exist_ok=True)  # Crear la carpeta de salida si no existe

    # Abrir el archivo PDF
    pdf_document = pymupdf.open(pdf_path)
    image_data = []

    # Recorrer todas las páginas del PDF
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text = page.get_text("text")

        # Buscar la palabra clave en el texto de la página
        if keyword.lower() in text.lower():
            # Crear una imagen JPEG de la página actual
            pix = page.get_pixmap()
            image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            # Guardar la imagen como archivo JPEG en la carpeta de salida
            output_path = os.path.join(output_dir, f'page_{page_num + 1}.jpg')
            image.save(output_path, 'JPEG')

            image_data.append({"page_number": page_num + 1, "image_path": output_path})
            print(f"Página {page_num + 1} del PDF convertida a JPEG: {output_path}")

    pdf_document.close()
    print(f"Se han encontrado y guardado las páginas que contienen la palabra clave '{keyword}' en la carpeta: {output_dir}")
    return output_dir, image_data



def process_data(pdf_path, keyword, prompt ):
    # Archivo PDF a procesar

    # Convertir el PDF a imágenes que contengan la palabra clave
    folder_converted_images, _ = extract_and_convert_pages_with_keyword(pdf_path, keyword)
    print(str(folder_converted_images))

    # Crear una lista para almacenar los resultados
    results = []

    # Bucle sobre los archivos de la carpeta 'converted_image'
    for name_file in tqdm(os.listdir(folder_converted_images), desc="Procesando imágenes"):
        route_file = os.path.join(folder_converted_images, name_file)

        # Ejecutar el prompt en cada imagen
        try:
            raw_image = Image.open(route_file)
            inputs = processor(prompt, raw_image, return_tensors="pt").to(model.device)
            output = model.generate(**inputs, max_new_tokens=20)
            result = processor.decode(output[0], skip_special_tokens=True)[len(prompt):]

            # Agregar el resultado a la lista
            results.append({"file": route_file, "Resultado": result})

            print(f'{route_file} == {result}\n')

        except Exception as e:
            print(f'No se pudo procesar {route_file}: {e}')

    # Convertir la lista de resultados a un DataFrame de Pandas
    results_df = pd.DataFrame(results)

    # Guardar el DataFrame como un archivo CSV
    results_df.to_excel("results.xlsx", index=False)

    return results_df


def prueba():
    results = []
    print('Otra mondá')
    
    route_file='/workspaces/Streamlit_OC_Gemini/Pages_with_7282_20240724_031339/page_7.jpg'
    prompt = 'Extract Dates'

    raw_image = Image.open(route_file)

    inputs = processor(prompt, raw_image, return_tensors="pt")
    output = model.generate(**inputs, max_new_tokens=20)
    result = processor.decode(output[0], skip_special_tokens=True)[len(prompt):]

    # Agregar el resultado a la lista
    results.append({"file": route_file, "Resultado": result})
    print(f'{route_file} == {result}\n')


