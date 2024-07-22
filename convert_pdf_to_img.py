# Importar OS
import os

# Convert PDF to Image
from pdf2image import convert_from_path

def pdf_to_images(pdf_path, output_base_folder, image_format = 'png'):
    """
    Convert each page of the PDF to an image and save in the specified format.

    :param pdf_path: Path to the input PDF file.
    :param output_folder: Folder where the images will be saved.
    :param image_format: Format of the output images ('png' or 'jpg').
    """

    # Get the base name of the PDF file (without extension) to use in folder structure
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

    # Create the output folder structure
    output_folder = os.path.join(output_base_folder, pdf_name)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Convert PDF to a list of images
    images = convert_from_path(pdf_path)

    # Save each image in the specified format
    for i, image in enumerate(images):
        image_filename = os.path.join(output_folder, f'page_{i + 1}.{image_format}')
        image.save(image_filename, image_format.upper())
        print(f'Guardado {image_filename}')
        
