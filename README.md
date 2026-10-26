# ⚡ Dashboard de sustentación — Tesis DRO + RL + CP

**Modelo de Optimización Robusta Distribucional (DRO) con Aprendizaje por Refuerzo (RL) y
Conformal Prediction (CP) para la Programación Operativa de Sistemas Eléctricos con Alta
Penetración de Fuentes de Energía Renovable**

Dashboard interactivo (Streamlit) para la sustentación del proyecto de tesis doctoral de
**Carlos Manuel Romero Rojas** (Doctorado en Ingeniería Eléctrica, Universidad Nacional de Colombia).
Presenta la propuesta en detalle, responde didácticamente las observaciones del jurado
(Camilo Andrés Cortés Guerrero) y explica de forma interactiva el **DRO**, la **distancia de
Wasserstein** y la **calibración conforme** del radio de ambigüedad.

---

## 🚀 Ejecución local

```bash
pip install -r requirements.txt
streamlit run app.py
```

## ☁️ Despliegue en Streamlit Community Cloud

1. Crea un repositorio en GitHub y sube este proyecto:
   ```bash
   git init
   git add .
   git commit -m "Dashboard sustentación tesis DRO+RL+CP"
   git branch -M main
   git remote add origin https://github.com/<tu-usuario>/tesis-dro-rl-cp-dashboard.git
   git push -u origin main
   ```
2. Entra a [share.streamlit.io](https://share.streamlit.io) → **New app**.
3. Selecciona el repositorio, la rama `main` y el archivo `app.py`.
4. Deploy. `requirements.txt` y `runtime.txt` se detectan automáticamente.

## 🗺️ Estructura del dashboard

| Página | Contenido |
|---|---|
| 🏠 Inicio | Resumen ejecutivo, arquitectura y aportes |
| 🎯 Problema e Hipótesis | Alcance delimitado, ξ, métricas y H1–H3 |
| 📚 Antecedentes y Brecha | Mapa de la brecha + explorador de 72 referencias |
| 🧠 DRO interactivo | Laboratorio minimax: prima de robustez en vivo |
| 📏 Distancia de Wasserstein | Transporte óptimo jugable (W₁, plan π, bola) |
| 🎚️ CP calibra el radio | Calibración conforme con verificación Monte Carlo |
| 🤖 RL y MDP | Constructor de MDP y función de recompensa |
| 🏗️ Arquitectura integrada | Pipeline CP → ε → DRO → RL paso a paso |
| 📊 Resultados preliminares | Laboratorio de corrección Planta C (190 vs 150 MW) |
| 💬 Respuestas al Jurado | Las 11 observaciones con respuesta y plan de acción |
| 📝 Examen de Calificación | Las 2 preguntas del jurado, interactivas |
| 🗺️ Plan y Presupuesto | Gantt con estados, hitos H1–H5, financiación honesta |
| 🚀 Potencial del Aporte | Contribuciones C1–C3 y plan de publicación |

## 🧪 Datos y reproducibilidad

- Las cifras de los **resultados preliminares** provienen de la propuesta de tesis (82 pp.).
- El **laboratorio de la Planta C** re-resuelve en vivo una recreación simplificada del problema
  de expansión de dos etapas (LP con `scipy.optimize.linprog`, 32 escenarios) con los parámetros
  de las Tablas 7–11 del documento. Está marcado explícitamente como recreación didáctica.
- Las **referencias** (72) se extrajeron de la bibliografía de la propuesta
  (`data/references.json`).

## 📄 Licencia

MIT — ver [LICENSE](LICENSE).
