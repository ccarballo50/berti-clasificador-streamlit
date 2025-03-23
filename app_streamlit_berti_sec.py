import streamlit as st
import pandas as pd
import os
import base64
from enriquecedor_clinico import enriquecer_anamnesis, score_tipicidad, clasificacion_angina

st.set_page_config(page_title="Clasificación de Angina - BERTI SEC", layout="centered")
st.title("🩺 Clasificación clínica de angina según la SEC")

st.markdown("""
Esta app analiza anamnesis clínicas, calcula el score de tipicidad y clasificación SEC,
y además te permite acumular múltiples casos en sesión y exportarlos todos a Excel al final.
""")

# Inicializar lista acumulativa
if "casos_acumulados" not in st.session_state:
    st.session_state.casos_acumulados = []

# Entrada del texto clínico
texto_input = st.text_area("Introduce la anamnesis clínica del paciente:", height=200)

if st.button("🔍 Analizar y guardar este caso"):
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

        st.subheader("🧠 Variables clínicas detectadas")
        for var, val in resumen.items():
            st.markdown(f"- **{var}**: `{val}`")

        # Guardar directamente el caso en la lista
        fila = {
            "anamnesis": texto_input,
            "texto_enriquecido": enriquecido,
            "score": score,
            "clasificacion_sec": tipo
        }
        fila.update(resumen)
        st.session_state.casos_acumulados.append(fila)
        st.success("✅ Caso guardado correctamente en la sesión.")

# Mostrar todos los casos acumulados
st.markdown("---")
st.subheader("📊 Casos acumulados en esta sesión")

if len(st.session_state.casos_acumulados) > 0:
    df = pd.DataFrame(st.session_state.casos_acumulados)
    st.dataframe(df)

    if st.button("📥 Exportar Excel de todos los casos acumulados"):
        nombre_archivo = "feedback_berti_acumulado.xlsx"
        df.to_excel(nombre_archivo, index=False, engine='openpyxl')

        with open(nombre_archivo, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="{nombre_archivo}">📥 Descargar Excel</a>'
        st.markdown(href, unsafe_allow_html=True)
else:
    st.info("Aún no hay casos acumulados. Analiza primero una anamnesis.")
