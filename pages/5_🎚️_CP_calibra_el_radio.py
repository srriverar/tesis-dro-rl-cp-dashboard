"""Página 5 · Cómo CP calibra el radio de Wasserstein (respuesta metodológica central)."""
import streamlit as st

from utils import load_css
from utils.components import (
    formula_note, info_card, ok_box, page_header, warn_box,
)
from utils.charts import cp_demo, fig_cp_calibration, fig_cp_coverage
from utils.content import CADENA_CP, SUPUESTOS

st.set_page_config(page_title="CP calibra el radio · Tesis DRO+RL+CP", page_icon="🎚️", layout="wide")
load_css()
page_header("🎚️", "Cómo el Conformal Prediction calibra el radio de Wasserstein",
            "La pregunta metodológica clave del jurado — «cómo se obtendrá el radio y bajo qué "
            "supuestos serán válidas las garantías» — explicada paso a paso y verificable en vivo.")

# ---------------------------------------------------------------- cadena
st.markdown("#### 🔗 La cadena completa: de los datos al radio con garantía 1−α")
for num, nombre, desc in CADENA_CP:
    st.markdown(f"**{num}️⃣ {nombre}** — {desc}")
formula_note(
    "<b>La fórmula central:</b> con n scores de calibración s₁ ≤ s₂ ≤ … ≤ sₙ ordenados,<br><br>"
    "q̂ = s<sub>(k)</sub> &nbsp; con &nbsp; k = ⌈(n+1)(1−α)⌉<br><br>"
    "y el radio de la bola se define como <b>ε := q̂</b> (o una transformación monótona g(q̂) según la "
    "norma elegida para el score). Entonces ℙ( ξ<sub>nuevo</sub> ∈ 𝔹(Q̂₀, ε) ) ≥ 1−α. "
    "<i>La robustez deja de ser un gusto del modelador y pasa a ser un contrato estadístico.</i>")

st.divider()

# ---------------------------------------------------------------- demo interactiva
st.markdown("#### 🎛️ Laboratorio de calibración conformal (Monte Carlo en vivo)")
c1, c2, c3 = st.columns(3)
with c1:
    n_cal = st.slider("Tamaño del conjunto de calibración n", 30, 600, 120, 10)
with c2:
    alpha = st.slider("Nivel de error α", 0.01, 0.25, 0.10, 0.01,
                      help="1−α = cobertura objetivo. α = 0,10 → quieres que la bola cubra la "
                           "distribución real el 90 % de las veces.")
with c3:
    seed = st.select_slider("Semilla de simulación", options=list(range(1, 21)), value=7)

demo = cp_demo(n_cal, alpha, seed)
col_l, col_r = st.columns(2)
with col_l:
    st.plotly_chart(fig_cp_calibration(demo), width="stretch", theme=None, key="cpcal")
with col_r:
    st.plotly_chart(fig_cp_coverage(demo, 1 - alpha), width="stretch", theme=None, key="cpcov")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Cuantil conforme q̂", f"{demo['q_hat']:.3f}", help="← este número es el radio ε de la bola")
m2.metric("Nivel del cuantil", f"{demo['level']:.3f}", help="⌈(n+1)(1−α)⌉/n")
m3.metric("Cobertura media (Monte Carlo)", f"{demo['cov_mean']:.3f}", f"± {demo['cov_std']:.3f}")
m4.metric("Objetivo 1−α", f"{1 - alpha:.2f}")
ok_box(f"Con n = {n_cal} y α = {alpha:.2f}, la calibración produce q̂ = {demo['q_hat']:.2f} y, en 2000 "
       f"experimentos independientes, la cobertura lograda promedia <b>{demo['cov_mean']:.1%}</b> "
       f"≈ 1−α = {1 - alpha:.0%}. <b>Este es exactamente el mecanismo que fijará ε en la tesis.</b>")
st.caption("Los scores simulados siguen una distribución de colas pesadas (como los errores de "
           "pronóstico reales). El método no asume la forma de la distribución: solo ordena los scores.")

st.divider()

# ---------------------------------------------------------------- supuestos
st.markdown("#### 🛡️ ¿Bajo qué supuestos son válidas las garantías? (respuesta explícita al jurado)")
st.markdown("La garantía de cobertura no es «gratis»: vale bajo supuestos precisos, que la tesis "
            "declara y audita. Cada tarjeta indica cómo se maneja cada supuesto.")
cards_html = []
for nombre, desc in SUPUESTOS:
    st.markdown(f"**🔸 {nombre}**  \n{desc}")
warn_box("<b>Límite honesto de la garantía:</b> la cobertura es <i>marginal</i> (1−α en promedio), no "
         "condicional para cada escenario. Prometer cobertura condicional sería incorrecto; la tesis lo "
         "declara y estudia extensiones (CP con covariables / adaptativo) como línea de investigación.")

st.divider()

# ---------------------------------------------------------------- por qué importa
st.markdown("#### 🧩 Por qué esta calibración es el eslabón que faltaba")
c1, c2 = st.columns(2)
with c1:
    info_card("Sin CP (estado del arte actual)",
              "<p>El radio ε se fija por heurística, prueba y error, o validación informal. "
              "Problemas:</p><ul><li>No hay forma de decir «confío en esta bola al 90 %».</li>"
              "<li>Dos modeladores obtienen robustez distinta con los mismos datos.</li>"
              "<li>La comparación entre estudios es imposible (¿qué tan robusto es «robusto»?).</li></ul>", "red")
with c2:
    info_card("Con CP (aporte de la tesis)",
              "<p>ε(n, α) se deriva de los residuos de calibración:</p>"
              "<ul><li>Cobertura finita verificable (Monte Carlo + demostración).</li>"
              "<li>El operador elige α según su aversión al riesgo: decisión, no modelado.</li>"
              "<li>Comparabilidad entre sistemas y estudios.</li></ul>", "green")

st.markdown("#### 🧪 Cómo se validará en la tesis")
st.markdown(
    "1. **Demostración teórica** de la propiedad de cobertura bajo intercambiabilidad "
    "(y análisis bajo β-mixing para series temporales).\n"
    "2. **Verificación Monte Carlo** con datos sintéticos y con residuos reales de XM "
    "(≥ 1000 réplicas, curvas de cobertura vs. α y vs. n).\n"
    "3. **Sensibilidad:** ¿qué pasa con ε si n cae (pocos datos) o si α se endurece? (curvas de "
    "calibración).\n"
    "4. **Prueba end-to-end:** la bola calibrada alimenta el DRO y se mide la tasa de violación "
    "fuera de muestra (H3: ≤ 1 % de escenarios).\n"
    "5. **Monitoreo en operación:** pruebas de cobertura rodantes para detectar deriva y "
    "disparar recalibración.")
