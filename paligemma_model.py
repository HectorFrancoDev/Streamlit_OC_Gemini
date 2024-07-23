from dotenv import load_dotenv
import os
import shutil
from PIL import Image
import requests
from huggingface_hub import login
from transformers import AutoProcessor, PaliGemmaForConditionalGeneration

HUGGING_FACE_API_KEY = os.getenv('HUGGING_FACE_API_KEY')
login(token=HUGGING_FACE_API_KEY)