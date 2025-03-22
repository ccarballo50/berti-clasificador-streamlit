
import re

def enriquecer_anamnesis(texto):
    texto = texto.lower()

    variables = {
        "disnea": {"presente": [r"disnea", r"dificultad.*respirar", r"falta.*aire"],
                   "ausente": [r"sin disnea", r"niega disnea"]},
        "sudoracion": {"presente": [r"sudoraci[oó]n", r"sudoroso"],
                       "ausente": [r"sin sudoraci[oó]n", r"niega sudoraci[oó]n"]},
        "vomitos": {"presente": [r"v[oó]mitos?", r"náuseas"],
                    "ausente": [r"sin v[oó]mitos?", r"niega v[oó]mitos?"]},
        "palpitaciones": {"presente": [r"palpitaciones"],
                          "ausente": [r"sin palpitaciones", r"niega palpitaciones"]},
        "irradiacion": {"presente": [r"irradiado", r"irradiaci[oó]n", r"hacia.*(brazo|mandíbula|cuello|espalda)"],
                        "ausente": [r"sin irradiaci[oó]n", r"no irradiado"]},
        "duracion": {"presente": [r"duraci[oó]n.*(min|hora|h)", r"\d+\s*(min|h|horas)"],
                     "ausente": []}
    }

    resumen = {}

    for var, patrones in variables.items():
        detectado = "no mencionado"
        for patron in patrones.get("ausente", []):
            if re.search(patron, texto):
                detectado = "ausente"
                break
        else:
            for patron in patrones.get("presente", []):
                if re.search(patron, texto):
                    detectado = "presente"
                    break
        resumen[var] = detectado

    etiquetas = " ".join([f"[{k}: {v}]" for k, v in resumen.items()])
    texto_enriquecido = texto.strip() + " " + etiquetas
    return texto_enriquecido

# ✅ Ejemplo:
if __name__ == "__main__":
    ejemplo = "Paciente con dolor retroesternal irradiado a brazo izquierdo, con disnea y sudoración profusa, sin vómitos."
    print("Texto enriquecido:")
    print(enriquecer_anamnesis(ejemplo))
