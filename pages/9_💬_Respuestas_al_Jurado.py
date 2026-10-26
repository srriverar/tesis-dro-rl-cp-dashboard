"""Página 9 · Respuestas didácticas a las observaciones del jurado."""
import streamlit as st

from utils import load_css
from utils.components import (
    action_list, formula_note, info_card, jury_badge, ok_box, page_header,
    quote_block, render_response_block, status_chip, warn_box,
)
from utils.charts import fig_radar_jury
from utils.content import (
    JURY_EVAL, JURY_RESPONSES, JURY_REPORT_ITEMS, SCORE_LABELS, actions_progress,
)

st.set_page_config(page_title="Respuestas al jurado · Tesis DRO+RL+CP", page_icon="💬", layout="wide")
load_css()
page_header("💬", "Respuesta a cada observación del jurado",
            "Concepto de Camilo Andrés Cortés Guerrero · 11 criterios calificados · "
            "«¿cambios significativos al documento? Sí» — aquí está la respuesta completa, "
            "con interpretación didáctica y plan de acción verificable.")

# ---------------------------------------------------------------- resumen
scores = [e["score"] for e in JURY_EVAL]
c1, c2, c3, c4 = st.columns(4)
c1.metric("Calificación promedio", f"{sum(scores)/len(scores):.2f} / 4.00")
c2.metric("Calificación más baja", "Insuficiente ×2", "Diseño · Actividades")
c3.metric("Criterios en «Bueno»", str(sum(1 for s in scores if s == 3)))
c4.metric("Cambio significativo requerido", "SÍ", "según el jurado")

meta = [4, 4, 4, 4, 4, 4, 4, 4, 3, 4, 4]
col_radar, col_plan = st.columns([6, 5])
with col_radar:
    st.plotly_chart(fig_radar_jury([e["componente"] for e in JURY_EVAL], scores, meta),
                    width="stretch", theme=None, key="radar")
with col_plan:
    total_acc = sum(len(r["acciones"]) for r in JURY_RESPONSES.values())
    total_done = sum(sum(1 for a in r["acciones"] if a["estado"] == "Hecho") for r in JURY_RESPONSES.values())
    st.progress(total_done / total_acc,
                text=f"Plan de acción global: {total_done}/{total_acc} acciones completadas")
    st.markdown("##### 🎯 Compromisos globales")
    st.markdown(
        "1. **Alcance delimitado** (día siguiente + intradía; sin tiempo real).\n"
        "2. **Contribuciones C1–C3** con validación declarada (no solo «novedad»).\n"
        "3. **Diseño reproducible**: formulación + MDP + integración CP–DRO–RL + protocolo.\n"
        "4. **WBS con productos verificables** y ablaciones por técnica.\n"
        "5. **Cronograma con estados** e hitos H1–H5; corrección «Maestría» → «Doctorado».\n"
        "6. **Presupuesto honesto**: los $15 M pasan a «por gestionar» con fuentes identificadas.\n"
        "7. **Depuración editorial** con tabla de consistencia ecuación↔tabla↔resultado.")
    ok_box("Cada observación de abajo incluye: <b>interpretación</b>, <b>respuesta</b>, "
           "<b>acciones con estado</b> y <b>productos verificables</b>.")

st.divider()

# ---------------------------------------------------------------- filtros
st.markdown("#### 🗂️ Observaciones y respuestas (filtra, busca, expande)")
f_scores = st.multiselect("Filtrar por calificación:", list(SCORE_LABELS.values()),
                          default=list(SCORE_LABELS.values()))
f_state = st.multiselect("Filtrar por estado del plan de acción:",
                         ["Hecho", "En curso", "Pendiente"], default=["Hecho", "En curso", "Pendiente"])
q = st.text_input("Buscar en las observaciones o respuestas:", "")

shown = 0
for item in JURY_EVAL:
    resp = JURY_RESPONSES[item["id"]]
    if SCORE_LABELS[item["score"]] not in f_scores:
        continue
    if not any(a["estado"] in f_state for a in resp["acciones"]):
        continue
    if q.strip():
        blob = (item["observacion"] + item["componente"] + resp["interpretacion"]
                + " ".join(resp["respuesta"])).lower()
        if q.strip().lower() not in blob:
            continue
    render_response_block(item, resp, item["id"])
    shown += 1
if shown == 0:
    st.info("Ninguna observación coincide con los filtros seleccionados.")
else:
    st.caption(f"Mostrando {shown} de {len(JURY_EVAL)} observaciones.")

st.divider()

# ---------------------------------------------------------------- reporte del jurado
st.markdown("#### 📄 Observaciones adicionales del reporte justificativo del concepto")
st.markdown("El reporte del jurado (además de la matriz de criterios) formula 6 observaciones "
            "globales. Todas tienen un frente de respuesta asignado en este dashboard:")
for it in JURY_REPORT_ITEMS:
    with st.expander(f"📌 {it['titulo']}"):
        quote_block(it["detalle"])
        st.markdown(f"**Frente de respuesta:** {it['frente']}")

st.divider()

# ---------------------------------------------------------------- compromiso final
st.markdown("#### 🤝 Compromiso de cierre")
formula_note(
    "Agradecemos la profundidad del concepto: cada observación identifica una debilidad real y "
    "accionable. Las 11 observaciones y las 6 del reporte tienen respuesta, responsable y producto "
    "verificable en este dashboard y en el plan de tesis. Las correcciones de mayor impacto — "
    "<b>diseño reproducible, contribuciones C1–C3 y protocolo experimental</b> — ya están en "
    "ejecución (ver página «Plan y Presupuesto»). El objetivo es un documento que, tras la revisión, "
    "alcance el perfil «Bueno/Excelente» en todos los criterios, con evidencia verificable.")
