# Hackaton Asobancaria

## Equipo Davivienda

## 1. Crear Virtual Environment (venv)
```bash
python -m venv venv
```

## 1. Activar Virtual Environment (venv)

### 1.1 Windows
```bash
./venv/Scripts/activate
```
### 1.2 Unix y Linux
```bash
source ./venv/bin/activate
```
## 2. Instalar dependencias
```bash
pip install -r requirements.txt
```
## 3. Crear archivo .env
Crear el archivo .env en la ruta ráiz del proyecto

## 4. Asignar la variable de entorno de Gemini
Crear una variable de entorno con el API key de Gemini
```js
GEMINI_API_KEY=TU_API_KEY
```
## 5. Correr la aplicación
```bash
streamlit run main.py
```