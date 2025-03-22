import streamlit as st
import pandas as pd
import os
from enriquecedor_clinico import enriquecer_anamnesis, score_tipicidad, clasificacion_angina

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
        st.subheader("🧠 Variables clínicas detectadas (valores extraídos)")
        for var, val in resumen.items():
            st.markdown(f"- **{var}**: `{val}`")

        st.markdown("---")
        st.markdown("### 🧪 Debug del resumen (valores completos capturados)")
        st.code(resumen, language='json')

        # 🔽 NUEVA FUNCIÓN: Guardar en Excel
        st.markdown("---")
        st.subheader("💾 Guardar resultado para análisis posterior")

        if st.button("Guardar este caso en Excel"):
            fila = {
                "anamnesis": texto_input,
                "texto_enriquecido": enriquecido,
                "score": score,
                "clasificacion_sec": tipo
            }
            for var, val in resumen.items():
                fila[var] = val

            df_nuevo = pd.DataFrame([fila])
            nombre_archivo = "feedback_berti.xlsx"

            if os.path.exists(nombre_archivo):
                df_existente = pd.read_excel(nombre_archivo)
                df_final = pd.concat([df_existente, df_nuevo], ignore_index=True)
            else:
                df_final = df_nuevo

            df_final.to_excel(nombre_archivo, index=False)
            st.success(f"Caso guardado correctamente en '{nombre_archivo}'")

