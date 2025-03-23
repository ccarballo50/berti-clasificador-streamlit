import streamlit as st
import pandas as pd
import os
import base64
from enriquecedor_clinico import enriquecer_anamnesis, score_tipicidad, clasificacion_angina

st.set_page_config(page_title="Clasificación de Angina - BERTI SEC", layout="centered")
st.title("🩺 Clasificación clínica de angina - Modo acumulativo")

st.markdown("""
Esta app permite analizar múltiples anamnesis clínicas, revisar los resultados y exportar todos los casos en bloque a un Excel.
""")

# Inicializar lista acumulativa en la sesión
if "casos_acumulados" not in st.session_state:
    st.session_state.casos_acumulados = []

# Entrada de nueva anamnesis
texto_input = st.text_area("Introduce una anamnesis clínica:", height=200)

if st.button("➕ Añadir caso a la sesión"):
    if texto_input.strip() == "":
        st.warning("Por favor, escribe una anamnesis.")
    else:
        enriquecido, resumen = enriquecer_anamnesis(texto_input)
        score = score_tipicidad(resumen)
        tipo = clasificacion_angina(score)

        fila = {
            "anamnesis": texto_input,
            "texto_enriquecido": enriquecido,
            "score": score,
            "clasificacion_sec": tipo
        }
        fila.update(resumen)

        st.session_state.casos_acumulados.append(fila)
        st.success("✅ Caso añadido correctamente a la sesión.")
        st.markdown("Puedes seguir introduciendo más anamnesis o exportar todo al final.")

# Mostrar tabla acumulada
st.markdown("---")
st.subheader("📊 Casos acumulados en esta sesión")

if len(st.session_state.casos_acumulados) > 0:
    df = pd.DataFrame(st.session_state.casos_acumulados)
    st.dataframe(df)

    # Exportar Excel
    nombre_archivo = "feedback_berti_sesion.xlsx"
    df.to_excel(nombre_archivo, index=False)

    # Botón de descarga
    with open(nombre_archivo, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{nombre_archivo}">📥 Descargar Excel de esta sesión</a>'
    st.markdown(href, unsafe_allow_html=True)
else:
    st.info("Aún no se ha añadido ningún caso en esta sesión.")
