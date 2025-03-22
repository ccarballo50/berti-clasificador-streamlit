
import re

def enriquecer_anamnesis(texto):
    texto = texto.lower()

    variables = {
        "tipo_dolor": {
            "valores": [r"dolor (?:de tipo )?(quemante|urente|opresivo|punzante|lancinante|lacerante|molesto|pesado|presivo|sordo|picante|compresivo)"]
        },
        "localizacion_dolor": {
            "valores": [r"(retrosternal|a punta de dedo|precordial|epigastrio|costado|tor[áa]cico|pecho|infraclavicular|subesternal)"]
        },
        "alivio_con_reposo": {
            "valores": [r"(cede|mejora|desaparece).*reposo", r"(mejor[aó]).*(al|con).*reposo"]
        },
        "similitud_dolor_previo_isquemico": {
            "valores": [r"(similar|parecido|recuerda|comparable).*?(infarto|iam|isquemia|episodio previo|dolor anterior|dolor isqu[ée]mico)"]
        },
        "inicio_dolor": {
            "valores": [r"inicio (s[uú]bito|brusco|gradual|lento)", r"(comienzo|aparici[oó]n).* (s[uú]bito|brusco|gradual|lento)"]
        },
        "disnea": {
            "valores": [r"(disnea|dificultad.*respirar|falta.*aire)"]
        },
        "sudoracion": {
            "valores": [r"(sudoraci[oó]n|sudoroso)"]
        },
        "vomitos": {
            "valores": [r"(v[oó]mitos?|n[aá]useas)"]
        },
        "palpitaciones": {
            "valores": [r"(palpitaciones)"]
        },
        "irradiacion": {
            "valores": [r"(irradiado|irradiaci[oó]n|hacia.*(brazo|mand[ií]bula|cuello|espalda))"]
        },
        "duracion": {
            "valores": [r"duraci[oó]n.*?(\d+\s*(minutos|min|horas|h))", r"(\d+\s*(min|h|horas))"]
        }
    }

    resumen = {}

    for var, patrones in variables.items():
        valor_detectado = "no mencionado"
        for patron in patrones.get("valores", []):
            match = re.search(patron, texto)
            if match and match.lastindex:
                valor_detectado = match.group(1)
                break
        resumen[var] = valor_detectado

    etiquetas = " ".join([f"[{k}: {v}]" for k, v in resumen.items()])
    texto_enriquecido = texto.strip() + " " + etiquetas
    return texto_enriquecido, resumen

def score_tipicidad(resumen):
    pesos = {
        "tipo_dolor": {"opresivo": 2},
        "irradiacion": {"irradiado": 2},
        "alivio_con_reposo": {"cede": 1.5, "mejora": 1.5, "desaparece": 1.5},
        "disnea": {"disnea": 1},
        "sudoracion": {"sudoracion": 1, "sudoroso": 1},
        "duracion": {">20 min": -1},
        "similitud_dolor_previo_isquemico": {"similar": 1, "recuerda": 1, "comparable": 1},
        "inicio_dolor": {"súbito": 1, "brusco": 1}
    }
    score = 0
    for var, valores in pesos.items():
        val_detectado = resumen.get(var, "")
        if val_detectado in valores:
            score += valores[val_detectado]
    return score

def clasificacion_angina(score):
    if score >= 6:
        return "tipica"
    elif score >= 3:
        return "atipica"
    else:
        return "no anginosa"

# Ejemplo
if __name__ == "__main__":
    ejemplo = "Paciente con dolor opresivo retroesternal que cede con el reposo, similar a infarto previo, de inicio súbito. Asocia disnea y sudoración."
    enriquecido, resumen = enriquecer_anamnesis(ejemplo)
    score = score_tipicidad(resumen)
    tipo = clasificacion_angina(score)
    print("Texto enriquecido:\n", enriquecido)
    print("Resumen estructurado:\n", resumen)
    print("Score tipicidad:", score)
    print("Clasificación SEC:", tipo)
