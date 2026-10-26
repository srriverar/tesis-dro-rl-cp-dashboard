"""Página 2 · Antecedentes, brecha científica y explorador de referencias."""
import streamlit as st
import pandas as pd

from utils import load_css
from utils.components import formula_note, info_card, page_header, warn_box
from utils.charts import fig_gap_map
from utils.content import load_references

st.set_page_config(page_title="Antecedentes y Brecha · Tesis DRO+RL+CP", page_icon="📚", layout="wide")
load_css()
page_header("📚", "Antecedentes: de la enumeración al análisis crítico",
            "Respuesta a la observación de Antecedentes: comparación crítica, brecha científica "
            "explícita y reestructuración del marco teórico.")

st.markdown("#### 🗺️ Mapa de la brecha científica")
st.markdown("El jurado pidió identificar la brecha «con mayor precisión». Este mapa posiciona los "
            "enfoques por lo que **garantizan** (eje X: calibración estadística del riesgo) y por cómo "
            "**deciden** (eje Y: integración con aprendizaje). La brecha de la tesis es la esquina "
            "superior derecha: garantía estadística + decisión aprendida, a la vez.")
st.plotly_chart(fig_gap_map(), width="stretch", theme=None, key="gapmap")

st.markdown("##### 🎯 La brecha, en una frase verificable")
formula_note(
    "<b>Brecha:</b> ningún trabajo de la literatura revisada (72 referencias) calibra el radio del "
    "conjunto de ambigüedad de Wasserstein con garantías de cobertura en muestras finitas (Conformal "
    "Prediction) <i>y</i> lo integra con una política de aprendizaje por refuerzo para la programación "
    "operativa con alta penetración renovable. Los trabajos más cercanos resuelven solo partes: "
    "Cho &amp; Yang 2022 [6] (W-DRO para UC, radio fijo), Li et al. 2023 [7] (DRO aplicado, sin "
    "calibración), Zhu et al. 2025 [18] (DRO + RL, sin CP), Fertiz/inventario [42] (CP + DRO-W, pero "
    "no operación de sistemas eléctricos).")

st.divider()

# ---------------------------------------------------------------- tabla comparativa crítica
st.markdown("#### 🔍 Comparación crítica de los enfoques (extracto de la matriz del documento revisado)")
comp = pd.DataFrame([
    {"Familia": "Determinista", "Ejemplo": "UC clásico con pronósticos puntuales [1]",
     "Incertidumbre": "Ninguna (implícita en holguras)", "¿Calibra el riesgo?": "No",
     "Limitación central": "Fragilidad ante errores de pronóstico"},
    {"Familia": "Estocástico", "Ejemplo": "UC con escenarios [24], [2]",
     "Incertidumbre": "Distribución conocida (escenarios)", "¿Calibra el riesgo?": "No",
     "Limitación central": "Error de especificación de la distribución"},
    {"Familia": "Robusto (caja)", "Ejemplo": "RO para UC / expansión [20]",
     "Incertidumbre": "Conjunto determinista (caja)", "¿Calibra el riesgo?": "No (el conjunto es ad-hoc)",
     "Limitación central": "Conservadurismo excesivo, ignora probabilidades"},
    {"Familia": "W-DRO", "Ejemplo": "UC con políticas afines [6]; comunidad energética [7]",
     "Incertidumbre": "Bola de Wasserstein alrededor de datos", "¿Calibra el riesgo?": "Parcialmente (validación, no garantía)",
     "Limitación central": "El radio ε se fija por heurística; sin nivel de confianza"},
    {"Familia": "RL para operación", "Ejemplo": "Despacho en tiempo real [8]; UC con Q-learning [26]",
     "Incertidumbre": "Aprendida de la interacción", "¿Calibra el riesgo?": "No",
     "Limitación central": "Rápido, pero sin garantías de factibilidad ni robustez"},
    {"Familia": "CP para pronóstico", "Ejemplo": "Intervalos de carga [11], [12]; intro [10]",
     "Incertidumbre": "Cobertura 1−α del error de pronóstico", "¿Calibra el riesgo?": "Sí (en pronóstico)",
     "Limitación central": "No se consume en decisiones de optimización"},
    {"Familia": "CP + optimización", "Ejemplo": "Gestión de inventarios [42]",
     "Incertidumbre": "Conjunto calibrado por CP", "¿Calibra el riesgo?": "Sí",
     "Limitación central": "Dominio distinto (inventario); sin RL ni escalas de decisión"},
    {"Familia": "★ Esta tesis", "Ejemplo": "CP + W-DRO + RL para programación operativa",
     "Incertidumbre": "Bola W calibrada por CP (ξ multivariado)", "¿Calibra el riesgo?": "Sí (garantía finita 1−α)",
     "Limitación central": "A demostrar (H1–H3): costo, cobertura y factibilidad"},
])
st.dataframe(comp, width="stretch", hide_index=True)

