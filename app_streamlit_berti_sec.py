import streamlit as st
import pandas as pd
import os
import base64
from enriquecedor_clinico import enriquecer_anamnesis, score_tipicidad, clasificacion_angina


st.set_page_config(page_title="BERTI - Clasificador clínico", layout="wide")
st.title("🩺 Clasificación clínica asistida - BERTI")

st.markdown("""
Para la clasificación de riesgo de este paciente, se considera que las enzimas han sido normales, y que no hay alteración electrocardiográfica sugerente de isquemia aguda.
""")

if "casos_acumulados" not in st.session_state:
    st.session_state["casos_acumulados"] = []
if "respuestas_berti" not in st.session_state:
    st.session_state["respuestas_berti"] = {}

texto_input = st.text_area("Introduce la anamnesis clínica:")
if st.button("🔍 Analizar anamnesis"):
    enriquecido, resumen = enriquecer_anamnesis(texto_input)
    score = score_tipicidad(resumen)
    clasif_sec = clasificacion_angina(score)

    st.subheader("✅ Resultado del análisis clínico")
    st.markdown(f"**Texto enriquecido:**\n
{enriquecido}")
    st.markdown(f"**Score de tipicidad clínica:** {score}")
    st.markdown(f"**Clasificación SEC:** `{clasif_sec.upper()}`")

    st.subheader("🧠 Variables clínicas detectadas")
    for var, val in resumen.items():
        st.markdown(f"- **{var}**: `{val}`")

    caso = {
        "anamnesis": texto_input,
        "texto_enriquecido": enriquecido,
        "clasificacion_SEC": clasif_sec
    }
    st.session_state.casos_acumulados.append(caso)

# Mostrar preguntas asistidas después del análisis completo
if st.session_state.get("casos_acumulados"):
    st.markdown("""
---
## ❓ Preguntas asistidas por BERTI para completar diagnóstico
""")
    resumen_actual = enriquecer_anamnesis(texto_input)[1] if texto_input else {}
    preguntas = {
            "tipo_dolor": "¿Cuál es el tipo de dolor (opresivo, ardor, punzante...)?",
            "localizacion_dolor": "¿Dónde se localiza el dolor (torácico, retroesternal, precordial...)?",
            "similitud_dolor_previo_isquemico": "¿Se parece a algún dolor previo como un IAM o problema cardíaco anterior?",
            "alivio_con_reposo": "¿El dolor mejora con el reposo?",
            "disnea": "¿Presenta disnea o dificultad respiratoria?",
            "sudoracion": "¿Hubo cortejo vegetativo (náuseas, vómitos o sudoración)?",
            "vomitos": "¿Hubo cortejo vegetativo (náuseas, vómitos o sudoración)?",
            "palpitaciones": "¿Ha tenido palpitaciones?",
            "irradiacion": "¿Irradia el dolor hacia brazo, cuello, mandíbula...?",
            "duracion": "¿Cuál fue la duración del episodio (minutos, horas, segundos)?",
            "factores_riesgo": "¿Presenta factores de riesgo cardiovascular relevantes (HTA, DM, dislipemia, tabaquismo)?"
        }
    respuestas_berti = st.session_state.respuestas_berti

    with st.form("formulario_berti"):
        for var, pregunta in preguntas.items():
            if resumen_actual.get(var) in [None, "no mencionado"]:
                respuesta = st.radio(pregunta, ["No contestado", "Sí", "No", "No lo sabe"], key=var)
                respuestas_berti[var] = respuesta
        submit = st.form_submit_button("✅ Resultado BERTI")

    if submit:
        st.markdown("---")
        st.subheader("📊 Resumen de respuestas asistidas")
        for k, v in respuestas_berti.items():
            st.markdown(f"- **{k}**: `{v}`")

        st.success("Resultado BERTI generado correctamente. Puedes exportar los casos acumulados.")

        if st.button("📤 Exportar todos los casos a Excel"):
            df = pd.DataFrame(st.session_state.casos_acumulados)
            df.to_excel("output_berti_excel.xlsx", index=False)
            st.success("Archivo 'output_berti_excel.xlsx' exportado correctamente")

