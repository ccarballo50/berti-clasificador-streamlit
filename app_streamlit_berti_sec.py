import streamlit as st
import pandas as pd
import os
import base64
from enriquecedor_clinico import enriquecer_anamnesis, score_tipicidad, clasificacion_angina


st.set_page_config(page_title="Clasificador BERTI", layout="centered")
st.title("🩺 Clasificación clínica asistida - BERTI")

st.markdown(
    """
    Para la clasificación de riesgo de este paciente, se considera que las enzimas han sido normales, y que no hay alteración electrocardiográfica sugerente de isquemia aguda.
    """
)

texto_input = st.text_area("Introduce la anamnesis clínica:")
if 'casos_acumulados' not in st.session_state:
    st.session_state.casos_acumulados = []

if st.button("🔍 Analizar anamnesis"):
    if texto_input:
        enriquecido, resumen = enriquecer_anamnesis(texto_input)
        score = score_tipicidad(resumen)
        clasificacion = clasificacion_angina(score)

        st.markdown("## ✅ Resultado del análisis clínico")
        st.markdown("**Texto enriquecido:**")
        st.code(enriquecido)
        st.markdown(f"**Score de tipicidad clínica:** {score}")
        st.markdown(f"**Clasificación SEC:** {clasificacion.upper()}")

        st.markdown("## 🧠 Variables clínicas detectadas")
        for var, valor in resumen.items():
            st.markdown(f"- **{var}**: {valor}")

        # Preguntas asistidas si faltan variables importantes
        st.markdown("## ❓ Preguntas asistidas por BERTI para completar diagnóstico")
        st.info("Para emitir un diagnóstico más preciso, BERTI sugiere preguntar al médico clínico:")

        preguntas = {
            "tipo_dolor": "¿Cuál es el tipo de dolor (opresivo, ardor, punzante...)?",
            "localizacion_dolor": "¿Dónde se localiza el dolor (pecho, precordial, epigastrio...)?",
            "similitud_dolor_previo_isquemico": "¿Se parece a algún dolor previo como un IAM o problema cardíaco anterior?",
            "disnea": "¿Presenta disnea o dificultad respiratoria?",
            "sudoracion": "¿Hubo cortejo vegetativo (náuseas, vómitos o sudoración)?",
            "duracion": "¿Cuál fue la duración del episodio (minutos, horas, segundos)?",
            "factores_riesgo": "¿Presenta factores de riesgo cardiovascular relevantes? (HTA, DM, dislipemia, tabaquismo, CI previa)"
        }

        respuestas = {}
        for var, pregunta in preguntas.items():
            if resumen.get(var) == "no mencionado":
                respuestas[var] = st.radio(pregunta, ["No contestado", "Sí", "No", "No lo sabe"], key=var)

        # Botón final para mostrar la conclusión
        if st.button("💡 Mostrar clasificación final BERTI"):
            st.markdown("### 🧾 Conclusiones clínicas finales")
            st.markdown(f"**Clasificación SEC (texto + preguntas):** {clasificacion.upper()}")
            st.markdown(f"**Score tipicidad ajustado:** {score}")
            for var, resp in respuestas.items():
                st.markdown(f"- **{var}**: {resp}")

        # Acumular caso para exportación
        caso = {
            "anamnesis": texto_input,
            "texto_enriquecido": enriquecido,
            "score": score,
            "clasificacion_sec": clasificacion,
        }
        caso.update(resumen)
        st.session_state.casos_acumulados.append(caso)

# Exportar casos acumulados
st.markdown("---")
st.markdown("## 📊 Casos acumulados en esta sesión")
if len(st.session_state.casos_acumulados) > 0:
    df_export = pd.DataFrame(st.session_state.casos_acumulados)
    st.dataframe(df_export)
    nombre_archivo = "berticasos_exportados.xlsx"
    df_export.to_excel(nombre_archivo, index=False)
    with open(nombre_archivo, "rb") as f:
        st.download_button("⬇️ Exportar todos los casos a Excel", f, file_name=nombre_archivo)
else:
    st.info("Aún no hay casos acumulados. Analiza primero una anamnesis.")

