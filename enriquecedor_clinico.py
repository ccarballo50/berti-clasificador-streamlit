import re
from enriquecedor_clinico import enriquecer_anamnesis

variables = {
"tipo_dolor": {
    "presente": [
        {"regex": r"(quemante|ardor|urente)", "valor": "ardor"},
        {"regex": r"(opresivo|presivo|pesado|compresivo)", "valor": "opresivo"},
        {"regex": r"(punzante|lancinante|lacerante)", "valor": "punzante"},
        {"regex": r"(a )?punta de dedo", "valor": "punta dedo"},
        {"regex": r"(sordo)", "valor": "sordo"}
    ],
    "ausente": []
},
"localizacion_dolor": {
    "presente": [
        {"regex": r"(precordial|centrotor[áa]cico|centro del tor[áa]x)", "valor": "precordial"},
        {"regex": r"(tor[áa]cico|t[oó]rax|pecho|zona tor[áa]cica|regi[oó]n tor[áa]cica)", "valor": "torácico"},
        {"regex": r"(dolor|molestia).*?(tor[áa]cico|pecho|t[oó]rax)", "valor": "torácico"}  # nuevo regex más clínico
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

def enriquecer_anamnesis(texto):
    resumen = {}
    texto_enriquecido = texto

    for variable, patrones in variables.items():
        valor_detectado = None

        for patron in patrones["presente"]:
            patron_regex = patron.get("regex", "")
            valor = patron.get("valor", "")

            if re.search(patron_regex, texto, flags=re.IGNORECASE):
                valor_detectado = valor
                resumen[variable] = valor_detectado
                texto_enriquecido += f" [{variable}: {valor_detectado}]"
                break

        if not valor_detectado:
            resumen[variable] = "no mencionado"

    return texto_enriquecido, resumen

def score_tipicidad(resumen):
    pesos = {
        "tipo_dolor": 2,
        "irradiacion": 2,
        "alivio_con_reposo": 1.5,
        "similitud_dolor_previo_isquemico": 1.5,
        "disnea": 1,
        "sudoracion": 1,
        "inicio_dolor": 0.5,
        "duracion": 1,
        "palpitaciones": 0.5,
        "vomitos": 0.5
    }
    score = 0
    for var, peso in pesos.items():
        if resumen.get(var) not in ["no mencionado", None]:
            score += peso
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
