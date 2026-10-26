"""Página 6 · Aprendizaje por Refuerzo y MDP para la programación del día siguiente."""
import streamlit as st

from utils import load_css
from utils.components import formula_note, info_card, page_header, warn_box
from utils.charts import fig_solve_times, fig_timeline_decision
from utils.content import EXAM_Q2

st.set_page_config(page_title="RL y MDP · Tesis DRO+RL+CP", page_icon="🤖", layout="wide")
load_css()
page_header("🤖", "El agente de Aprendizaje por Refuerzo: MDP concreto, no metáfora",
            "Estados, acciones, transiciones y recompensa definidos operativamente para la "
            "programación del día siguiente y el ajuste intradía.")

st.markdown("#### 🧩 ¿Por qué RL y no solo optimización?")
c1, c2 = st.columns(2)
with c1:
    info_card("El cuello de botella del optimizador",
              "<p>Un modelo UC-DRO completo tarda de segundos a minutos. Eso es aceptable "
              "<b>una vez al día</b>, pero no para re-dispachar cada 15 minutos cuando el viento "
              "cae o una nube cubre un parque solar. Re-resolver ante cada materialización de la "
              "incertidumbre es inviable.</p>", "orange")
with c2:
    info_card("La respuesta de la tesis: híbrido",
              "<p>El <b>DRO</b> resuelve el programa robusto del día siguiente (con garantías). "
              "El agente <b>RL</b> aprende una política de ajuste que replica y mejora al oráculo "
              "DRO en milisegundos, operando <i>dentro de la holgura robusta</i>. Velocidad sin "
              "perder factibilidad.</p>", "green")
st.plotly_chart(fig_solve_times(), width="stretch", theme=None, key="times")
st.caption("Valores ilustrativos del estado del arte (referencias [8], [26]); la tesis medirá los "
           "tiempos reales de su implementación (métrica de H2).")

st.divider()

# ---------------------------------------------------------------- MDP interactivo
st.markdown("#### 🎛️ Constructor interactivo del MDP")
st.markdown("Explora cada componente del proceso de decisión de Markov tal como se definirá en la "
            "tesis (formato de la respuesta a la pregunta 2 del examen de calificación).")
tabs = st.tabs(["Estado  sₜ", "Acción  aₜ", "Transición  P(sₜ₊₁|sₜ,aₜ)", "Recompensa  rₜ₊₁"])
for tab, comp in zip(tabs, EXAM_Q2["mdp"]):
    with tab:
        st.markdown(f"**{comp['def']}**")
        formula_note(comp["nota"])

st.markdown("##### 🎛️ Constructor de la función de recompensa")
st.markdown("Ajusta los pesos de la recompensa y observa cómo cambia el diseño de la función objetivo "
            "del agente. (El entrenamiento los validará; aquí entiendes su rol.)")
c1, c2, c3, c4 = st.columns(4)
lam_cost = c1.slider("λ · peso del costo operativo", 0.0, 2.0, 1.0, 0.1)
lam_viol = c2.slider("ρ · penalización por violación", 0.0, 20.0, 8.0, 0.5)
lam_dro = c3.slider("μ · desviación del programa DRO", 0.0, 5.0, 1.5, 0.1)
lam_res = c4.slider("ν · déficit de reserva", 0.0, 10.0, 3.0, 0.5)
formula_note(
    f"r<sub>t+1</sub> = − [ <b>{lam_cost:.1f}</b>·(costo energía + arranques) "
    f"+ <b>{lam_viol:.1f}</b>·(violación de balance/rampas/límites) "
    f"+ <b>{lam_dro:.1f}</b>·(desviación del programa DRO) "
    f"+ <b>{lam_res:.1f}</b>·(déficit de reserva) ]")
st.markdown(
    "- Un **λ (costo) alto** con ρ bajo entrena agentes económicos pero arriesgados.\n"
    "- Un **ρ (violación) alto** produce políticas conservadoras y factibles — preferible en operación.\n"
    "- **μ (desviación DRO)** mantiene al agente cerca del programa robusto (ancla de robustez).\n"
    "- **ν (reserva)** internaliza el valor de la flexibilidad, conectando con la pregunta 1 del examen.")

st.divider()

# ---------------------------------------------------------------- restricciones intertemporales
st.markdown("#### ⛓️ El punto difícil: restricciones intertemporales en un MDP")
st.markdown("Las restricciones de la operación (rampas, mínimos de encendido/apagado) hacen que la "
            "acción válida dependa de la *historia*. La tesis las incorpora por cuatro vías "
            "complementarias (respuesta del examen, pregunta 2):")
for i, item in enumerate(EXAM_Q2["intertemporales"], 1):
    st.markdown(f"{i}. {item}")
warn_box("<b>Detalle que un jurado puede preguntar:</b> ¿por qué no simplemente penalizar las "
         "violaciones? Porque penalizar no garantiza factibilidad y deforma la recompensa. El "
         "enmascaramiento + proyección garantizan que cada acción ejecutada sea físicamente viable; "
         "la penalización solo refina el desempeño económico.")

st.divider()

# ---------------------------------------------------------------- comparación
st.markdown("#### ⚖️ RL frente a la optimización convencional (tabla de la respuesta al examen)")
st.dataframe(EXAM_Q2["rl_vs_optimizacion"], width="stretch", hide_index=True,
             column_config={"eje": "Eje de comparación", "optim": "Optimización convencional",
                            "rl": "Aprendizaje por refuerzo"})
formula_note(EXAM_Q2["solucion_tesis"])
st.plotly_chart(fig_timeline_decision(), width="stretch", theme=None, key="tl2")

st.divider()
st.markdown("#### 🏋️ ¿Cómo se entrenará al agente?")
c1, c2, c3 = st.columns(3)
with c1:
    info_card("Entorno", "<p>Gymnasium a medida con el modelo de sistema embebido (Pyomo como oráculo "
                         "DRO del día siguiente). Escenarios de entrenamiento muestreados de los datos "
                         "históricos de XM + IEEE 39.</p>")
with c2:
    info_card("Algoritmo", "<p>Políticas actor-critic continuas (PPO/SAC) con <b>enmascaramiento de "
                           "acciones</b>. Pre-entrenamiento por imitación del oráculo DRO y "
                           "afinamiento por recompensa.</p>", "purple")
with c3:
    info_card("Evaluación", "<p>30 semillas, IC 95 %, comparadores C0–C5, suite de factibilidad "
                            "fuera de muestra y medición de latencia de inferencia (H2).</p>", "green")
