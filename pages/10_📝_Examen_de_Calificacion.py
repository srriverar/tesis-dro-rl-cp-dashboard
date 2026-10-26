"""Página 10 · Examen de calificación: respuestas didácticas e interactivas."""
import streamlit as st

from utils import load_css
from utils.components import formula_note, info_card, page_header, warn_box
from utils.charts import fig_duck_curve, fig_reserves_vs_penetration
from utils.content import EXAM_Q1, EXAM_Q2

st.set_page_config(page_title="Examen de calificación · Tesis DRO+RL+CP", page_icon="📝", layout="wide")
load_css()
page_header("📝", "Examen de calificación: las dos preguntas del jurado",
            "Respuestas didácticas con herramientas interactivas: reservas operativas con alta "
            "penetración renovable y representación MDP de la programación del día siguiente.")

tab_q1, tab_q2 = st.tabs(["❓ Pregunta 1 · Reservas operativas", "❓ Pregunta 2 · MDP y RL"])

# =================================================================== PREGUNTA 1
with tab_q1:
    st.markdown(f"> {EXAM_Q1['pregunta']}")
    st.markdown("#### 1️⃣ Los tres conceptos que hay que distinguir")
    c1, c2, c3 = st.columns(3)
    for col, comp in zip((c1, c2, c3), EXAM_Q1["tres_conceptos"]):
        with col:
            info_card(comp["nombre"], f"<p>{comp['def']}</p>"
                      f"<p class='small-muted'><b>Por qué no basta solo:</b> {comp['insuficiente_sola']}</p>",
                      "red" if "rampa" in comp["nombre"] else "")

    st.markdown("#### 2️⃣ ¿Por qué la generación instalada suficiente NO garantiza atender la demanda neta?")
    for p in EXAM_Q1["por_que_no_basta"]:
        st.markdown(p)
    warn_box("<b>Ejemplo numérico para el jurado:</b> un sistema con 300 % de capacidad instalada "
             "renombrable puede fallar si su <i>rampa</i> útil es menor que la caída de la demanda "
             "neta al atardecer (curva de pato), o si la reserva está en unidades que requieren "
             "horas de arranque. La suficiencia estática no implica flexibilidad dinámica.")

    st.markdown("#### 3️⃣ La curva de pato, jugable: dónde duele realmente la variabilidad")
    c1, c2, c3 = st.columns(3)
    solar = c1.slider("Penetración solar (fracción del pico)", 0.0, 0.8, 0.35, 0.05)
    wind = c2.slider("Penetración eólica (base)", 0.0, 0.5, 0.15, 0.05)
    var = c3.slider("Variabilidad / error de pronóstico", 0.0, 1.0, 0.35, 0.05)
    fig, up, down = fig_duck_curve(solar, wind, var)
    st.plotly_chart(fig, width="stretch", theme=None, key="duck")
    m1, m2, m3 = st.columns(3)
    m1.metric("Rampa ascendente máxima", f"{up:.3f} p.u./h", "requisito de reserva ↑")
    m2.metric("Rampa descendente máxima", f"{down:.3f} p.u./h", "requisito de flexibilidad ↓",
              delta_color="inverse")
    m3.metric("Ancho de la banda de error", f"±{var * 0.012 * 2:.3f} p.u.", "define el cuantil 1−α")
    st.caption("El punto crítico (triángulo naranja) suele estar al atardecer: caída solar + pico de "
               "demanda. Ahí la reserva de **rampa** importa más que la reserva de **capacidad**.")

    st.markdown("#### 4️⃣ Criterios para evaluar el compromiso costo–flexibilidad–confiabilidad")
    st.dataframe(EXAM_Q1["criterios"], width="stretch", hide_index=True,
                 column_config={"nombre": "Dimensión", "metrica": "Métrica propuesta",
                                "lectura": "Cómo se lee"})
    st.markdown("#### 5️⃣ Reservas vs. penetración: la curva que un operador debe ver")
    c1, c2 = st.columns(2)
    pen = c1.slider("Penetración renovable seleccionada", 0.05, 0.80, 0.45, 0.05)
    alpha_r = c2.slider("Nivel de confianza α para el cuantil de error", 0.01, 0.30, 0.10, 0.01)
    st.plotly_chart(fig_reserves_vs_penetration(pen, alpha_r), width="stretch",
                    theme=None, key="reserv")
    st.markdown("La reserva de capacidad crece con la **cola** del error de pronóstico de la demanda "
                "neta; la reserva de rampa crece con su **velocidad de variación**. Dimensionar solo "
                "con reglas fijas (p. ej. 5 % de la demanda) es exactamente lo que la tesis reemplaza "
                "por cuantiles calibrados con CP.")

    formula_note(EXAM_Q1["solucion_tesis"])

