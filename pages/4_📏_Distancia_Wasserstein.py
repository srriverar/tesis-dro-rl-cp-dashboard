"""Página 4 · Explicador interactivo de la distancia de Wasserstein."""
import streamlit as st
import numpy as np

from utils import load_css
from utils.components import formula_note, info_card, page_header, ok_box
from utils.charts import fig_wasserstein_1d, fig_transport_plan, fig_transport_matrix

st.set_page_config(page_title="Distancia de Wasserstein · Tesis DRO+RL+CP", page_icon="📏", layout="wide")
load_css()
page_header("📏", "La distancia de Wasserstein, jugable",
            "El «costo de mover masa» como métrica entre distribuciones: el corazón geométrico "
            "del conjunto de ambigüedad de la tesis.")

# ---------------------------------------------------------------- analogía
st.markdown("#### 🚚 Analogía del camión de tierra (optimal transport)")
info_card("¿Cuánto cuesta transformar un montículo de tierra en otro?",
          "<p>Imagina dos montículos de tierra (dos distribuciones). La <b>distancia de Wasserstein</b> "
          "es el costo mínimo de mover la tierra de un montículo al otro, donde el costo es "
          "<i>masa × distancia transportada</i>. Si los montículos están lejos o tienen formas muy "
          "distintas, el transporte es caro. Si son casi iguales, es barato. W = 0 solo cuando las "
          "distribuciones coinciden.</p>"
          "<p>Por eso también se llama <b>Earth Mover's Distance (EMD)</b>: a diferencia de otras "
          "divergencias (KL, χ²), penaliza suavemente los desplazamientos — es la métrica correcta "
          "cuando «estar un poco equivocado» debe costar «un poco».</p>", "purple")

st.divider()

# ---------------------------------------------------------------- demo 1D
st.markdown("#### 🎛️ Demo 1 · Área entre CDFs = W₁ (muve la distribución)")
st.markdown("La distancia de Wasserstein de orden 1 tiene una lectura visual en 1-D: **es exactamente "
            "el área entre las funciones de distribución acumulada**. Desplaza la distribución destino "
            "y observa cómo crece el área.")
c1, c2, c3 = st.columns(3)
with c1:
    mu2 = st.slider("Desplazamiento de la media de Q", -2.0, 4.0, 1.2, 0.1,
                    help="Simula un cambio de régimen: sesgo del pronóstico, nueva planta, cambio climático.")
with c2:
    sigma2 = st.slider("Dispersión de Q (σ)", 0.4, 3.0, 1.4, 0.1,
                       help="Simula un aumento de la volatilidad del error de pronóstico.")
with c3:
    show_t = st.checkbox("Mostrar flechas de transporte", value=True)
fig, w1 = fig_wasserstein_1d(mu2, sigma2, show_t)
st.plotly_chart(fig, width="stretch", theme=None, key="w1")
st.metric("Distancia W₁(P, Q) calculada en vivo", f"{w1:.3f}",
          delta=f"{'+' if w1 > 1.0 else ''}{w1 - 1.0:.2f} vs. desplazamiento de referencia",
          delta_color="inverse")
st.caption("W₁ crece linealmente con el desplazamiento de la media y con la diferencia de dispersión. "
           "Esta sensibilidad es lo que hace a W₁ ideal para detectar desplazamientos de distribución.")

st.divider()

# ---------------------------------------------------------------- demo transporte 2D
st.markdown("#### 🎛️ Demo 2 · El plan de transporte (acoplamiento óptimo)")
st.markdown("En dimensiones mayores, Wasserstein resuelve un **problema de optimización**: encontrar "
            "el plan de transporte π que minimiza Σ masa × distancia. Modifica las masas y observa el "
            "plan óptimo y su costo.")
st.markdown(
    r"$$W_\rho(p, q) = \left( \inf_{\pi \in \Pi(p,q)} \int d(x,y)^\rho \, d\pi(x,y) \right)^{1/\rho}"
    r"= \left( \inf_{\pi \in \Pi(p,q)} \sum_{i,j} \pi_{ij} \, \|x_i - y_j\|^\rho \right)^{1/\rho}$$")
c1, c2 = st.columns(2)
with c1:
    st.markdown("**Masas en las fuentes (cúmulos de datos)**")
    s1 = st.slider("F1", 0.2, 3.0, 1.2, 0.1)
    s2 = st.slider("F2", 0.2, 3.0, 1.0, 0.1)
    s3 = st.slider("F3", 0.2, 3.0, 0.8, 0.1)
with c2:
    st.markdown("**Masas en los destinos (escenario desplazado)**")
    d1 = st.slider("D1", 0.2, 3.0, 0.6, 0.1)
    d2 = st.slider("D2", 0.2, 3.0, 1.3, 0.1)
    d3 = st.slider("D3", 0.2, 3.0, 1.1, 0.1)

