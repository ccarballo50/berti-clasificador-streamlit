
# Clasificador BERTI - Dolor torácico clínico

Aplicación Streamlit para análisis clínico del dolor torácico mediante dos enfoques complementarios:

## 1️⃣ Clasificador BERTI (modelo NLP basado en ClinicalBERT)
- Carga el modelo fine-tuned desde HuggingFace.
- Clasifica anamnesis como TIPICO o ATIPICO.
- Ideal para análisis NLP avanzado con miles de casos.

### Repositorio modelo HuggingFace
https://huggingface.co/ccarballo50/berti-clasificador-clinico

### Archivos necesarios
- app_streamlit_bert.py
- requirements.txt

---

## 2️⃣ Clasificador SEC (por lógica clínica programable)
- Clasifica la anamnesis en **angina típica / atípica / no anginosa**, según criterios clínicos de la Sociedad Española de Cardiología.
- Basado en puntuación automática de variables clínicas.
- No requiere modelo BERT ni conexión a internet externa.

### Archivos necesarios
- app_streamlit_berti_sec.py
- enriquecedor_clinico_extendido.py

---

## Instrucciones de despliegue en Streamlit Cloud
1. Sube todos los archivos a un nuevo repositorio GitHub.
2. Ve a https://streamlit.io/cloud y despliega tu app.
3. Parámetros:
   - Repositorio: `usuario/repo`
   - Rama: `main`
   - Archivo principal: elegir:
     - `app_streamlit_bert.py` (modo BERTI)
     - `app_streamlit_berti_sec.py` (modo SEC)
