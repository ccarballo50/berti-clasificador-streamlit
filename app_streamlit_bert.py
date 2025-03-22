
import streamlit as st
import pandas as pd
from transformers import pipeline

# -------------------------------
st.set_page_config(page_title="Clasificador BERTI", layout="wide")
st.title("🤖 Clasificador BERTI - Dolor torácico clínico")

# -------------------------------
# Cargar modelo desde HuggingFace
clf = pipeline("text-classification",
               model="ccarballo50/berti-clasificador-clinico",
               tokenizer="ccarballo50/berti-clasificador-clinico")

# -------------------------------
# Sesión para resultados
if "bert_resultado" not in st.session_state:
    st.session_state.bert_resultado = None
if "acumulado" not in st.session_state:
    st.session_state.acumulado = []

# -------------------------------
# Paso 1 - Introducir anamnesis
st.subheader("1. Introduce la anamnesis del paciente:")
text_input = st.text_area("Texto libre de anamnesis clínica", height=180)

# Paso 2 - Clasificar con BERTI
if st.button("Clasificar con BERTI"):
    if text_input.strip() != "":
        pred = clf(text_input)[0]
        st.session_state.bert_resultado = {
            "bert_clasificacion": pred["label"],
            "confianza_berti": round(pred["score"] * 100, 2),
            "anamnesis": text_input
        }
        st.success(f"✅ Resultado BERTI: **{pred['label']}** (confianza: {round(pred['score'] * 100, 2)}%)")

# Paso 3 - Mostrar resultado y pedir clasificación del médico solo si hay resultado BERTI
if st.session_state.bert_resultado:
    st.subheader("2. Clasificación del médico:")
    clasificacion_medico = st.selectbox("¿Qué considera el médico?", ["TIPICO", "ATIPICO"])

    # Paso 4 - Botón para guardar el caso completo
    if st.button("Guardar caso clínico"):
        nuevo_resultado = {
            "anamnesis": st.session_state.bert_resultado["anamnesis"],
            "bert_clasificacion": st.session_state.bert_resultado["bert_clasificacion"],
            "confianza_berti": st.session_state.bert_resultado["confianza_berti"],
            "clasificacion_medico": clasificacion_medico
        }
        st.session_state.acumulado.append(nuevo_resultado)
        st.success("✅ Caso clínico guardado correctamente.")

# Paso 5 - Tabla acumulada
if st.session_state.acumulado:
    st.subheader("📊 Casos acumulados en esta sesión:")
    df_acumulado = pd.DataFrame(st.session_state.acumulado)
    st.dataframe(df_acumulado)

    # Descarga
    csv = df_acumulado.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Descargar resultados acumulados",
                       data=csv,
                       file_name="resultados_clasificacion.csv",
                       mime="text/csv")
