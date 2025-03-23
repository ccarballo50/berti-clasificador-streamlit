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

# Inicializar lista acumulativa en sesión
if "casos_acumulados" not in st.session_state:
    st.session_state.casos_acumulados = []

# Entrada libre del texto clínico
texto_input = st.text_area("Introduce la anamnesis clínica del paciente:", height=200)

if st.button("🔍 Analizar anamnesis"):
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
        st.subheader("🧠 Variables clínicas detectadas (valores extraídos)")
        for var, val in resumen.items():
            st.markdown(f"- **{var}**: `{val}`")

        st.markdown("---")
        st.markdown("### 🧪 Debug del resumen (valores completos capturados)")
        st.code(resumen, language='json')

        # Botón para acumular este caso
        if st.button("➕ Guardar este caso en la sesión acumulativa"):
            fila = {
                "anamnesis": texto_input,
                "texto_enriquecido": enriquecido,
                "score": score,
                "clasificacion_sec": tipo
            }
            fila.update(resumen)
            st.session_state.casos_acumulados.append(fila)
            st.success("✅ Caso guardado en la lista acumulada.")

# Mostrar los casos acumulados en sesión
st.markdown("---")
st.subheader("📊 Casos acumulados en esta sesión")

if len(st.session_state.casos_acumulados) > 0:
    df = pd.DataFrame(st.session_state.casos_acumulados)
    st.dataframe(df)

    # Botón para exportar todos los casos acumulados
    if st.button("📥 Exportar Excel de todos los casos analizados"):
        nombre_archivo = "feedback_berti_acumulado.xlsx"
        df.to_excel(nombre_archivo, index=False, engine='openpyxl')

        with open(nombre_archivo, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="{nombre_archivo}">📥 Descargar Excel</a>'
        st.markdown(href, unsafe_allow_html=True)
else:
    st.info("Aún no hay casos acumulados. Analiza primero una anamnesis.")
