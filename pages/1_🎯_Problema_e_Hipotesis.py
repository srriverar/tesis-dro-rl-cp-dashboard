"""Página 1 · Problema, alcance, métricas e hipótesis."""
import streamlit as st

from utils import load_css
from utils.components import (
    formula_note, info_card, kpi_row, ok_box, page_header, warn_box,
)
from utils.charts import fig_timeline_decision, fig_traceability_matrix
from utils.content import ALCANCE, HIPOTESIS, METRICAS, COMPARADORES

st.set_page_config(page_title="Problema e Hipótesis · Tesis DRO+RL+CP", page_icon="🎯", layout="wide")
load_css()
page_header("🎯", "Problema, alcance e hipótesis verificables",
            "Respuesta a las observaciones de Introducción, Planteamiento y Objetivos: "
            "horizonte delimitado, incertidumbres explícitas y «calidad de decisiones» medible.")

# ---------------------------------------------------------------- árbol del problema
st.markdown("#### 🌳 Del contexto al problema, en cuatro pasos")
tabs = st.tabs(["1 · Causas", "2 · Consecuencias", "3 · Problema", "4 · Pregunta de investigación"])
with tabs[0]:
    st.markdown(
        "- La transición energética integra masivamente **solar y eólica**, cuya producción es "
        "intermitente y depende del clima.\n"
        "- La **demanda neta** (demanda − renovables) acumula la incertidumbre de tres procesos a la vez.\n"
        "- Los modelos estocásticos **asumen una distribución** de la incertidumbre que casi nunca es "
        "la correcta (error de especificación).\n"
        "- El radio de los conjuntos de ambigüedad robustos se elige **ad-hoc**, sin nivel de confianza.\n"
        "- Re-optimizar con modelos completos cada pocos minutos es **computacionalmente inviable**.")
with tabs[1]:
    st.markdown(
        "- Decisiones de programación **frágiles**: pequeños desplazamientos de la distribución "
        "degradan el costo y la confiabilidad.\n"
        "- O decisiones **excesivamente conservadoras**: reservas y costos innecesarios que "
        "encarecen la operación.\n"
        "- Violaciones operativas en tiempo intradía (rampas, reservas, balance) cuando la "
        "incertidumbre se materializa.\n"
        "- Sin garantías de cobertura, no hay forma auditable de decir «confío en esta región de "
        "incertidumbre al 95 %».")
with tabs[2]:
    st.markdown(
        "**Limitación operativa-científica que se resuelve:** los operadores carecen de un marco que "
        "(i) asigne los parámetros de robustez (radio de ambigüedad) con **validez estadística "
        "demostrable** y (ii) traduzca el programa robusto en **decisiones ágiles** cuando la "
        "incertidumbre se materializa. Es decir: ni la robustez tiene nivel de confianza, ni la "
        "velocidad tiene garantías de factibilidad.")
    warn_box("<b>Delimitación pedida por el jurado:</b> la tesis NO abarca operación en tiempo real "
             "(AGC/EMS). El horizonte es <b>día siguiente</b> (24 pasos horarios) con <b>ajuste "
             "intradía</b> (15 min). Cada técnica opera en la escala donde aporta.")
with tabs[3]:
    st.info("¿En qué medida la integración de aprendizaje por refuerzo, utilizando optimización robusta "
            "distribucional basada en distancias de Wasserstein y Conformal Prediction, mejora la "
            "calidad de las decisiones de programación operativa en sistemas eléctricos con alta "
            "penetración de energía solar y eólica, en horizontes de tiempo de corto plazo (day ahead)?")

st.divider()

# ---------------------------------------------------------------- alcance
st.markdown("#### 📦 Alcance formal: qué entra y qué queda fuera")
c1, c2 = st.columns(2)
with c1:
    st.markdown("##### ✅ Dentro del alcance")
    for item in ALCANCE["dentro"]:
        st.markdown(f"- {item}")
with c2:
    st.markdown("##### ⛔ Fuera del alcance (declarado)")
    for item in ALCANCE["fuera"]:
        st.markdown(f"- {item}")

