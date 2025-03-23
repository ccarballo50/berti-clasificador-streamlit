
import re

def enriquecer_anamnesis(texto):
    texto = texto.lower()

variables = {
    "tipo_dolor": {
        "presente": [
            r"(?:dolor|molestia).*?(?:opresivo|presivo|pesado|quemante|urente|punzante|molesto|sordo|picante|lancinante|lacerante|compresivo)",
            r"(?:de tipo|carácter)\s*(?:opresivo|quemante|punzante|urente)"
        ],
        "ausente": []
    },
    "localizacion_dolor": {
        "presente": [
            r"(zona )?(retrosternal|precordial|epigastrio|costado|tor[áa]cico|t[oó]rax|infraclavicular|subesternal|pecho)",
            r"(dolor en|molestia en).*?(pecho|torax|regi[oó]n precordial|zona tor[áa]cica|t[oó]rax)"
        ],
        "ausente": []
    },
    "alivio_con_reposo": {
        "presente": [
            r"(cede|mejora|remite|desaparece).*?(reposo|descanso|al cesar la actividad)",
            r"(mejor[aó]) (al|con).*reposo"
        ],
        "ausente": []
    },
    "similitud_dolor_previo_isquemico": {
        "presente": [
            r"(similar|parecido|comparable|recordando).*?(infarto|IAM|isquemia|dolor previo|dolor anterior)",
            r"(recuerda|ya conocido).*?(dolor isqu[eé]mico|infarto)"
        ],
        "ausente": []
    },
    "inicio_dolor": {
        "presente": [
            r"(inicio|comienzo|aparici[oó]n).*(brusco|s[uú]bito|gradual|lento)",
            r"(dolor).*?(comienza|inicia).*(brusco|s[uú]bito|gradual|poco a poco)"
        ],
        "ausente": []
    },
    "disnea": {
        "presente": [r"disnea", r"falta.*aire", r"dificultad.*respirar", r"ahogo", r"sensaci[oó]n de asfixia"],
        "ausente": [r"sin disnea", r"niega disnea", r"no disnea"]
    },
    "sudoracion": {
        "presente": [r"sudoraci[oó]n", r"sudoroso", r"sudoraci[oó]n profusa", r"sudor fr[ií]o", r"presenta sudoraci[oó]n"],
        "ausente": [r"sin sudoraci[oó]n", r"niega sudoraci[oó]n"]
    },
    "vomitos": {
        "presente": [r"v[oó]mitos?", r"n[aá]useas?", r"g[aá]strico", r"reflujo"],
        "ausente": [r"sin v[oó]mitos?", r"niega v[oó]mitos?", r"no n[aá]useas"]
    },
    "palpitaciones": {
        "presente": [r"palpitaciones", r"sensaci[oó]n de latidos", r"latido acelerado"],
        "ausente": [r"sin palpitaciones", r"niega palpitaciones", r"no palpitaciones"]
    },
    "irradiacion": {
        "presente": [
            r"irradiado", r"irradiaci[oó]n", 
            r"(dolor|molestia).*?(brazo|mand[ií]bula|cuello|espalda|hombro)", 
            r"se extiende a.*?(brazo|mand[ií]bula|cuello|espalda)"
        ],
        "ausente": [r"sin irradiaci[oó]n", r"no irradiado", r"niega irradiaci[oó]n"]
    },
    "duracion": {
        "presente": [
            r"duraci[oó]n.*?(\d+\s*(minutos|min|h|horas))",
            r"aprox.*?(\d+\s*(min|minutos|horas|h))",
            r"menos de.*?(10\s*(min|minutos))"
        ],
        "ausente": []
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
