import streamlit as st
import language_tool_python
from openai import OpenAI
import re

# 🔐 PON TU API KEY AQUÍ
client = OpenAI(api_key=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)

tool = language_tool_python.LanguageTool('es')

# ----------------------------
# FUNCIONES
# ----------------------------

def revisar_ortografia(texto):
    errores = tool.check(texto)
    return len(errores)

def evaluar_con_ia(texto):
    prompt = f"""
Evalúa el siguiente ensayo universitario con escala de 0 a 10 en cada criterio.

Criterios:
Contenido
Argumentación
Estructura
Referencias

Devuelve SOLO en este formato exacto:

Contenido: X
Argumentación: X
Estructura: X
Referencias: X

Texto:
{texto}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


def extraer_numeros(texto_resultado):
    numeros = re.findall(r"\d+", texto_resultado)
    if len(numeros) >= 4:
        return list(map(int, numeros[:4]))
    else:
        return [7,7,7,7]  # fallback seguro


def calcular_nota(contenido, argumentacion, estructura, referencias, ortografia):
    nota = (
        contenido * 0.30 +
        argumentacion * 0.25 +
        estructura * 0.20 +
        referencias * 0.10 +
        ortografia * 0.15
    )
    return round(nota, 2)


def feedback_por_criterio(valor, criterio):
    if valor >= 9:
        return f"Excelente nivel en {criterio}."
    elif valor >= 8:
        return f"Buen desempeño en {criterio}, puede mejorar ligeramente."
    elif valor >= 7:
        return f"Nivel aceptable en {criterio}, pero necesita mayor profundidad."
    else:
        return f"Debe reforzar significativamente {criterio}."


# ----------------------------
# INTERFAZ
# ----------------------------

st.title("📚 Sistema Inteligente de Evaluación Universitaria")

texto = st.text_area("Pega aquí el ensayo del alumno", height=300)

if st.button("Evaluar Ensayo"):

    if texto.strip() == "":
        st.warning("Debes pegar un texto.")
    else:
        st.subheader("🔎 Revisión Ortográfica")
        errores = revisar_ortografia(texto)
        st.write(f"Errores detectados: {errores}")

        if errores <= 3:
            nota_ortografia = 10
        elif errores <= 6:
            nota_ortografia = 8
        elif errores <= 10:
            nota_ortografia = 7
        else:
            nota_ortografia = 6

        st.write(f"Nota Ortografía: {nota_ortografia}")

        st.subheader("🧠 Evaluación IA")
        resultado_ia = evaluar_con_ia(texto)
        st.text(resultado_ia)

        contenido, argumentacion, estructura, referencias = extraer_numeros(resultado_ia)

        st.subheader("📊 Cálculo Final")

        nota_final = calcular_nota(
            contenido,
            argumentacion,
            estructura,
            referencias,
            nota_ortografia
        )

        st.write(f"### 🎓 Nota Final: {nota_final}")

        st.subheader("📝 Retroalimentación")

        st.write(feedback_por_criterio(contenido, "Contenido"))
        st.write(feedback_por_criterio(argumentacion, "Argumentación"))
        st.write(feedback_por_criterio(estructura, "Estructura"))
        st.write(feedback_por_criterio(referencias, "Referencias"))
        st.write(feedback_por_criterio(nota_ortografia, "Ortografía"))

        if nota_final >= 9:
            st.success("Desempeño sobresaliente.")
        elif nota_final >= 8:
            st.info("Buen trabajo general.")
        elif nota_final >= 7:
            st.warning("Trabajo aceptable, con áreas de mejora.")
        else:
            st.error("Trabajo insuficiente según rúbrica.")
