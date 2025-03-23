import streamlit as st
import pandas as pd
import os
import base64
from enriquecedor_clinico import enriquecer_anamnesis, score_tipicidad, clasificacion_angina


st.set_page_config(page_title="Clasificador clínico BERTI", layout="centered")
st.title("🩺 Clasificación clínica asistida - BERTI")

# Mensaje informativo
st.markdown("""
Para la clasificación de riesgo de este paciente, se considera que las enzimas han sido normales,
y que no hay alteración electrocardiográfica sugerente de isquemia aguda.
""")

# Campo para introducir texto libre
texto_input = st.text_area("Introduce aquí la anamnesis clínica del paciente:")

if 'respuestas_bert' not in st.session_state:
    st.session_state.respuestas_bert = {}
if 'casos_guardados' not in st.session_state:
    st.session_state.casos_guardados = []

if st.button("🔍 Analizar anamnesis"):
    if texto_input:
        enriquecido, resumen = enriquecer_anamnesis(texto_input)
        score = score_tipicidad(resumen)
        clasificacion_sec = clasificacion_angina(score)

        st.session_state.texto_input = texto_input
        st.session_state.enriquecido = enriquecido
        st.session_state.resumen = resumen
        st.session_state.score = score
        st.session_state.clasificacion_sec = clasificacion_sec

        st.markdown("---")
        st.markdown("### ✅ Resultado del análisis clínico")
        st.markdown(f"**Texto enriquecido:**\n\n{enriquecido}")
        st.markdown(f"**Score de tipicidad clínica:** {score}")
        st.markdown(f"**Clasificación SEC:** {clasificacion_sec.upper()}")

        # Preguntas asistidas si faltan variables
        st.markdown("---")
        st.markdown("### ❓ Preguntas asistidas por BERTI para completar diagnóstico")

        preguntas_diccionario = {
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

        for variable, pregunta in preguntas_diccionario.items():
            if resumen.get(variable) in ["no mencionado", None]:
                st.session_state.respuestas_bert.setdefault(variable, "No contestado")
                st.session_state.respuestas_bert[variable] = st.radio(
                    pregunta,
                    options=["No contestado", "Sí", "No", "No lo sabe"],
                    index=["No contestado", "Sí", "No", "No lo sabe"].index(
                        st.session_state.respuestas_bert.get(variable, "No contestado")
                    ),
                    key=f"radio_{variable}"
                )

        if st.button("✅ Ver resultado BERTI"):
            st.markdown("---")
            st.markdown("### 📌 Resultado final clínico")
            st.markdown(f"**Clasificación SEC (NLP):** {st.session_state.clasificacion_sec.upper()}")
            st.markdown(f"**Score clínico:** {st.session_state.score}")
            st.markdown("**Factores adicionales aportados por el médico:**")
            for var, resp in st.session_state.respuestas_bert.items():
                st.markdown(f"- {var.replace('_',' ').capitalize()}: {resp}")

            st.session_state.casos_guardados.append({
                "anamnesis": st.session_state.texto_input,
                "enriquecido": st.session_state.enriquecido,
                "clasificacion_SEC": st.session_state.clasificacion_sec,
                **st.session_state.respuestas_bert
            })
            st.success("✅ Caso guardado correctamente en la sesión.")

st.markdown("---")
st.markdown("### 📊 Casos acumulados en esta sesión")
if st.session_state.casos_guardados:
    df_casos = pd.DataFrame(st.session_state.casos_guardados)
    st.dataframe(df_casos)
    if st.button("💾 Exportar todos los casos a Excel"):
        df_casos.to_excel("casos_bert_sesion.xlsx", index=False)
        st.success("Archivo exportado correctamente: casos_bert_sesion.xlsx")
else:
    st.info("Aún no hay casos acumulados. Analiza primero una anamnesis.")


