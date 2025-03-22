
import streamlit as st
import pandas as pd
from transformers import pipeline

st.set_page_config(page_title="Clasificador BERTI", layout="wide")
st.title("🤖 Clasificador BERTI - Dolor torácico clínico")

clf = pipeline("text-classification",
               model="ccarballo50/berti-clasificador-clinico",
               tokenizer="ccarballo50/berti-clasificador-clinico")

if "bert_resultado" not in st.session_state:
    st.session_state.bert_resultado = None
if "acumulado" not in st.session_state:
    st.session_state.acumulado = []

st.subheader("1. Introduce la anamnesis del paciente:")
text_input = st.text_area("Texto libre de anamnesis clínica", height=180)

if st.button("Clasificar con BERTI"):
    if text_input.strip() != "":
        pred = clf(text_input)[0]
        st.session_state.bert_resultado = {
            "bert_clasificacion": pred["label"],
            "confianza_berti": round(pred["score"] * 100, 2),
            "anamnesis": text_input
        }
        st.success(f"✅ Resultado BERTI: **{pred['label']}** (confianza: {round(pred['score'] * 100, 2)}%)")

if st.session_state.bert_resultado:
    st.subheader("2. Clasificación del médico:")
    clasificacion_medico = st.selectbox("¿Qué considera el médico?", ["TIPICO", "ATIPICO"])

    if st.button("Guardar caso clínico"):
        nuevo_resultado = {
            "anamnesis": st.session_state.bert_resultado["anamnesis"],
            "bert_clasificacion": st.session_state.bert_resultado["bert_clasificacion"],
            "confianza_berti": st.session_state.bert_resultado["confianza_berti"],
            "clasificacion_medico": clasificacion_medico
        }
        st.session_state.acumulado.append(nuevo_resultado)
        st.success("✅ Caso clínico guardado correctamente.")

if st.session_state.acumulado:
    st.subheader("📊 Casos acumulados en esta sesión:")
    df_acumulado = pd.DataFrame(st.session_state.acumulado)
    st.dataframe(df_acumulado)

    csv = df_acumulado.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Descargar resultados acumulados",
                       data=csv,
                       file_name="resultados_clasificacion.csv",
                       mime="text/csv")
