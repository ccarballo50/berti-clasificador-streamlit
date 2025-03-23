
import re

def enriquecer_anamnesis(texto):
    texto = texto.lower()

variables = {
    "tipo_dolor": {
        "presente": [
            {"regex": r"(quemante|ardor|urente)", "valor": "ardor"},
            {"regex": r"(opresivo|presivo|pesado|punzante|lancinante|lacerante|molesto|sordo|picante|compresivo)", "valor": "opresivo"}
        ],
        "ausente": []
    },
    "localizacion_dolor": {
        "presente": [
            {"regex": r"(precordial)", "valor": "precordial"},
            {"regex": r"(tor[áa]cico|t[oó]rax|pecho|zona tor[áa]cica|regi[oó]n tor[áa]cica|zona tor[áa]cica)", "valor": "torácico"}
        ],
        "ausente": []
    },
    "alivio_con_reposo": {
        "presente": [
            {"regex": r"(mejora)", "valor": "mejora"},
            {"regex": r"(cede|remite|desaparece)", "valor": "cede"}
        ],
        "ausente": []
    },
    "similitud_dolor_previo_isquemico": {
        "presente": [
            {"regex": r"(similar|parecido|comparable|recordando|recuerda|ya conocido).*?(infarto|IAM|isquemia|dolor previo|dolor anterior|problema cardiaco)", "valor": "similar a isquémico previo"}
        ],
        "ausente": []
    },
    "inicio_dolor": {
        "presente": [
            {"regex": r"(s[uú]bito|brusco)", "valor": "súbito"},
            {"regex": r"(gradual|lento)", "valor": "gradual"}
        ],
        "ausente": []
    },
    "disnea": {
        "presente": [
            {"regex": r"(disnea|falta de aire|ahogo|asfixia|dificultad respiratoria|dificultad para respirar|no puede respirar)", "valor": "disnea"}
        ],
        "ausente": []
    },
    "sudoracion": {
        "presente": [
            {"regex": r"(sudoraci[oó]n|sudor fr[ií]o|sudoraci[oó]n profusa|empapado en sudor|está sudando)", "valor": "sudoracion"}
        ],
        "ausente": []
    },
    "vomitos": {
        "presente": [
            {"regex": r"(v[oó]mitos?|n[aá]useas?|g[aá]strico|reflujo)", "valor": "vomitos"}
        ],
        "ausente": []
    },
    "palpitaciones": {
        "presente": [
            {"regex": r"(palpitaciones|latidos|latido acelerado|sensaci[oó]n de latido)", "valor": "palpitaciones"}
        ],
        "ausente": []
    },
    "irradiacion": {
        "presente": [
            {"regex": r"(brazo)", "valor": "brazo"},
            {"regex": r"(mand[ií]bula)", "valor": "mandíbula"},
            {"regex": r"(cuello)", "valor": "cuello"},
            {"regex": r"(espalda|hombro)", "valor": "espalda"}
        ],
        "ausente": []
    },
    "duracion": {
        "presente": [
            {"regex": r"(\\d+\\s*(min|minutos|h|horas))", "valor": "duracion_detectada"}
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
