
import streamlit as st
from enriquecedor_clinico_extendido import enriquecer_anamnesis, score_tipicidad, clasificacion_angina

st.set_page_config(page_title="Clasificación de Angina - BERTI SEC", layout="centered")
st.title("🩺 Clasificación clínica de angina según la SEC")
st.markdown("""
Esta app utiliza lógica clínica programable para analizar anamnesis y clasificar el tipo de angina según los criterios de la Sociedad Española de Cardiología (SEC).
""")

texto_input = st.text_area("Introduce la anamnesis clínica del paciente:", height=200)

if st.button("Analizar anamnesis"):
    if texto_input.strip() == "":
        st.warning("Por favor, introduce una anamnesis.")
    else:
        enriquecido, resumen = enriquecer_anamnesis(texto_input)
        score = score_tipicidad(resumen)
        tipo = clasificacion_angina(score)

        st.subheader("✅ Resultado del análisis clínico")
        st.markdown(f"**Texto enriquecido:**\n\n```{enriquecido}```")
        st.markdown(f"**Score de tipicidad clínica:** `{score}`")
        st.markdown(f"**Clasificación SEC:** `Angina {tipo.upper()}`")

        st.markdown("---")
        st.subheader("🧠 Variables clínicas detectadas")
        for var, val in resumen.items():
            st.markdown(f"- **{var}**: `{val}`")