st.plotly_chart(fig_timeline_decision(), width="stretch", theme=None, key="timeline")

st.divider()

# ---------------------------------------------------------------- incertidumbres
st.markdown("#### 🎲 El vector de incertidumbre ξ: qué se modela y por qué")
sel = st.multiselect(
    "Selecciona componentes del vector ξ para ver cómo se modelan:",
    ["Generación eólica", "Generación solar", "Demanda (por nodo/zona)", "Fallas de equipos",
     "Disponibilidad hidráulica"],
    default=["Generación eólica", "Generación solar", "Demanda (por nodo/zona)"])
model = {
    "Generación eólica": "Error de pronóstico horario de potencia eólica (cola pesada, correlación "
                         "espacial entre parques) — entra al vector ξ y a la bola de Wasserstein.",
    "Generación solar": "Error de pronóstico de irradiancia/potencia fotovoltaica (sesgo por nubosidad "
                        "de la tarde) — entra al vector ξ y a la bola de Wasserstein.",
    "Demanda (por nodo/zona)": "Error de pronóstico de demanda por nodo (correlacionado con "
                               "temperatura y actividad económica) — **incluido consistentemente en "
                               "OE1, hipótesis y diseño** (corrección al desajuste señalado por el jurado).",
    "Fallas de equipos": "**Fuera de alcance declarado** (trabajo futuro: extensión con disponibilidad "
                         "estocástica de unidades). No se modela en ξ.",
    "Disponibilidad hidráulica": "**Fuera de alcance declarado** para el horizonte diario; se asume "
                                 "programa hidráulico conocido (dato del operador).",
}
for s in sel:
    tone = "warn" if "Fuera de alcance" in model[s] else "ok"
    (warn_box if tone == "warn" else ok_box)(f"**{s}:** {model[s]}")

st.divider()

# ---------------------------------------------------------------- métricas
st.markdown("#### 📏 «Calidad de las decisiones» = 6 métricas medibles (y no adjetivos)")
st.markdown("Esta tabla reemplaza las promesas de *optimalidad, rapidez y factibilidad* por "
            "hipótesis con métrica, dirección de mejora y umbral — como pidió el jurado.")
st.dataframe(
    METRICAS, width="stretch", hide_index=True,
    column_config={
        "kpi": "KPI", "def": "Definición operativa", "dir": "Mejor",
        "meta": "Umbral de éxito (meta declarada)", "hipotesis": "Hipótesis",
    })

st.markdown("#### 🔬 Hipótesis a demostrar (antes de los experimentos)")
cols = st.columns(3)
for col, h in zip(cols, HIPOTESIS):
    with col:
        info_card(f"{h['id']}", f"<p>{h['texto']}</p>"
                  f"<p class='small-muted'><b>Contraste:</b> {h['prueba']}</p>",
                  "green" if h["id"] == "H1" else ("purple" if h["id"] == "H2" else ""))

st.divider()

# ---------------------------------------------------------------- trazabilidad
st.markdown("#### 🔗 Trazabilidad unificada: objetivo → hipótesis → actividad → métrica → comparador")
st.markdown("Corrige los desajustes señalados en **Objetivos**: una única matriz es la fuente de "
            "verdad para todo el documento. Los comparadores son siempre C0–C5.")
st.plotly_chart(fig_traceability_matrix(), width="stretch", theme=None, key="trace")
st.dataframe(COMPARADORES, width="stretch", hide_index=True,
             column_config={"id": "ID", "nombre": "Comparador", "desc": "Descripción", "rol": "Rol en la evaluación"})

st.divider()
st.markdown("##### 🌍 ¿Por qué Colombia hace única esta problemática?")
formula_note(
    "Colombia integra eólica, solar y biomasa a un sistema histórico **hidro-térmico**: la variabilidad "
    "renovable se suma a la incertidumbre hidrológica. Además, las <b>zonas no interconectadas (ZNI)</b> "
    "dependen de soluciones robustas ante fallas en entornos aislados, donde la pérdida de suministro "
    "no tiene respaldo de la red nacional. Un marco con garantías de cobertura y decisiones rápidas es "
    "particularmente valioso en este contexto [3], [49].")