# =================================================================== PREGUNTA 2
with tab_q2:
    st.markdown(f"> {EXAM_Q2['pregunta']}")
    st.markdown("#### 1️⃣ La representación MDP: los cuatro componentes")
    tabs = st.tabs(["Estado", "Acción", "Transición", "Recompensa"])
    for tab, comp in zip(tabs, EXAM_Q2["mdp"]):
        with tab:
            st.markdown(f"**Definición concreta:** {comp['def']}")
            formula_note(comp["nota"])
    formula_note("<b>MDP formal:</b> (S, A, P, R, γ) con S ⊂ ℝⁿ el espacio de estados descrito arriba, "
                 "A el conjunto de acciones enmascaradas por factibilidad, P(s′|s, a) el modelo de "
                 "transición aprendido de datos, R la recompensa inmediata y γ el factor de descuento. "
                 "La política óptima π* maximiza 𝔼[Σ γᵗ rₜ₊₁]; el agente la aproxima por función "
                 "(actor-critic).")

    st.markdown("#### 2️⃣ Restricciones intertemporales: cómo se incorporan")
    for i, item in enumerate(EXAM_Q2["intertemporales"], 1):
        st.markdown(f"{i}. {item}")
    warn_box("<b>Detalle técnico:</b> sin augmentación del estado, el proceso NO sería de Markov: "
             "la factibilidad de una acción depende del tiempo en estado (min up/down) y de la "
             "producción previa (rampas). Incluir esas variables en sₜ es lo que hace válido el marco MDP.")

    st.markdown("#### 3️⃣ ¿Qué papel cumple RL frente a la optimización convencional?")
    st.dataframe(EXAM_Q2["rl_vs_optimizacion"], width="stretch", hide_index=True,
                 column_config={"eje": "Eje", "optim": "Optimización convencional",
                                "rl": "Aprendizaje por refuerzo"})
    formula_note(EXAM_Q2["solucion_tesis"])

    st.markdown("#### 4️⃣ Diseña tu propio MDP (para fijar conceptos)")
    c1, c2, c3 = st.columns(3)
    estado = c1.selectbox("¿Qué información lleva el estado?",
                          ["Solo la hora y el pronóstico",
                           "Hora, pronósticos, estado de unidades, rampas y reservas ✔",
                           "Última acción tomada"])
    accion = c2.selectbox("¿Cómo se trata la acción?",
                          ["Sin restricciones (se penaliza después)",
                           "Enmascarada por factibilidad + proyección ✔",
                           "Discreta: solo encender/apagar"])
    recomp = c3.selectbox("¿Qué optimiza la recompensa?",
                          ["Solo el costo económico",
                           "Costo + violaciones + desviación del programa DRO + déficit de reserva ✔",
                           "Solo la factibilidad"])
    if "✔" in estado and "✔" in accion and "✔" in recomp:
        ok_box("¡Configuración correcta! Este es el MDP de la tesis: estado completo (propiedad de "
               "Markov), acciones factibles por diseño y recompensa multicriterio anclada al programa "
               "robusto del DRO.")
    else:
        st.error("Revisa las opciones marcadas con ✔: esa es la configuración justificada en la "
                 "respuesta de arriba.")
