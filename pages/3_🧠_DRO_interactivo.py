"""Página 3 · Explicador interactivo de DRO."""
import streamlit as st

from utils import load_css
from utils.components import formula_note, info_card, page_header, warn_box
from utils.charts import fig_dro_lab, fig_dro_pmf
from utils.content import PRELIM

st.set_page_config(page_title="DRO interactivo · Tesis DRO+RL+CP", page_icon="🧠", layout="wide")
load_css()
page_header("🧠", "Optimización Robusta Distribucional (DRO), jugable",
            "De la intuición a la formulación: apostar contra la peor distribución plausible, "
            "no contra un único pronóstico.")

# ---------------------------------------------------------------- analogía
st.markdown("#### 🎰 La idea central en una analogía")
info_card("¿Cuánta reserva instalarías si tu pronóstico de error pudiera estar equivocado… y no sabes cómo?",
          "<p>Un modelo <b>estocástico</b> apuesta a que tu distribución estimada es correcta. "
          "Un modelo <b>robusto (caja)</b> se prepara para cualquier cosa dentro de un rango, aunque "
          "sea muy improbable. <b>DRO</b> intermedio: se prepara para la <b>peor distribución "
          "probable</b> dentro de una <i>bola</i> de distribuciones cercanas a tus datos. Si tus datos "
          "son buenos, la bola es pequeña y pagas poco por la robustez; si hay poca confianza, la bola "
          "crece y el modelo se protege más.</p>")

st.markdown("#### 🕹️ Laboratorio: el efecto de ε sobre la decisión")
st.markdown("Mueve los controles y observa tres cosas a la vez: (1) cómo cambia el **costo worst-case**, "
            "(2) hacia dónde se desplaza la **decisión robusta**, y (3) la **prima de robustez** "
            "(el costo de prepararse para lo peor).")
c1, c2, c3 = st.columns(3)
with c1:
    eps = st.slider("Radio de ambigüedad ε (tamaño de la bola de Wasserstein)", 0.0, 1.5, 0.35, 0.05,
                    help="ε = 0 equivale a fiarse de la distribución nominal; ε grande cubre "
                         "distribuciones muy lejanas (más conservador).")
with c2:
    c_over = st.slider("Penalización por déficit (costo de no cubrir la demanda)", 5.0, 25.0, 12.0, 0.5)
with c3:
    c_under = st.slider("Costo de reserva ociosa (sobre-instalar)", 1.0, 10.0, 5.0, 0.5)

st.plotly_chart(fig_dro_lab(eps, c_under, c_over), width="stretch", theme=None, key="drolab")
col_pmf, col_note = st.columns([6, 5])
with col_pmf:
    st.plotly_chart(fig_dro_pmf(eps), width="stretch", theme=None, key="dropri")
with col_note:
    st.markdown("##### 📖 Cómo leer la gráfica")
    st.markdown(
        "- **Curva azul:** costo si la distribución nominal (la de tus datos) es la verdadera.\n"
        "- **Curva roja:** costo bajo la **peor distribución dentro de la bola** W₁(ε).\n"
        "- El **óptimo robusto** se corre hacia la derecha (más reserva) cuando crece ε o la "
        "penalización por déficit.\n"
        "- La franja naranja es la **prima de robustez**: pagar un poco más de costo nominal para "
        "proteger la cola adversa.")
    formula_note(
        "<b>Formalmente:</b> en lugar de optimizar el costo esperado bajo una sola distribución "
        "p, DRO resuelve<br><br>"
        "min<sub>x∈χ</sub> &nbsp; max<sub>p∈𝒫</sub> &nbsp; 𝔼<sub>p</sub>[ f(x, ξ) ]<br><br>"
        "donde 𝒫 es el <b>conjunto de ambigüedad</b>: todas las distribuciones «plausibles» "
        "alrededor de la distribución empírica de los datos. La tesis define 𝒫 como la "
        "<b>bola de Wasserstein</b> de radio ε alrededor de la distribución empírica Q̂₀.")
    st.caption("Laboratorio didáctico (vendedor de periódicos / reserva estática). Los valores son "
               "normalizados; la formulación completa de la tesis está más abajo.")

st.divider()

# ---------------------------------------------------------------- las cuatro filosofías
st.markdown("#### ⚖️ Las cuatro filosofías de decisión bajo incertidumbre")
fil = st.radio("Selecciona un enfoque:", ["Determinista", "Estocástico", "Robusto (caja)", "DRO"],
               horizontal=True)
