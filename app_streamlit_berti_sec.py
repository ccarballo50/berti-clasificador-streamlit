import streamlit as st
import pandas as pd
import os
import base64
from enriquecedor_clinico import enriquecer_anamnesis, score_tipicidad, clasificacion_angina


st.set_page_config(layout="wide")
st.title("🧠 Clasificador clínico BERTI - Dolor torácico")

if "casos" not in st.session_state:
    st.session_state.casos = []
if "respuestas_clinicas" not in st.session_state:
    st.session_state.respuestas_clinicas = []

texto_input = st.text_area("Introduce la anamnesis clínica:")

if st.button("🔍 Analizar anamnesis"):
    enriquecido, resumen = enriquecer_anamnesis(texto_input)
    score = score_tipicidad(resumen)
    clasificacion = clasificacion_angina(score)

    st.markdown("### ✅ Resultado del análisis clínico")
    st.markdown("**Texto enriquecido:**")
    st.code(enriquecido)
    st.markdown(f"**Score de tipicidad clínica:** {score}")
    st.markdown(f"**Clasificación SEC:** {clasificacion.upper()}")

    st.markdown("---")
    st.markdown("### 🧠 Variables clínicas detectadas")
    for var, valor in resumen.items():
        st.markdown(f"- **{var}**: `{valor}`")

    # Generar preguntas clínicas asistidas
    st.markdown("---")
    st.markdown("### ❓ Preguntas asistidas por BERTI para completar diagnóstico")
    st.info("Para emitir un diagnóstico más preciso, BERTI sugiere preguntar al médico clínico:")

    preguntas = {
        "tipo_dolor": "¿Cuál es el tipo de dolor (opresivo, quemante, etc.)?",
        "inicio_dolor": "¿Fue un inicio súbito o gradual?",
        "disnea": "¿Presentaba disnea o dificultad respiratoria?",
        "sudoracion": "¿Hubo sudoración acompañante?",
        "vomitos": "¿Aparecieron náuseas o vómitos?",
        "duracion": "¿Cuál fue la duración del episodio (minutos, horas, segundos)?",
        "similitud_dolor_previo_isquemico": "¿Se parece a algún dolor previo como un IAM o problema cardíaco anterior?",
        "edad": "¿Qué edad tiene el paciente?",
        "fc": "¿Cuál es la frecuencia cardíaca del paciente?",
        "ta": "¿Cuál es la presión arterial sistólica?",
        "creatinina": "¿Cuál es el valor de creatinina del paciente?",
        "killip": "¿Clase Killip del paciente?",
        "ecg_anormal": "¿El ECG muestra alteraciones significativas? (Actualmente asumido como normal)",
        "enzimas": "¿Las enzimas cardíacas están elevadas? (Actualmente asumido como normales)",
        "episodio_angina_prev": "¿Tuvo episodios de angina previos?",
        "riesgo_factores": "¿Presenta factores de riesgo cardiovascular relevantes?"
    }

    respuestas_usuario = {}
    for clave, pregunta in preguntas.items():
        if clave in resumen and resumen[clave] not in ["no mencionado", ""]:
            continue  # No preguntar si ya tenemos respuesta
        respuesta = st.radio(pregunta, ["No contestado", "Sí", "No"], key=f"respuesta_{clave}")
        respuestas_usuario[clave] = respuesta

    if st.button("📊 Resultado BERTI completo"):
        st.markdown("---")
        st.subheader("📌 Resumen final de clasificación")
        st.markdown(f"**SEC:** {clasificacion.upper()}")
        st.markdown("**TIMI Score:** (Cálculo estimado próximamente)")
        st.markdown("**GRACE Score:** (Cálculo estimado próximamente)")

        st.session_state.casos.append({
            "anamnesis": texto_input,
            "texto_enriquecido": enriquecido,
            "score_tipicidad": score,
            "clasificacion_SEC": clasificacion,
            **resumen,
            **respuestas_usuario
        })

    st.markdown("---")
    st.subheader("📈 Casos acumulados en esta sesión")
    if len(st.session_state.casos) == 0:
        st.info("Aún no hay casos acumulados. Analiza primero una anamnesis.")
    else:
        df = pd.DataFrame(st.session_state.casos)
        st.dataframe(df)

        if st.button("📥 Exportar todos los casos a Excel"):
            df.to_excel("output_feedback_clinico.xlsx", index=False)
            st.success("Casos exportados correctamente como output_feedback_clinico.xlsx")

