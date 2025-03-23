import streamlit as st
import pandas as pd
import os
import base64
from enriquecedor_clinico import enriquecer_anamnesis, score_tipicidad, clasificacion_angina


# Inicializar sesión si no existe
if 'respuestas_clinicas' not in st.session_state:
    st.session_state.respuestas_clinicas = {}

# Encabezado
st.title("🩺 Clasificación clínica asistida - BERTI")
st.markdown("""
#### Para la clasificación de riesgo de este paciente, se considera que las enzimas han sido normales, y que no hay alteración electrocardiográfica sugerente de isquemia aguda.
""")

# Preguntas dinámicas según variables no detectadas en la anamnesis
variables_clinicas = {
    "tipo_dolor": "¿Cuál es el tipo de dolor (opresivo, ardor, punzante...)?",
    "disnea": "¿Presenta disnea o dificultad respiratoria?",
    "cortejo_vegetativo": "¿Cortejo vegetativo? (náuseas, vómitos o sudoración)",
    "palpitaciones": "¿Ha presentado palpitaciones?",
    "irradiacion": "¿El dolor irradia a alguna zona (brazo, mandíbula...)?",
    "duracion": "¿Cuál fue la duración del episodio (minutos, horas, segundos)?",
    "similitud_dolor_previo_isquemico": "¿Se parece a algún dolor previo como un IAM o problema cardíaco anterior?",
    "factores_riesgo": "¿Presenta factores de riesgo cardiovascular relevantes? (HTA, DM, dislipemia, tabaquismo, obesidad, antecedentes familiares)",
    "edad": "¿Cuál es la edad del paciente?"
}

respuestas_actuales = st.session_state.respuestas_clinicas

st.markdown("## ❓ Preguntas asistidas por BERTI para completar diagnóstico")

with st.form("formulario_clinico"):
    for var, pregunta in variables_clinicas.items():
        if var not in respuestas_actuales or respuestas_actuales[var] == "No contestado":
            respuestas_actuales[var] = st.radio(
                f"{pregunta}",
                ["No contestado", "Sí", "No", "No lo sabe"],
                index=0,
                key=f"respuesta_{var}"
            )

    submitted = st.form_submit_button("📊 Resultado BERTI completo")

if submitted:
    st.markdown("---")
    st.subheader("🧠 Resumen clínico final")
    for var, respuesta in respuestas_actuales.items():
        st.write(f"**{variables_clinicas.get(var, var)}:** {respuesta}")

# Exportar resultados a Excel
st.markdown("---")
st.subheader("📥 Exportación de resultados")
if st.button("📤 Exportar todos los casos a Excel"):
    df = pd.DataFrame.from_dict(respuestas_actuales, orient='index', columns=['Respuesta'])
    df.to_excel("output_feedback_clinico.xlsx")
    st.success("Archivo 'output_feedback_clinico.xlsx' exportado correctamente.")