desc = {
    "Determinista": ("Usa el pronóstico puntual como si fuera la verdad.",
                     "Simple y rápido.", "Frágil: cualquier error de pronóstico golpea la operación.",
                     "min<sub>x</sub> f(x, ξ̂)"),
    "Estocástico": ("Optimiza el costo esperado sobre muchos escenarios de una distribución supuesta.",
                    "Aprovecha la información probabilística.", "Si la distribución supuesta es "
                    "incorrecta, la solución puede ser mala sin advertencia.",
                    "min<sub>x</sub> 𝔼<sub>p</sub>[f(x, ξ)] con p conocida"),
    "Robusto (caja)": ("Protege contra cualquier realización dentro de un conjunto (caja).",
                       "Nunca viola restricciones dentro del conjunto.", "Excesivamente conservador: "
                       "ignora que algunos extremos son casi imposibles.",
                     "min<sub>x</sub> max<sub>ξ∈𝒰</sub> f(x, ξ)"),
    "DRO": ("Optimiza contra la peor distribución dentro de un conjunto de ambigüedad (bola).",
            "Equilibra eficiencia y robustez; usa datos en lugar de supuestos duros.",
            "El radio ε debe calibrarse bien — ¡y eso es exactamente lo que hace CP en esta tesis!",
            "min<sub>x</sub> max<sub>p∈𝒫</sub> 𝔼<sub>p</sub>[f(x, ξ)]"),
}
a, b, c, d = st.columns(4)
a.metric("Idea", desc[fil][0][:60] + "…")
with b: st.markdown(f"**Ventaja** ✅ {desc[fil][1]}")
with c: st.markdown(f"**Debilidad** ⚠️ {desc[fil][2]}")
formula_note(f"<b>Forma canónica:</b> {desc[fil][3]}")

st.divider()

# ---------------------------------------------------------------- formulación de la tesis
st.markdown("#### 📐 La formulación DRO de la tesis (del documento, §Marco teórico y §Resultados preliminares)")
st.markdown("Con expanders para navegar la derivación completa (conjunto de momentos → dualidad → LP).")
with st.expander("1 · Conjunto de ambigüedad basado en momentos (media) — usado en el ejercicio preliminar"):
    st.latex(r"\mathbb{P} := \{ p \in \mathcal{M}^+(\mathbb{R}^l) : \ p(\xi \in U) = 1, \ \mu^- \leq "
             r"\mathbb{E}_p[\xi] \leq \mu^+ \}")
    st.markdown("Todas las distribuciones con soporte en U y con media entre μ⁻ y μ⁺. El problema "
                "minimax resultante se transforma vía **dualidad de Lagrange** en un problema de "
                "programación lineal resoluble con solvers convencionales.")
    st.latex(r"\min_{x \in \chi, \gamma, \beta \geq 0, \lambda} \ \lambda + \beta^\top \mu^+ - "
             r"\gamma^\top \mu^- \qquad \text{s.t.} \quad f(x,\xi) - \lambda - \beta^\top \xi + "
             r"\gamma^\top \xi \leq 0")
with st.expander("2 · Conjunto de ambigüedad basado en la distancia de Wasserstein — el de la tesis"):
    st.latex(r"\mathbb{P}_w(\hat{Q}_0, \varepsilon) = \{ \mathbb{P} : W_\rho(\mathbb{P}, \hat{Q}_0) "
             r"\leq \varepsilon \}")
    st.markdown("Bola de radio ε alrededor de la distribución empírica Q̂₀. **El aporte de la tesis es "
                "fijar ε con calibración conforme** (página «CP calibra el radio»), en lugar de "
                "elegirlo a mano. La restricción del subproblema interno se cumple para todos los "
                "puntos extremos del conjunto de incertidumbre U.")
with st.expander("3 · ¿Por qué la reformulación dual es imprescindible?"):
    st.markdown(
        "La etapa de maximización sobre distribuciones no es implementable directamente. Al escribir "
        "el lagrangiano y exigir que la integral quede acotada, el peor caso se captura en una "
        "restricción punto a punto y todo colapsa a un **LP estándar** (Eqs. 10–13 del documento). "
        "Esto fue verificado en el ejercicio preliminar con Pyomo + solver abierto.")

st.divider()
st.markdown("#### 💰 El resultado clave del ejercicio preliminar (ver página «Resultados preliminares»)")
m1, m2, m3 = st.columns(3)
m1.metric("Costo estocástico", f"${PRELIM['costos']['estocastico']:,.0f}".replace(",", "."))
m2.metric("Costo DRO", f"${PRELIM['costos']['dro']:,.0f}".replace(",", "."))
m3.metric("Prima de robustez", "+10,05 %",
          f"+${PRELIM['costos']['dro'] - PRELIM['costos']['estocastico']:,.0f}".replace(",", "."))
st.markdown("DRO pagó un 10,05 % adicional — un «seguro» frente a distribuciones mal especificadas — "
            "y produjo patrones de despacho más defensivos (mayor uso de unidades flexibles como G02).")
warn_box("Estas cifras corresponden al <b>ejercicio preliminar de expansión</b> (conjunto de momentos), "
         "no a la operación día siguiente. Su función es validar la implementación de la reformulación "
         "dual y cuantificar la prima de robustez.")
