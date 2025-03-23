import streamlit as st
import pandas as pd
import os
import base64
from enriquecedor_clinico import enriquecer_anamnesis, score_tipicidad, clasificacion_angina


st.set_page_config(page_title="BERTI - Clasificador SEC", layout="wide")
st.title("🩺 Clasificador Clínico BERTI - Angina Típica / Atípica")

# Inicializar lista acumulativa en sesión si no existe
if "casos_analizados" not in st.session_state:
    st.session_state.casos_analizados = []

texto_input = st.text_area("✍ Introduce aquí la anamnesis clínica del paciente:", height=200)

if st.button("🔍 Analizar anamnesis"):
    if texto_input.strip() != "":
        enriquecido, resumen = enriquecer_anamnesis(texto_input)
        score = score_tipicidad(resumen)
        clasificacion = clasificacion_angina(score)

        st.markdown("### ✅ Resultado del análisis clínico")
        st.markdown("**Texto enriquecido:**")
        st.code(enriquecido, language="markdown")

        st.markdown("**Score de tipicidad clínica:**")
        st.write(score)

        st.markdown("**Clasificación SEC:**")
        st.write(clasificacion)

        st.markdown("### 🧠 Variables clínicas detectadas")
        for var, val in resumen.items():
            st.markdown(f"- **{var}**: `{val}`")

        # BLOQUE: Preguntas asistidas por BERTI si hay datos ausentes relevantes
        preguntas_clave = {
            "tipo_dolor": "¿Cómo describiría el tipo de dolor? ¿Opresivo, quemante, punzante…?",
            "localizacion_dolor": "¿Dónde se localiza el dolor? ¿Precordial, retroesternal, torácico…?",
            "inicio_dolor": "¿Fue un inicio súbito o gradual?",
            "irradiacion": "¿Irradia el dolor a brazo, cuello o mandíbula?",
            "alivio_con_reposo": "¿El dolor mejora con el reposo?",
            "similitud_dolor_previo_isquemico": "¿Se parece a algún dolor previo como un IAM o problema cardíaco anterior?",
            "duracion": "¿Cuál fue la duración del episodio (minutos, horas, segundos)?",
            "disnea": "¿Presentaba disnea o dificultad respiratoria?",
            "sudoracion": "¿Hubo sudoración acompañante?",
            "vomitos": "¿Aparecieron náuseas o vómitos?",
            "palpitaciones": "¿Se acompañaba de palpitaciones?"
        }

        respuestas_usuario = {}
        faltan_datos = [var for var, valor in resumen.items() if valor == "no mencionado" and var in preguntas_clave]

        if faltan_datos:
            st.markdown("### ❓ Preguntas asistidas por BERTI para completar diagnóstico")
            st.info("Para emitir un diagnóstico más preciso, BERTI sugiere preguntar al médico clínico. Por favor, responde SI / NO / NO LO SABE")

            for var in faltan_datos:
                respuesta = st.selectbox(f"➡️ {preguntas_clave[var]}", ["NO RESPONDE", "SI", "NO", "NO LO SABE"], key=var)
                respuestas_usuario[var] = respuesta

        # Guardar caso en sesión con respuestas
        st.session_state.casos_analizados.append({
            "anamnesis": texto_input,
            "texto_enriquecido": enriquecido,
            "clasificacion_sec": clasificacion,
            "respuestas_berti": respuestas_usuario
        })
        st.success("✅ Caso guardado correctamente en la sesión.")

# Mostrar los casos acumulados
if len(st.session_state.casos_analizados) > 0:
    st.markdown("### 📊 Casos acumulados en esta sesión")
    df_casos = pd.DataFrame(st.session_state.casos_analizados)
    st.dataframe(df_casos)

    if st.button("⬇️ Exportar todos los casos a Excel"):
        df_casos.to_excel("casos_enriquecidos_BERTI.xlsx", index=False)
        st.success("✅ Archivo 'casos_enriquecidos_BERTI.xlsx' generado. Puedes descargarlo desde el entorno de ejecución.")
else:
    st.markdown("### 📊 Casos acumulados en esta sesión")
    st.info("Aún no hay casos acumulados. Analiza primero una anamnesis.")


    # Botón para exportar
if st.button("⬇️ Exportar todos los casos a Excel"):
    df_casos.to_excel("casos_enriquecidos_BERTI.xlsx", index=False)
    st.success("✅ Archivo 'casos_enriquecidos_BERTI.xlsx' generado. Puedes descargarlo desde el entorno de ejecución.")
else:
    st.markdown("### 📊 Casos acumulados en esta sesión")
    st.info("Aún no hay casos acumulados. Analiza primero una anamnesis.")
