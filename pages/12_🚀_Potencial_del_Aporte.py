"""Página 12 · Potencial del aporte de la tesis."""
import streamlit as st

from utils import load_css
from utils.components import formula_note, info_card, page_header, section_card_grid
from utils.content import APORTES, POTENCIAL, PLAN_PUBLICACION

st.set_page_config(page_title="Potencial del aporte · Tesis DRO+RL+CP", page_icon="🚀", layout="wide")
load_css()
page_header("🚀", "El potencial del aporte: qué cambia si esta tesis se desarrolla",
            "Contribuciones concretas, validación declarada y plan de publicación — la respuesta a "
            "«qué conocimiento nuevo producirá la investigación».")

st.markdown("#### 💎 Las tres contribuciones, en detalle")
for a in APORTES:
    with st.expander(f"**{a['id']} · {a['titulo']}** — {a['tipo']}", expanded=(a["id"] == "C1")):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**🔴 Vacío que llena**")
            st.markdown(a["problema"])
            st.markdown("**💎 Aporte nuevo**")
            st.markdown(a["aporte"])
        with c2:
            st.markdown("**🧪 Cómo se valida**")
            st.markdown(a["validacion"])
            st.markdown("**📤 Publicación destino**")
            st.markdown(a["publicacion"])

st.divider()

st.markdown("#### 🌟 ¿Por qué la integración es necesaria? (no es un agregado de técnicas)")
c1, c2, c3 = st.columns(3)
with c1:
    info_card("CP sin DRO", "<p>Produce intervalos con garantía que <b>nadie consume</b> en decisiones "
              "operativas: incertidumbre bien medida, pero sin traducción a acciones.</p>", "red")
with c2:
    info_card("DRO sin CP", "<p>Produce decisiones robustas pero con radio elegido <b>ad-hoc</b>: "
              "robustez sin nivel de confianza declarado ni comparable.</p>", "orange")
with c3:
    info_card("RL sin DRO", "<p>Produce decisiones rápidas pero <b>sin ancla de robustez ni "
              "factibilidad garantizada</b> ante desplazamientos de distribución.</p>", "purple")
formula_note("La tesis cierra exactamente estas tres carencias con una arquitectura coherente: "
             "<b>CP</b> mide la incertidumbre con garantía → <b>DRO</b> decide con robustez calibrada "
             "→ <b>RL</b> ejecuta con velocidad y factibilidad. Cada técnica es necesaria para que "
             "las otras dos cumplan su promesa en operación.")

st.divider()

st.markdown("#### 🎯 Impacto esperado por audiencia")
for titulo, bullets in POTENCIAL:
    st.markdown(f"##### {titulo}")
    for b in bullets:
        st.markdown(f"- {b}")

st.divider()

st.markdown("#### 📤 Plan de publicación y productos")
st.dataframe(PLAN_PUBLICACION, width="stretch", hide_index=True,
             column_config={"momento": "Momento", "producto": "Producto académico", "estado": "Estado"})

c1, c2 = st.columns(2)
with c1:
    st.markdown("##### 📈 Indicadores de impacto (metas declaradas)")
    st.markdown(
        "- ≥ 2 artículos en revistas indexadas (Q1/Q2) + 1 congreso internacional.\n"
        "- Repositorio de código y datos citable (DOI) con replicación independiente.\n"
        "- Protocolo experimental reutilizable por otros grupos (benchmark).\n"
        "- Formación de recursos humanos (asistencia de investigación, posibles tesis derivadas).")
with c2:
    st.markdown("##### 🔭 Líneas futuras que abre la tesis")
    st.markdown(
        "- Cobertura condicional (CP con covariables) para decisiones localizadas en el tiempo.\n"
        "- Extensión a zonas no interconectadas (ZNI) y microredes resilientes.\n"
        "- Incertidumbre de fallas de equipos y disponibilidad hidráulica.\n"
        "- Integración con mercados de balance y señales de precios.")

st.markdown("")
formula_note(
    "<b>La tesis en una frase:</b> transformar la robustez de la operación eléctrica con alta "
    "penetración renovable —de una práctica artesanal de tunning— en un <b>contrato estadístico "
    "verificable</b> (cobertura 1−α), ejecutado con <b>velocidad de decisión</b> (milisegundos) y "
    "auditado con un <b>benchmark reproducible</b> para el sistema colombiano.")
st.balloons()