sources = np.array([[0.0, 0.0], [2.0, 0.3], [0.7, 2.1]])
sinks = np.array([[1.6, 1.9], [3.4, 0.9], [2.6, -0.4]])
fig_t, total = fig_transport_plan([s1, s2, s3], [d1, d2, d3], sources, sinks)
col_a, col_b = st.columns([7, 5])
with col_a:
    st.plotly_chart(fig_t, width="stretch", theme=None, key="tplan")
with col_b:
    st.metric("Costo de transporte (W del plan)", f"{total:.2f}")
    plan = np.zeros((3, 3))
    # recomputar plan para la matriz (mismo LP)
    from scipy.optimize import linprog
    src = np.array([s1, s2, s3]); snk = np.array([d1, d2, d3]); snk = snk * (src.sum() / snk.sum())
    D = np.linalg.norm(sources[:, None, :] - sinks[None, :, :], axis=2)
    A_eq = np.zeros((6, 9))
    for i in range(3):
        A_eq[i, i * 3:(i + 1) * 3] = 1.0
    for j in range(3):
        A_eq[3 + j, j::3] = 1.0
    res = linprog(D.ravel(), A_eq=A_eq, b_eq=np.concatenate([src, snk]),
                  bounds=[(0, None)] * 9, method="highs")
    plan = res.x.reshape(3, 3)
    st.plotly_chart(fig_transport_matrix(plan), width="stretch", theme=None, key="tmat")
    ok_box("El plan π es un <b>acoplamiento</b> entre las dos distribuciones: cada celda dice cuánta "
           "probabilidad se transporta de la fuente i al destino j. W es el costo total de este plan "
           "óptimo.")

st.divider()

# ---------------------------------------------------------------- bola de Wasserstein
st.markdown("#### ⚽ De la distancia a la bola: el conjunto de ambigüedad")
formula_note(
    "Una vez tenemos una métrica entre distribuciones, el conjunto de ambigüedad es natural:<br><br>"
    "𝔹(Q̂₀, ε) = { ℙ : W<sub>ρ</sub>(ℙ, Q̂₀) ≤ ε }<br><br>"
    "Todas las distribuciones a distancia ≤ ε de la distribución empírica. El DRO optimiza contra la "
    "<b>peor</b> distribución de esta bola. Tres propiedades la hacen ideal para la tesis:"
    "<ul><li><b>Data-driven:</b> Q̂₀ viene de los datos (no de supuestos paramétricos).</li>"
    "<li><b>Interpretable:</b> ε mide «cuánto podríamos estar equivocados» en las mismas unidades "
    "del error.</li>"
    "<li><b>Calibrable:</b> existe un valor de ε con significado estadístico — y la tesis lo obtiene "
    "por Conformal Prediction (próxima página).</li></ul>")
st.info("👆 En el laboratorio DRO de la página anterior pudiste ver la bola en acción: al crecer ε, "
        "la distribución adversaria (roja) se aleja de la nominal (azul) — pero solo hasta donde el "
        "transporte lo permite.")

st.markdown("#### 🧮 Propiedades que el jurado puede preguntar")
p1, p2, p3 = st.columns(3)
with p1:
    info_card("Es una métrica real",
              "<p>Cumple identidad, simetría y desigualdad triangular. W = 0 ⟺ las distribuciones "
              "coinciden. A diferencia de la divergencia de KL, está definida aunque los soportes no "
              "se solapen.</p>")
with p2:
    info_card("Convergencia débil",
              "<p>W<sub>ρ</sub>(ℙ<sub>n</sub>, ℙ) → 0 si y solo si ℙ<sub>n</sub> converge débilmente "
              "a ℙ con momentos de orden ρ convergentes. Por eso «más datos ⇒ bola más confiable» "
              "es un teorema, no una esperanza.</p>", "green")
with p3:
    info_card("Diferenciable y tratable",
              "<p>Para costos lineales y soportes finitos, el subproblema interno del DRO se "
              "reformula como LP (o como restricción de soporte finito). Compatible con Pyomo y "
              "solvers estándar — así se implementó el ejercicio preliminar.</p>", "orange")

st.markdown("#### 🔗 Conexión concreta con la tesis")
st.markdown(
    "- La distribución empírica Q̂₀ es la de los **errores de pronóstico multivariados** "
    "ξ = (viento, sol, demanda) de los datos de XM.\n"
    "- La bola W₁(ε) representa «todos los regímenes de error plausibles».\n"
    "- El DRO despacha contra el peor régimen de la bola → decisiones factibles incluso bajo el peor "
    "desplazamiento.\n"
    "- **ε no se elige a mano:** se calibra con CP para que la bola contenga la distribución real con "
    "probabilidad ≥ 1−α (página siguiente).")