st.markdown("##### 🧱 Plan de reestructuración del marco teórico (56 páginas → ~18 + anexos)")
c1, c2, c3 = st.columns(3)
with c1:
    info_card("Antes (problema señalado)",
              "<p>56 páginas con desarrollos extensos (variantes de clasificación, demostraciones "
              "auxiliares) sostenidas en <b>solo 3 fuentes distintas</b>.</p>", "red")
with c2:
    info_card("Después (plan aplicado)",
              "<p>4 fundamentos con fuentes primarias múltiples cada uno: <b>CP</b>, <b>DRO</b>, "
              "<b>Wasserstein</b>, <b>MDP/RL</b>. Cada sección termina en «qué se usa de esto en la "
              "tesis».</p>")
with c3:
    info_card("Anexos",
              "<p>Variantes (APS, CP para clasificación), demostraciones de dualidad completas, "
              "tablas de datos y detalles de implementación.</p>", "green")

st.divider()

# ---------------------------------------------------------------- explorador de referencias
st.markdown("#### 📖 Explorador de las 72 referencias del documento")
st.markdown("Clasificación temática aproximada para demostrar que la base es amplia y actual, y "
            "organizar el **análisis crítico por familia** (no solo el conteo).")
refs = load_references()
df = pd.DataFrame(refs).rename(columns={"id": "#", "text": "Referencia", "theme": "Familia temática"})
fams = sorted(df["Familia temática"].unique())
sel_fams = st.multiselect("Filtrar por familia:", fams, default=fams)
q = st.text_input("Buscar en las referencias (autor, título, año…):", "")
mask = df["Familia temática"].isin(sel_fams)
if q.strip():
    mask &= df["Referencia"].str.contains(q.strip(), case=False, regex=False)
st.dataframe(df[mask], width="stretch", hide_index=True, height=420,
             column_config={"#": st.column_config.NumberColumn(width="small"),
                            "Referencia": st.column_config.TextColumn(width="large"),
                            "Familia temática": st.column_config.TextColumn(width="medium")})
st.caption(f"Mostrando {mask.sum()} de 72 referencias. Fuentes: propuesta de tesis (§24 Bibliografía).")

st.markdown("##### 🧭 Tabla «afirmación central → fuente» (muestra del plan bibliográfico)")
st.markdown(
    "| Afirmación teórica central | Fuentes primarias (mín. 3) |\n"
    "|---|---|\n"
    "| CP garantiza cobertura 1−α en muestras finitas bajo intercambiabilidad | Vovk/Gammerman/Shafer; "
    "Lei et al. (2018); Angelopoulos & Bates [10] |\n"
    "| DRO con bola de Wasserstein admite reformulación dual tratable | Mohajerin Esfahani & Kuhn (2018); "
    "Kuhn et al. [5]; Blanchet & Murthy (2019) |\n"
    "| UC es un problema entero-mixto NP-duro con restricciones intertemporales | Bertsimas et al. (2013); "
    "Bhardwaj et al. [1]; O'Malley et al. [2] |\n"
    "| RL aproxima políticas óptimas en MDP con recompensa demorada | Sutton & Barto [9]; Mnih et al. (2015); "
    "Lillicrap et al. (2016) |\n"
    "| La demanda neta con alta penetración exige reservas de rampa, no solo de capacidad | Morales et al.; "
    "Jiménez et al. [26]; Quan et al. [24] |")
