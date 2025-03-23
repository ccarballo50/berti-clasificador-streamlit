import re


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
        {"regex": r"(precordial|retroesternal|centrotor[áa]cico|centro del tor[áa]x)", "valor": "precordial"},
        {"regex": r"(tor[áa]cico|t[oó]rax|pecho|zona tor[áa]cica|regi[oó]n tor[áa]cica)", "valor": "torácico"},
        {"regex": r"(dolor|molestia).*?(tor[áa]cico|pecho|t[oó]rax)", "valor": "torácico"}  # nuevo regex más clínico
        {"regex": r"(zona|región)?\s?(torácica|del tórax|tórax)", "valor": "torácico"}
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
        {"regex": r"(similar|parecido|idéntico|comparable|igual|mismo).*?(infarto|IAM|isquemia|dolor anterior|episodio previo|evento previo)", "valor": "similar a isquémico previo"},
        {"regex": r"(recuerda|me recuerda|me suena|reminiscente|ya conocido|reconocido|evoca|ya vivido).*?(IAM|infarto|dolor previo|dolor anterior)", "valor": "similar a isquémico previo"},
        {"regex": r"(dolor|molestia).*?(ya ha tenido|tuvo previamente|conocido previamente|dolor antiguo|habitual|de siempre)", "valor": "similar a isquémico previo"},
        {"regex": r"(episodio).*?(ya conocido|habitual|repetido|crónico|recurrente)", "valor": "similar a isquémico previo"},
        {"regex": r"(como otras veces|como en otras ocasiones|como en anteriores ocasiones)", "valor": "similar a isquémico previo"},
        {"regex": r"(dolor previamente descrito|episodio previo de dolor|molestia habitual)", "valor": "similar a isquémico previo"},
        {"regex": r"(episodios similares previos|molestias similares previamente)", "valor": "similar a isquémico previo"},
        {"regex": r"(dolor previamente conocido|ya experimentado anteriormente|como los que presenta habitualmente)", "valor": "similar a isquémico previo"},
        {"regex": r"(dolor previamente referido|como ya presentado en otras ocasiones)", "valor": "similar a isquémico previo"},
        {"regex": r"(como ha tenido anteriormente|que ya conoce el paciente|dolor que le resulta familiar)", "valor": "similar a isquémico previo"},
        {"regex": r"(mismo tipo de dolor que el de otras veces|dolor que el paciente identifica como habitual)", "valor": "similar a isquémico previo"},
        {"regex": r"(comparable al de otros episodios previos|coincide con molestias anteriores)", "valor": "similar a isquémico previo"},
        {"regex": r"(dolor típico del paciente|el mismo patrón que episodios anteriores)", "valor": "similar a isquémico previo"},
        {"regex": r"(dolor que coincide con otras veces|que reconoce por experiencias previas)", "valor": "similar a isquémico previo"},
        {"regex": r"(dolor que el paciente relaciona con sus episodios habituales)", "valor": "similar a isquémico previo"}
        {"regex": r"(dolor).*?(cardiaco).*?(previo|anterior|pasado)", "valor": "similar a isquémico previo"}
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
        r"(duraci[oó]n\s*(aprox\.?|aproximada)?\s*(de\s*)?(>|<)?\s*\d+\s*(minutos|min|min\.|h|horas)?)",
        r"(aprox\.?|aproximadamente|alrededor de|unos|más de|menos de)\s*\d+\s*(minutos|min|min\.|h|horas)",
        r"\d+\s*(minutos|min|min\.|h|horas)\s*(de duración)?"
    ],
    "ausente": []
}
}
import re

def enriquecer_anamnesis(texto):
    texto = texto.lower()
    texto_enriquecido = texto
    resumen = {}

    for variable, patrones in variables.items():
        valor_detectado = "no mencionado"
        encontrado = False

        # Primero buscamos en los patrones "presente"
        for patron in patrones.get("presente", []):
            if isinstance(patron, dict):  # Estructura {"regex": ..., "valor": ...}
                match = re.search(patron["regex"], texto, re.IGNORECASE)
                if match:
                    valor_detectado = patron["valor"] if patron["valor"] is not None else match.group(1)
                    valor_detectado = valor_detectado.strip().lower()
                    encontrado = True
                    break
            else:  # Estructura clásica con lista simple de regex
                if re.search(patron, texto, re.IGNORECASE):
                    valor_detectado = "presente"
                    valor_detectado = valor_detectado.strip().lower()
                    encontrado = True
                    break

        # Solo si no se encontró ningún patrón presente, buscamos en los de "ausente"
        if not encontrado:
            for patron in patrones.get("ausente", []):
                if isinstance(patron, dict):
                    match = re.search(patron["regex"], texto, re.IGNORECASE)
                    if match:
                        valor_detectado = patron["valor"] if patron["valor"] is not None else match.group(1)
                        valor_detectado = valor_detectado.strip().lower()
                        encontrado = True
                        break
                else:
                    if re.search(patron, texto, re.IGNORECASE):
                        valor_detectado = "ausente"
                        valor_detectado = valor_detectado.strip().lower()
                        encontrado = True
                        break

        resumen[variable] = valor_detectado
        texto_enriquecido += f" [{variable}: {valor_detectado}]"

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
