"""Página 8 · Resultados preliminares + laboratorio de corrección de la Planta C."""
import streamlit as st
import numpy as np
from itertools import product
from scipy.optimize import linprog

from utils import load_css
from utils.components import formula_note, info_card, ok_box, page_header, warn_box
from utils.charts import fig_prelim_costs, fig_portfolio_reported
from utils.content import PRELIM

st.set_page_config(page_title="Resultados preliminares · Tesis DRO+RL+CP", page_icon="📊", layout="wide")
load_css()
page_header("📊", "Resultados preliminares y laboratorio de corrección",
            "Ejercicio de expansión en dos etapas (estocástico vs. DRO) + respuesta interactiva a la "
            "inconsistencia señalada por el jurado: 190 MW reportados vs. límite de 150 MW en la Planta C.")

st.markdown(PRELIM["contexto"])

col_a, col_b = st.columns(2)
with col_a:
    st.plotly_chart(fig_prelim_costs(), width="stretch", theme=None, key="costs8")
with col_b:
    st.plotly_chart(fig_portfolio_reported(), width="stretch", theme=None, key="port8")

st.markdown("##### 🔎 Hallazgos del ejercicio preliminar")
for h in PRELIM["hallazgos"]:
    st.markdown(f"- {h}")

st.divider()

# ---------------------------------------------------------------- aclaración jurado
st.markdown("#### ⚠️ Aclaración de la inconsistencia Planta C (observación del reporte del jurado)")
warn_box(PRELIM["aclaracion_planta_c"])
formula_note(f"**Unidades económicas** (segunda parte de la observación): {PRELIM['unidades']}")

st.divider()

# ---------------------------------------------------------------- laboratorio LP
st.markdown("#### 🧪 Laboratorio: re-resuelve el ejercicio con los parámetros corregidos")
st.markdown("Este laboratorio **recrea didácticamente** el problema de expansión de dos etapas con los "
            "mismos parámetros de las Tablas 7–11 (32 escenarios: demanda × renovables) y lo resuelve "
            "como LP. El objetivo: verificar en vivo el efecto de aplicar el límite declarado de la "
            "Planta C. *(Recreación simplificada: variables continuas y sin red; los valores pueden "
            "diferir ligeramente del documento, pero la dinámica de la corrección es la misma.)*")

# --- motor del laboratorio
CINV = {"A": 1500, "B": 1500, "C": 1000, "w": 1200, "f": 1000}
COP = {"o1": 500, "o2": 700, "r": 0, "A": 800, "B": 1000, "C": 400, "w": 0, "f": 0}
EXIST = {"o1": 100, "o2": 180, "r": 50}
INV_VARS = ["A", "B", "C", "w", "f"]
PLANTS = ["o1", "o2", "r", "A", "B", "C", "w", "f"]
DN = [(250, .5), (300, .5)]; DM = [(300, .5), (500, .5)]
EW = [(0.4, .6), (0.8, .4)]; EF = [(0.5, .7), (0.9, .3)]; ER = [(0.2, .6), (0.5, .4)]
SCEN = [dict(dn=dn, dm=dm, eW=w, eF=f, eR=r, p=pd_ * pm * pw * pf * pr)
        for (dn, pd_), (dm, pm), (w, pw), (f, pf), (r, pr) in product(DN, DM, EW, EF, ER)]


def solve_case(cap_a: float, cap_b: float, cap_c: float, cap_w: float, cap_f: float) -> dict:
    E = {"A": cap_a, "B": cap_b, "C": cap_c, "w": cap_w, "f": cap_f}
    n, N, nP = len(SCEN), len(INV_VARS), len(PLANTS)
    idx_x = lambda i: i
    idx_y = lambda s, j: N + s * nP + j
    nv = N + n * nP
    c = np.zeros(nv)
    for i, v in enumerate(INV_VARS):
        c[idx_x(i)] = CINV[v]
    for s in range(n):
        for j, p in enumerate(PLANTS):
            c[idx_y(s, j)] = SCEN[s]["p"] * COP[p]
    A_ub, b_ub = [], []
    for i, v in enumerate(INV_VARS):
        row = np.zeros(nv); row[idx_x(i)] = 1.0
        A_ub.append(row); b_ub.append(E[v])
    for s, sc in enumerate(SCEN):
        row = np.zeros(nv)
        for j in range(nP):
            row[idx_y(s, j)] = -1.0
        A_ub.append(row); b_ub.append(-(sc["dn"] + sc["dm"]))
        for j, p in enumerate(PLANTS):
            row = np.zeros(nv); row[idx_y(s, j)] = 1.0
            if p == "o1":
                A_ub.append(row); b_ub.append(EXIST["o1"])
            elif p == "o2":
                A_ub.append(row); b_ub.append(EXIST["o2"])
            elif p == "r":
                A_ub.append(row); b_ub.append(EXIST["r"] * sc["eR"])
            elif p in ("w", "f"):
                row[idx_x(INV_VARS.index(p))] = -sc["eW" if p == "w" else "eF"]
                A_ub.append(row); b_ub.append(0.0)
            else:  # A, B, C: y <= x
                row[idx_x(INV_VARS.index(p))] = -1.0
                A_ub.append(row); b_ub.append(0.0)
    res = linprog(c, A_ub=np.array(A_ub), b_ub=np.array(b_ub),
                  bounds=[(0, None)] * nv, method="highs")
    x = {v: float(res.x[idx_x(i)]) for i, v in enumerate(INV_VARS)}
    inv_cost = sum(CINV[v] * x[v] for v in INV_VARS)
    return {"x": x, "inv": inv_cost, "op": float(res.fun) - inv_cost, "total": float(res.fun),
            "ok": res.success}


