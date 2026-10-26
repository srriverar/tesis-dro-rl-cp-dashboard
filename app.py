"""Dashboard de sustentación — Tesis doctoral DRO + RL + CP.

Ejecución local:  streamlit run app.py
"""
import streamlit as st

from utils import load_css
from utils.components import info_card, kpi_row, page_header, section_card_grid
from utils.content import TESIS, APORTES, JURY_EVAL
import utils.charts as charts

st.set_page_config(
    page_title="Tesis DRO + RL + CP · Dashboard de sustentación",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)
load_css()

# ---------------------------------------------------------------- hero
st.markdown(
    f"""
    <div class="thesis-hero">
      <h1>⚡ {TESIS['titulo']}</h1>
      <h3>Dashboard interactivo para la sustentación del proyecto de tesis doctoral</h3>
      <div>
        <span class="chip">👤 {TESIS['proponente']}</span>
        <span class="chip">🎓 {TESIS['programa'].split('—')[0].strip()}</span>
        <span class="chip">🧭 Línea: {TESIS['linea']}</span>
        <span class="chip">📌 {TESIS['normativa']}</span>
      </div>
      <div>
        <span class="chip">Director: {TESIS['director'].split('(')[0].strip()}</span>
        <span class="chip">Codirector: {TESIS['codirector'].split('(')[0].strip()}</span>
        <span class="chip">Jurado evaluador: {TESIS['jurado'].split('—')[0].strip()}</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

kpi_row([
    {"value": "4", "label": "TÉCNICAS INTEGRADAS", "delta": "CP · Wasserstein · DRO · RL"},
    {"value": "3", "label": "CONTRIBUCIONES DOCTORALES", "delta": "método · arquitectura · evidencia"},
    {"value": "72", "label": "REFERENCIAS ANALIZADAS", "delta": "6 familias temáticas"},
    {"value": "11/11", "label": "OBSERVACIONES DEL JURADO CON RESPUESTA", "delta": "plan de acción verificable"},
    {"value": "6", "label": "COMPARADORES PRE-REGISTRADOS", "delta": "C0 – C5 + ablaciones"},
])

st.markdown("")

# ---------------------------------------------------------------- tesis en 60 segundos
st.markdown("### 🎯 La tesis en 60 segundos")
c1, c2, c3 = st.columns(3)
with c1:
    info_card("🔴 El problema",
              "<p>Con mucha generación solar y eólica, la <b>demanda neta</b> se vuelve impredecible "
              "y cambia rápido. Los modelos estocásticos asumen una distribución que casi nunca es "
              "correcta; los robustos son demasiado conservadores; y re-optimizar cada pocos minutos "
              "es demasiado lento.</p>", "red")
with c2:
    info_card("🔵 La propuesta",
              "<p><b>CP</b> calibra con garantía estadística el radio de una <b>bola de Wasserstein</b>; "
              "el <b>DRO</b> programa el día siguiente contra la peor distribución de esa bola; y un "
              "agente <b>RL</b> ajusta intradía en milisegundos dentro de la holgura robusta.</p>")
with c3:
    info_card("🟢 El potencial del aporte",
              "<p>Convertir la «robustez» en un <b>contrato estadístico explícito</b> (cobertura 1−α), "
              "articular garantías worst-case con velocidad de decisión, y entregar un benchmark "
              "reproducible para el sistema colombiano.</p>", "green")

st.markdown("")

# ---------------------------------------------------------------- arquitectura + navegación
col_fig, col_nav = st.columns([7, 5])
with col_fig:
    st.plotly_chart(charts.fig_architecture_flow(), width="stretch",
                    theme=None, key="flow_home")
with col_nav:
    st.markdown("#### 🗺️ Cómo usar este dashboard")
    st.markdown(
        """
| Página | Qué encontrarás |
|---|---|
| **🎯 Problema e Hipótesis** | Alcance delimitado, incertidumbres y H1–H3 medibles |
| **📚 Antecedentes y Brecha** | Mapa de la brecha científica + explorador de 72 referencias |
| **🧠 DRO interactivo** | Laboratorio minimax: la prima de robustez, en vivo |
| **📏 Distancia de Wasserstein** | Transporte óptimo jugable: mueve la masa y calcula W₁ |
| **🎚️ CP calibra el radio** | Cómo α, n y los residuos definen ε — con Monte Carlo |
| **🤖 RL y MDP** | Estados, acciones, transiciones, recompensa (con constructor) |
| **🏗️ Arquitectura integrada** | El pipeline CP → ε → DRO → RL paso a paso |
| **📊 Resultados preliminares** | Laboratorio de corrección de la Planta C (190 vs 150 MW) |
| **💬 Respuestas al jurado** | Las 11 observaciones con respuesta didáctica y acciones |
| **📝 Examen de calificación** | Las 2 preguntas del jurado, explicadas de forma interactiva |
| **🗺️ Plan y Presupuesto** | Gantt con estados, hitos H1–H5 y financiación honesta |
| **🚀 Potencial del aporte** | Qué gana la disciplina, el sector y la academia |
        """
    )
    st.info("💡 Todo el contenido es interactivo: mueve sliders, filtra, expande. "
            "Las cifras de los ejercicios preliminares están marcadas como **ilustrativas** cuando "
            "corresponden a recreaciones didácticas.")

st.divider()

# ---------------------------------------------------------------- contribuciones
st.markdown("### 🚀 Las tres contribuciones que justifican el doctorado")
cards = []
for a in APORTES:
    cards.append({
        "titulo": f"{a['id']} · {a['titulo']}",
        "html": (f"<p><b>Tipo:</b> {a['tipo']}</p>"
                 f"<p><b>Vacío que llena:</b> {a['problema']}</p>"
                 f"<p><b>Aporte:</b> {a['aporte']}</p>"
                 f"<p class='small-muted'>Validación: {a['validacion']} · Publicación: {a['publicacion']}</p>"),
        "tone": "purple" if a["id"] == "C1" else ("green" if a["id"] == "C3" else ""),
    })
section_card_grid(cards, cols=3)

st.markdown("")
st.markdown(
    '<p class="small-muted">Dashboard construido con Streamlit · código abierto para GitHub + Streamlit '
    'Community Cloud · datos del ejercicio preliminar tomados de la propuesta de tesis (82 pp.) y del '
    'concepto del jurado (5 pp.)</p>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------- sidebar
with st.sidebar:
    st.markdown("## ⚡ Tesis DRO + RL + CP")
    st.markdown(f"**{TESIS['proponente']}**  \n{TESIS['programa']}")
    st.divider()
    scores = [e["score"] for e in JURY_EVAL]
    st.markdown("**Evaluación del jurado**")
    st.progress(sum(scores) / (4 * len(scores)), text=f"Promedio: {sum(scores)/len(scores):.2f} / 4.00")
    st.caption("11 criterios calificados · se requieren cambios significativos · "
               "este dashboard responde cada uno.")
    st.divider()
    st.markdown("**Leyenda de estados**")
    st.markdown('<span class="chip-estado e-hecho">✅ Hecho</span> '
                '<span class="chip-estado e-curso">🔄 En curso</span> '
                '<span class="chip-estado e-pendiente">📅 Pendiente</span>',
                unsafe_allow_html=True)
    st.caption("«Hecho» = resuelto en este dashboard o en el plan de tesis; "
               "«En curso» = de ejecución inmediata tras la sustentación.")
