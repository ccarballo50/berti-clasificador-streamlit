import streamlit as st
import pandas as pd
import os
import base64
from enriquecedor_clinico import enriquecer_anamnesis, score_tipicidad, clasificacion_angina


st.set_page_config(page_title="BERTI - Clasificador Clínico", layout="wide")
st.title("🩺 BERTI - Clasificador de Dolor Torácico")
st.markdown("Introduzca la anamnesis clínica para análisis automatizado:")

texto_input = st.text_area("✍️ Anamnesis clínica:", height=200)

if 'casos' not in st.session_state:
    st.session_state['casos'] = []

if st.button("🔍 Analizar anamnesis"):
    enriquecido, resumen = enriquecer_anamnesis(texto_input)
    score = score_tipicidad(resumen)
    clasificacion = clasificacion_angina(score)

    st.markdown("### ✅ Resultado del análisis clínico")
    st.markdown("**Texto enriquecido:**")
    st.code(enriquecido)
    st.markdown(f"**Score de tipicidad clínica:** {score}")
    st.markdown(f"**Clasificación SEC:** {clasificacion.upper()}")

    st.markdown("### 🧠 Variables clínicas detectadas")
    for var, val in resumen.items():
        st.markdown(f"- **{var}**: {val}")

    # Preguntas asistidas
    st.markdown("### ❓ Preguntas asistidas por BERTI para completar diagnóstico")
    preguntas = {
        "tipo_dolor": "¿Qué tipo de dolor presenta el paciente (opresivo, ardor, punzante...)?",
        "duracion": "¿Cuál fue la duración del episodio (minutos, horas, segundos)?",
        "inicio_dolor": "¿Fue un inicio súbito o gradual?",
        "disnea": "¿Presentaba disnea o dificultad respiratoria?",
        "sudoracion": "¿Hubo sudoración acompañante?",
        "vomitos": "¿Aparecieron náuseas o vómitos?",
        "alivio_con_reposo": "¿El dolor cedía con el reposo?",
        "relacion_con_esfuerzo": "¿El dolor se desencadenó con esfuerzo físico?",
        "similitud_dolor_previo_isquemico": "¿Se parece a algún dolor previo como un IAM o problema cardíaco anterior?",
        "grace_edad": "¿Edad del paciente?",
        "grace_fc": "¿Frecuencia cardíaca?",
        "grace_pas": "¿Presión arterial sistólica?",
        "grace_creatinina": "¿Nivel de creatinina?",
        "grace_clase_killip": "¿Clase Killip del paciente?",
        "grace_sca_elevacion": "¿Elevación del ST?",
        "grace_biomarcadores": "¿Biomarcadores positivos?",
        "timi_factores_riesgo": "¿Tiene factores de riesgo cardiovascular?",
        "timi_asa_ultimos7dias": "¿Toma de aspirina en los últimos 7 días?",
        "timi_angina_severa": "¿Ha tenido angina severa en las últimas 24h?",
        "timi_st_elevacion": "¿Alteraciones del ST actuales?",
        "timi_biomarcadores": "¿Biomarcadores positivos?"
    }

    respuestas = {}
    for clave, pregunta in preguntas.items():
        if clave not in resumen or resumen[clave] == "no mencionado":
            respuestas[clave] = st.radio(pregunta, ["NO", "SI", "NO LO SABE"], key=clave)

    # Guardar caso en sesión
    caso = {
        "anamnesis": texto_input,
        "enriquecido": enriquecido,
        "score": score,
        "clasificacion_sec": clasificacion,
        "resumen": resumen,
        "respuestas": respuestas
    }
    st.session_state['casos'].append(caso)
    st.success("✅ Caso guardado correctamente en la sesión.")

# Mostrar casos acumulados
st.markdown("### 📊 Casos acumulados en esta sesión")
if len(st.session_state['casos']) > 0:
    df = pd.DataFrame([{**c['resumen'], **{"Anamnesis": c['anamnesis'], "Texto enriquecido": c['enriquecido'], "Score": c['score'], "Clasificación SEC": c['clasificacion_sec'], **c['respuestas']}} for c in st.session_state['casos']])
    st.dataframe(df)

    # Exportar Excel
    nombre_archivo = "berticasos_output.xlsx"
    if st.button("📤 Exportar todos los casos a Excel"):
        df.to_excel(nombre_archivo, index=False)
        with open(nombre_archivo, "rb") as f:
            st.download_button("⬇️ Descargar archivo Excel", f, file_name=nombre_archivo)
else:
    st.info("Aún no hay casos acumulados. Analiza primero una anamnesis.")

