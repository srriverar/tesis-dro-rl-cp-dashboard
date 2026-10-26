"""Página 7 · Arquitectura integrada CP → ε → DRO → RL."""
import streamlit as st

from utils import load_css
from utils.components import formula_note, info_card, ok_box, page_header, warn_box
from utils.charts import fig_architecture_flow, fig_timeline_decision
from utils.content import COMPARADORES, SUPUESTOS, CADENA_CP

st.set_page_config(page_title="Arquitectura integrada · Tesis DRO+RL+CP", page_icon="🏗️", layout="wide")
load_css()
page_header("🏗️", "La arquitectura integrada CP → ε → DRO → RL",
            "Cómo encajan las tres técnicas en un procedimiento reproducible de 8 pasos "
            "(respuesta a la observación de «Diseño de la investigación»).")

st.markdown("#### ▶️ Recorre el pipeline paso a paso")
paso = st.slider("Paso del procedimiento", 1, 8, 1)
st.plotly_chart(fig_architecture_flow(highlight=min(paso, 8) - 1 if paso <= 8 else -1),
                width="stretch", theme=None, key="flow7")
nombre, desc = [(n, d) for _, n, d in CADENA_CP][min(paso, 8) - 1]
info_card(f"Paso {paso} · {nombre}", f"<p>{desc}</p>",
          "purple" if paso in (4, 5) else ("green" if paso >= 6 else ""))

st.divider()

st.markdown("#### 🧾 El procedimiento completo (reproducible)")
st.markdown(
    "| Paso | Qué se hace | Con qué | Producto verificable |\n"
    "|---|---|---|---|\n"
    "| 1 | Recolección y curación de datos | API de XM, IEEE 39 | Dataset versionado + diccionario |\n"
    "| 2 | Pronóstico puntual de ξ = (viento, sol, demanda) | Regresores (RF/GBM/red) | Modelos + métricas de pronóstico |\n"
    "| 3 | Partición temporal 60/20/20 (sin barajar) | Validación rodante | Split documentado |\n"
    "| 4 | Calibración CP de los residuos | Scores ‖eᵢ‖, cuantil q̂ | Librería de calibración + tests de cobertura |\n"
    "| 5 | Definición del radio ε = q̂ y de la bola 𝔹(Q̂₀, ε) | W₁ sobre ξ multivariado | Parámetro ε con garantía 1−α |\n"
    "| 6 | Programa del día siguiente con DRO-W | Pyomo + solver (LP/MILP) | Programa robusto + tiempos de resolución |\n"
    "| 7 | Ajuste intradía con la política RL | Entorno Gymnasium, PPO/SAC | Acciones en ms, dentro de la holgura |\n"
    "| 8 | Evaluación y contraste de hipótesis | C0–C5, 30 semillas, Wilcoxon | Tablas con IC 95 % + factibilidad |")

st.markdown("#### 🛡️ Cadena de garantías (qué se puede prometer y con qué respaldo)")
c1, c2, c3 = st.columns(3)
with c1:
    info_card("Cobertura estadística",
              "<p>La bola de Wasserstein contiene la distribución real de errores con probabilidad "
              "≥ 1−α (CP, muestras finitas), bajo intercambiabilidad.</p>", "purple")
with c2:
    info_card("Robustez operativa",
              "<p>El programa DRO es factible para <b>toda</b> distribución dentro de la bola "
              "(reformulación dual exacta, momento finito).</p>")
with c3:
    info_card("Factibilidad en tiempo real de decisión",
              "<p>La política RL opera con enmascaramiento y proyección: solo ejecuta acciones "
              "físicamente viables (rampas, límites, min up/down).</p>", "green")
warn_box("<b>Lo que NO se promete:</b> cobertura condicional por escenario, óptimo garantizado de la "
         "política RL (es aproximada), ni robustez a fallas de equipo (fuera de alcance). "
         "Declarar los límites es parte de la contribución.")

st.divider()

st.markdown("#### 🧪 Diseño experimental: comparadores y ablaciones")
st.markdown("El jurado pidió «comparar métodos y evaluar la contribución de cada técnica». "
            "Cada comparador está diseñado para aislar un aporte:")
st.dataframe(COMPARADORES, width="stretch", hide_index=True,
             column_config={"id": "ID", "nombre": "Comparador", "desc": "Descripción",
                            "rol": "Qué evalúa / abla"})
formula_note(
    "<b>Lectura de las ablaciones:</b><br>"
    "• C4 vs C3 → aporte de <b>calibrar ε con CP</b> (¿mejora cobertura y costo CVaR?).<br>"
    "• C4 vs C5 → aporte de la <b>capa DRO</b> (¿mejora factibilidad y cola adversa?).<br>"
    "• C4 vs C1 → aporte de la <b>robustez distribucional</b> frente al enfoque estocástico.<br>"
    "• C4 vs C0 → aporte global frente a la práctica actual de pronóstico puntual.")

st.plotly_chart(fig_timeline_decision(), width="stretch", theme=None, key="tl7")
st.caption("Dos escalas temporales, un solo marco de garantías: el DRO ancla el día, el RL lo "
           "adapta al intradía.")
