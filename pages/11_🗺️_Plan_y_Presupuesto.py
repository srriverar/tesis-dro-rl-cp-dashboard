"""Página 11 · Plan de trabajo, cronograma con estados y presupuesto honesto."""
import streamlit as st
import pandas as pd

from utils import load_css
from utils.components import formula_note, info_card, ok_box, page_header, warn_box
from utils.charts import fig_budget_donut, fig_gantt, fig_milestones
from utils.content import GANTT, HITOS, HOY_MES, PRESUPUESTO, GLOSARIO

st.set_page_config(page_title="Plan y Presupuesto · Tesis DRO+RL+CP", page_icon="🗺️", layout="wide")
load_css()
page_header("🗺️", "Plan de trabajo, cronograma y presupuesto",
            "Respuesta a Cronograma y Presupuesto: actividades con estados y productos verificables, "
            "hitos de validación/escritura/sustentación, y financiación clasificada con honestidad.")

# ---------------------------------------------------------------- WBS
st.markdown("#### 🧩 WBS: actividades con productos verificables (corrección de «Actividades»)")
st.markdown("El jurado pidió desagregar las tareas «indicando productos verificables» y establecer "
            "actividades explícitas para **comprobar restricciones**, **comparar métodos** y "
            "**evaluar la contribución de cada técnica**. La tabla del Gantt incluye exactamente esas "
            "tres columnas de evidencia (A5–A7).")

estados = st.multiselect("Mostrar estados:", ["Realizado", "En curso", "Pendiente"],
                         default=["Realizado", "En curso", "Pendiente"])
st.plotly_chart(fig_gantt(GANTT, HOY_MES, estados), width="stretch", theme=None, key="gantt")
st.plotly_chart(fig_milestones(HITOS, HOY_MES), width="stretch", theme=None, key="hitos")

col_t, col_n = st.columns([7, 4])
with col_t:
    df = pd.DataFrame(GANTT)
    st.dataframe(df, width="stretch", hide_index=True, height=420,
                 column_config={
                     "fase": "Paquete", "tarea": "Actividad", "inicio": "Inicio (mes)",
                     "duracion": "Duración", "estado": "Estado", "producto": "Producto verificable"})
with col_n:
    done = sum(1 for t in GANTT if t["estado"] == "Realizado")
    curso = sum(1 for t in GANTT if t["estado"] == "En curso")
    pend = sum(1 for t in GANTT if t["estado"] == "Pendiente")
    st.metric("Realizadas", f"{done} / {len(GANTT)}")
    st.metric("En curso", str(curso))
    st.metric("Pendientes", str(pend))
    warn_box("<b>Corrección del encabezado:</b> el texto del cronograma decía «Tesis de Maestría». "
             "Se corrige a «Tesis de Doctorado» en todo el documento (acción en curso). Las fechas "
             "absolutas se fijarán con el director según acta de inicio; aquí la posición actual es "
             f"M{HOY_MES} del horizonte de 48 meses.")
    st.markdown("**Hitos**")
    for h in HITOS:
        st.markdown(f"- **{h['id']}** {h['nombre']} (M{h['mes']})")

st.divider()

# ---------------------------------------------------------------- presupuesto
st.markdown("#### 💵 Presupuesto reclasificado: confirmado / en especie / por gestionar")
st.markdown("Respuesta directa a la observación sobre los $15 millones: **quedan registrados como "
            "financiación por gestionar, con fuentes identificadas — no como recurso asegurado.**")
col_d, col_p = st.columns([5, 7])
with col_d:
    st.plotly_chart(fig_budget_donut(PRESUPUESTO), width="stretch", theme=None, key="donut")
    total = sum(p["monto"] for p in PRESUPUESTO)
    st.metric("Presupuesto total estimado", f"${total:,.0f} COP".replace(",", "."))
    st.caption("USD ≈ $3.500/COP (referencia). Los rubros «en especie» y «confirmados» no requieren "
               "caja nueva.")
with col_p:
    dfp = pd.DataFrame(PRESUPUESTO)
    st.dataframe(dfp, width="stretch", hide_index=True,
                 column_config={
                     "rubro": "Rubro", "monto": st.column_config.NumberColumn("Monto (COP)", format="dollar"),
                     "tipo": "Clasificación", "fuente": "Fuente de financiación",
                     "justificacion": "Justificación (vínculo con el WBS)"})

c1, c2, c3 = st.columns(3)
with c1:
    info_card("✅ Confirmados", "<p>Licencias académicas de solver (gratuitas para investigación) y "
              "horas de investigación del grupo. No dependen de nuevas aprobaciones.</p>", "green")
with c2:
    info_card("📦 En especie", "<p>Cómputo GPU (infraestructura UNAL/grupo) y acceso a datos vía API "
              "de XM. Se documenta su valor para la auditoría del proyecto.</p>")
with c3:
    info_card("🔎 Por gestionar", "<p><b>$23 M COP</b> (congresos $15 M + APC $8 M) vía convocatorias "
              "internas de apoyo a publicación y presentación de trabajos. Se registran como "
              "<i>financiación por gestionar</i>, con su probabilidad de éxito.</p>", "orange")

st.divider()

# ---------------------------------------------------------------- correcciones editoriales
st.markdown("#### ✍️ Plan de depuración editorial (observación de Presentación y redacción)")
ed = pd.DataFrame([
    {"Corrección": "Eliminar instrucciones de plantilla del formato", "Estado": "En curso"},
    {"Corrección": "«Tesis de Maestría» → «Tesis de Doctorado» (encabezados, cronograma, presupuesto)", "Estado": "En curso"},
    {"Corrección": "Numeración única y secuencial de ecuaciones (Eqs. 1–N en orden de aparición)", "Estado": "Pendiente"},
    {"Corrección": "Tabla de consistencia símbolo ↔ ecuación ↔ tabla ↔ resultado", "Estado": "Pendiente"},
    {"Corrección": "Glosario ES/EN con término único por concepto", "Estado": "Pendiente"},
    {"Corrección": "Revisión ortográfica (erratas: «Wassers tein», «al ta», espurios de espaciado)", "Estado": "En curso"},
    {"Corrección": "Coherencia numérica: aclaración Planta C + unidades económicas", "Estado": "Hecho"},
])
st.dataframe(ed, width="stretch", hide_index=True)

st.markdown("##### 📚 Glosario ES/EN (extracto del plan de uniformidad terminológica)")
st.markdown("| Término único (ES) | Equivalente inglés | Definición |")
st.markdown("|---|---|---|")
for es, en in GLOSARIO:
    st.markdown(f"| {es} | {en} | — |")
st.caption("El documento usará solo el término español con el equivalente inglés al primer uso. "
           "Términos como «unit commitment» y «compromiso de unidades» no se alternarán.")