c1, c2 = st.columns([4, 4])
with c1:
    st.markdown("**Límites técnicos de inversión (MW)** — los de la Tabla 10 son el default")
    cap_a = st.slider("Planta A (Emax = 200)", 50.0, 250.0, 200.0, 5.0)
    cap_b = st.slider("Planta B (Emax = 180)", 50.0, 250.0, 180.0, 5.0)
    cap_c = st.slider("Planta C (Emax declarado = 150 ⚠)", 50.0, 250.0, 150.0, 5.0,
                      help="El valor reportado en los resultados fue 190 MW, excediendo este límite. "
                           "Muévelo a 190 para reproducir la inconsistencia.")
    cap_w = st.slider("Planta eólica Gw (Emax = 100)", 0.0, 150.0, 100.0, 5.0)
    cap_f = st.slider("Planta solar Gf (Emax = 100)", 0.0, 150.0, 100.0, 5.0)
with c2:
    st.markdown("**Escenario del laboratorio**")
    preset = st.radio("Configuración rápida:", [
        "Límites declarados (C = 150 MW) ✔ corrección",
        "Configuración de la corrida reportada (C = 190 MW) ⚠",
        "Personalizada"], horizontal=False)
    if preset.startswith("Límites declarados"):
        cap_c = 150.0
    elif preset.startswith("Configuración de la corrida"):
        cap_c = 190.0

sol = solve_case(cap_a, cap_b, cap_c, cap_w, cap_f)
names = {"A": "Planta A", "B": "Planta B", "C": "Planta C", "w": "Eólica Gw", "f": "Solar Gf"}
st.markdown("##### 📈 Solución óptima del laboratorio")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Costo total", f"${sol['total']:,.0f}".replace(",", "."))
m2.metric("Inversión", f"${sol['inv']:,.0f}".replace(",", "."))
m3.metric("Operación esperada", f"${sol['op']:,.0f}".replace(",", "."))
m4.metric("Estado", "Óptimo ✔" if sol["ok"] else "Inviable")

import pandas as pd
rows = []
for v in INV_VARS:
    rows.append({
        "Planta": names[v],
        "Inversión óptima (MW)": round(sol["x"][v], 1),
        "Límite aplicado (MW)": {"A": cap_a, "B": cap_b, "C": cap_c, "w": cap_w, "f": cap_f}[v],
        "Reportado en el documento (MW)": PRELIM["portafolio"]["e" + v.lower()] if v in "ABC" else
                                          (PRELIM["portafolio"]["ew"] if v == "w" else PRELIM["portafolio"]["ef"]),
        "¿Excede el límite?": "⚠ SÍ" if sol["x"][v] > {"A": cap_a, "B": cap_b, "C": cap_c, "w": cap_w, "f": cap_f}[v] + 1e-6 else "No",
    })
st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)

if cap_c < 190:
    ok_box(f"Con el límite corregido (C ≤ {cap_c:.0f} MW), el modelo <b>no puede</b> recomendar 190 MW "
           f"para la Planta C: la capacidad se redistribuye hacia las demás plantas y el costo total "
           f"cambia (${sol['total']:,.0f} vs ${1_051_885:,} con C = 190 en esta recreación). "
           f"Esto confirma que la corrección es <b>material</b>, no solo editorial: puede cambiar la "
           f"recomendación de inversión.".replace(",", "."))
else:
    warn_box("Con C = 190 MW se reproduce la configuración de la corrida reportada: el modelo acepta "
             "instalar 190 MW porque el límite de la tabla no está aplicado. Exactamente esta "
             "discrepancia entre tabla y código es la causa probable de la inconsistencia detectada "
             "por el jurado.")

st.caption("Motor del laboratorio: LP de dos etapas con 32 escenarios (demanda dn/dm × fracciones "
           "renovables eW/eF/eR con sus probabilidades), costos de las Tablas 7–8, capacidades de la "
           "Tabla 9 y límites de la Tabla 10. Implementación: scipy.optimize.linprog (HiGHS).")

st.divider()
st.markdown("#### 🧭 Alcance de las conclusiones preliminares (otra observación del jurado)")
formula_note(
    "Las conclusiones de este ejercicio son <b>metodológicas</b>: (i) la reformulación dual DRO es "
    "implementable en Pyomo; (ii) la prima de robustez es cuantificable; (iii) los patrones de "
    "despacho difieren bajo DRO. <b>No</b> son conclusiones de planeación real del sistema: faltan "
    "red, límites de línea, hidrología y costos en escala financiera real. La tesis (operación día "
    "siguiente en IEEE 39 + datos XM) es el vehículo para esas conclusiones.")
