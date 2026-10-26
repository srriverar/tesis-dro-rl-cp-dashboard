"""Figuras Plotly del dashboard (todas interactivas y con estilo consistente)."""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from scipy.optimize import linprog

# Paleta
NAVY = "#0b2545"
BLUE = "#1d6094"
SKY = "#6290c8"
GREEN = "#2e7d4f"
ORANGE = "#c47f17"
RED = "#b23a48"
PURPLE = "#5b3a8e"
GREY = "#829ab1"
LIGHT = "#dde6f0"

GRID = dict(gridcolor="#e8eef5", zerolinecolor="#c3cfdd", linecolor="#c3cfdd")
LAYOUT = dict(
    font=dict(family="Inter, sans-serif", color="#243b53", size=13),
    paper_bgcolor="white", plot_bgcolor="white",
    margin=dict(l=40, r=20, t=60, b=45),
    hoverlabel=dict(bgcolor="white", font_size=13),
)


def _layout(fig: go.Figure, title: str, height: int = 430, y_title: str | None = None,
            x_title: str | None = None) -> go.Figure:
    fig.update_layout(title=dict(text=title, font=dict(size=17, color=NAVY), x=0.02),
                      height=height, **LAYOUT)
    fig.update_xaxes(title=x_title, **GRID)
    fig.update_yaxes(title=y_title, **GRID)
    return fig


# ---------------------------------------------------------------------------
# 1. Radar de evaluación del jurado
# ---------------------------------------------------------------------------
def fig_radar_jury(components: list[str], scores: list[int],
                   scores_goal: list[int] | None = None) -> go.Figure:
    fig = go.Figure()
    labels = [c.replace(" y ", " &<br>") for c in components]
    fig.add_trace(go.Scatterpolar(
        r=scores + scores[:1], theta=components + components[:1],
        fill="toself", name="Calificación del jurado",
        line_color=PURPLE, fillcolor="rgba(91,58,142,0.25)",
        hovertemplate="%{theta}: %{r}<extra>Jurado</extra>"))
    if scores_goal:
        fig.add_trace(go.Scatterpolar(
            r=scores_goal + scores_goal[:1], theta=components + components[:1],
            fill="toself", name="Meta del documento revisado",
            line_color=GREEN, fillcolor="rgba(46,125,79,0.13)",
            hovertemplate="%{theta}: %{r}<extra>Meta</extra>"))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 4.4], tickvals=[1, 2, 3, 4],
                                   ticktext=["Insuf.", "Acept.", "Bueno", "Excel."],
                                   gridcolor="#e8eef5"),
                   bgcolor="white"),
        title=dict(text="Perfil de evaluación · Concepto del jurado (escala 1–4)",
                   font=dict(size=17, color=NAVY), x=0.02),
        height=520, **{k: v for k, v in LAYOUT.items() if k != "margin"},
        margin=dict(l=80, r=80, t=90, b=60),
        legend=dict(orientation="h", y=-0.15))
    return fig


# ---------------------------------------------------------------------------
# 2. Laboratorio DRO: vendedor de periódicos con bola de W1
# ---------------------------------------------------------------------------
def dro_worst_case_cost(grid: np.ndarray, p0: np.ndarray, x_values: np.ndarray,
                        c_under: float, c_over: float, eps: float) -> np.ndarray:
    """Costo worst-case (bola W1 de radio eps) para cada nivel de decisión x."""
    n = len(grid)
    dx = float(grid[1] - grid[0])
    F0 = np.cumsum(p0)
    worst = np.zeros_like(x_values)
    for k, x in enumerate(x_values):
        # costo escenario a escenario: comprar x, demanda ξ
        C = c_under * np.maximum(0.0, x - grid) + c_over * np.maximum(0.0, grid - x)
        # LP: max q·C  s.t. W1(q,p0) <= eps, q simplex
        # vars: q (n) | u (n)   [u_i >= |CDF_q(i) - F0(i)|]
        c_obj = np.concatenate([-C, np.zeros(n)])            # minimizar -q·C
        A, b = [], []
        # u_i >= cumsum(q)_i - F0_i   →  cumsum(q)_i - u_i <= F0_i
        # u_i >= -(cumsum(q)_i - F0_i) → -cumsum(q)_i - u_i <= -F0_i
        for i in range(n):
            row_q = np.zeros(n); row_q[: i + 1] = 1.0
            row_u = np.zeros(n); row_u[i] = -1.0
            A.append(np.concatenate([row_q, row_u])); b.append(F0[i])
            A.append(np.concatenate([-row_q, row_u])); b.append(-F0[i])
        # W1 = Σ u_i * dx <= eps
        row = np.concatenate([np.zeros(n), np.full(n, dx)])
        A.append(row); b.append(eps)
        A_eq = np.zeros((1, 2 * n)); A_eq[0, :n] = 1.0
        res = linprog(c_obj, A_ub=np.array(A), b_ub=np.array(b),
                      A_eq=A_eq, b_eq=[1.0], bounds=[(0, None)] * (2 * n), method="highs")
        worst[k] = -res.fun if res.success else np.nan
    return worst


def fig_dro_lab(eps: float, c_under: float, c_over: float,
                x_star_shift: float = 0.0) -> go.Figure:
    """Demo: decisión de reserva vs. incertidumbre — nominal vs. peor caso en la bola W1."""
    grid = np.linspace(-3, 3, 61)
    p0 = np.exp(-0.5 * ((grid - 0.4) / 1.0) ** 2)           # pmf nominal (error de pronóstico)
    p0 = p0 / p0.sum()
    x_values = np.linspace(-1.0, 3.5, 46)

    def expected_cost(p: np.ndarray, x: float) -> float:
        C = c_under * np.maximum(0.0, x - grid) + c_over * np.maximum(0.0, grid - x)
        return float(np.dot(p, C))

    nominal = np.array([expected_cost(p0, x) for x in x_values])
    worst = dro_worst_case_cost(grid, p0, x_values, c_under, c_over, eps)

    x_nom = x_values[int(np.argmin(nominal))]
    x_rob = x_values[int(np.nanargmin(worst))]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_values, y=nominal, name="Costo esperado (distribución nominal)",
                             line=dict(color=BLUE, width=3),
                             hovertemplate="x=%{x:.2f}<br>costo=%{y:.1f}<extra>Nominal</extra>"))
    fig.add_trace(go.Scatter(x=x_values, y=worst, name="Peor caso en la bola W₁(ε)",
                             line=dict(color=RED, width=3),
                             hovertemplate="x=%{x:.2f}<br>costo=%{y:.1f}<extra>Worst-case</extra>"))
    fig.add_trace(go.Scatter(x=[x_nom], y=[nominal.min()], mode="markers+text",
                             marker=dict(size=13, color=BLUE, symbol="diamond"),
                             text=[f" óptimo nominal"], textposition="top center",
                             name="Óptimo nominal", showlegend=False))
    fig.add_trace(go.Scatter(x=[x_rob], y=[np.nanmin(worst)], mode="markers+text",
                             marker=dict(size=13, color=RED, symbol="star"),
                             text=[f" óptimo robusto"], textposition="top center",
                             name="Óptimo robusto", showlegend=False))
    fig.add_vrect(x0=x_rob, x1=x_nom if x_nom > x_rob else x_rob,
                  fillcolor="rgba(196,127,23,0.12)", line_width=0,
                  annotation_text="prima de robustez (decisión más conservadora)",
                  annotation_position="top", annotation_font_color=ORANGE)
    return _layout(
        fig,
        f"Laboratorio DRO · ε = {eps:.2f} · ¿cuánta reserva instalar ante un error de pronóstico incierto?",
        y_title="Costo total esperado (u. monetarias)", x_title="Reserva comprometida x (MW normalizados)",
        height=470)


def fig_dro_pmf(eps: float) -> go.Figure:
    """PMF nominal vs. la distribución más adversa dentro de la bola W1 (para x robusto típico)."""
    grid = np.linspace(-3, 3, 61)
    p0 = np.exp(-0.5 * ((grid - 0.4) / 1.0) ** 2); p0 = p0 / p0.sum()
    x = 1.3
    C = 5 * np.maximum(0.0, x - grid) + 12 * np.maximum(0.0, grid - x)
    worst_q = dro_worst_case_cost(grid, p0, np.array([x]), 5, 12, eps)  # solo para ε
    # recuperar q adversa resolviendo el LP de nuevo
    n = len(grid); dx = float(grid[1] - grid[0]); F0 = np.cumsum(p0)
    c_obj = np.concatenate([-C, np.zeros(n)])
    A, b = [], []
    for i in range(n):
        row_q = np.zeros(n); row_q[: i + 1] = 1.0
        row_u = np.zeros(n); row_u[i] = -1.0
        A.append(np.concatenate([row_q, row_u])); b.append(F0[i])
        A.append(np.concatenate([-row_q, row_u])); b.append(-F0[i])
    A.append(np.concatenate([np.zeros(n), np.full(n, dx)])); b.append(eps)
    A_eq = np.zeros((1, 2 * n)); A_eq[0, :n] = 1.0
    res = linprog(c_obj, A_ub=np.array(A), b_ub=np.array(b), A_eq=A_eq, b_eq=[1.0],
                  bounds=[(0, None)] * (2 * n), method="highs")
    q = res.x[:n] if res.success else p0

    fig = go.Figure()
    fig.add_trace(go.Bar(x=grid, y=p0, name="Distribución nominal Q̂₀ (empírica)",
                         marker_color=SKY, opacity=0.85,
                         hovertemplate="ξ=%{x:.2f}<br>p=%{y:.3f}<extra>Nominal</extra>"))
    fig.add_trace(go.Bar(x=grid, y=q, name="Peor distribución P* dentro de la bola",
                         marker_color=RED, opacity=0.65,
                         hovertemplate="ξ=%{x:.2f}<br>p=%{y:.3f}<extra>Adversaria</extra>"))
    fig.update_layout(barmode="overlay", legend=dict(orientation="h", y=1.12),
                      title=dict(text="La bola de Wasserstein concentra probabilidad donde más duele el costo",
                                 font=dict(size=15, color=NAVY), x=0.02),
                      height=380, **LAYOUT)
    fig.update_xaxes(title="Error de pronóstico ξ", **GRID)
    fig.update_yaxes(title="Probabilidad", **GRID)
    return fig


# ---------------------------------------------------------------------------
# 3. Distancia de Wasserstein 1-D
# ---------------------------------------------------------------------------
def fig_wasserstein_1d(mu2: float, sigma2: float, show_transport: bool = True) -> tuple[go.Figure, float]:
    """W1 entre N(0,1) y N(mu2, sigma2): área entre CDFs = W1 (caso 1-D)."""
    x = np.linspace(-5, 8, 700)
    f1 = np.exp(-0.5 * x ** 2) / np.sqrt(2 * np.pi)
    f2 = np.exp(-0.5 * ((x - mu2) / sigma2) ** 2) / (sigma2 * np.sqrt(2 * np.pi))
    F1 = np.cumsum(f1); F1 /= F1[-1]
    F2 = np.cumsum(f2); F2 /= F2[-1]
    dx = x[1] - x[0]
    w1 = float(np.sum(np.abs(F1 - F2)) * dx)

    fig = make_subplots_rows2()
    fig.add_trace(go.Scatter(x=x, y=f1, name="P — distribución origen (errores de referencia)",
                             line=dict(color=BLUE, width=3)), row=1, col=1)
    fig.add_trace(go.Scatter(x=x, y=f2, name="Q — distribución destino (régimen desplazado)",
                             line=dict(color=ORANGE, width=3)), row=1, col=1)
    fig.add_trace(go.Scatter(x=x, y=F1, name="CDF de P", line=dict(color=BLUE, width=3),
                             showlegend=False), row=2, col=1)
    fig.add_trace(go.Scatter(x=x, y=F2, name="CDF de Q", line=dict(color=ORANGE, width=3),
                             showlegend=False), row=2, col=1)
    fig.add_trace(go.Scatter(x=np.concatenate([x, x[::-1]]),
                             y=np.concatenate([F1, F2[::-1]]),
                             fill="toself", fillcolor="rgba(178,58,72,0.28)", line_width=0,
                             name="Área = W₁(P,Q)", hoverinfo="skip"), row=2, col=1)
    if show_transport:
        # flechas de transporte (mover masa) — anotaciones didácticas
        for frac in (0.15, 0.35, 0.55, 0.75, 0.92):
            i1 = int(frac * len(x))
            fig.add_annotation(x=x[i1], y=F1[i1], ax=x[i1] + mu2, ay=F2[i1],
                               xref="x3", yref="y3", axref="x3", ayref="y3",
                               arrowhead=3, arrowcolor=PURPLE, arrowwidth=1.6, opacity=0.55)
    fig.update_layout(
        title=dict(text=f"Distancia de Wasserstein W₁ = ∫|F_P − F_Q| dx = <b>{w1:.3f}</b>  "
                        f"(el área sombreada es exactamente la distancia)",
                   font=dict(size=15, color=NAVY), x=0.02),
        height=560, **LAYOUT, legend=dict(orientation="h", y=1.12))
    fig.update_xaxes(title="ξ (MW normalizados)", **GRID)
    fig.update_yaxes(title="Densidad", row=1, col=1, **GRID)
    fig.update_yaxes(title="Probabilidad acumulada", row=2, col=1, **GRID)
    return fig, w1


def make_subplots_rows2():
    """Helper: 2 filas, 1 columna."""
    from plotly.subplots import make_subplots
    return make_subplots(rows=2, cols=1, shared_xaxes=True,
                         row_heights=[0.45, 0.55], vertical_spacing=0.12)


# ---------------------------------------------------------------------------
# 4. Plan de transporte 2-D (3 fuentes → 3 destinos)
# ---------------------------------------------------------------------------
def fig_transport_plan(source_mass: list[float], sink_mass: list[float],
                       sources: np.ndarray, sinks: np.ndarray) -> tuple[go.Figure, float]:
    """Transporte óptimo entre fuentes y destinos (LP de Kantorovich)."""
    ns, nk = len(source_mass), len(sink_mass)
    src = np.asarray(source_mass, float); snk = np.asarray(sink_mass, float)
    # escalar destino para que sumen igual (masa total conservada)
    snk = snk * (src.sum() / snk.sum())
    D = np.linalg.norm(sources[:, None, :] - sinks[None, :, :], axis=2)  # costos
    c = D.ravel()
    A_eq = np.zeros((ns + nk, ns * nk))
    for i in range(ns):
        A_eq[i, i * nk:(i + 1) * nk] = 1.0
    for j in range(nk):
        A_eq[ns + j, j::nk] = 1.0
    b_eq = np.concatenate([src, snk])
    res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=[(0, None)] * (ns * nk), method="highs")
    plan = res.x.reshape(ns, nk)
    total_cost = float(res.fun)

    fig = go.Figure()
    # flechas de flujo (grosor ∝ masa)
    maxm = plan.max() if plan.max() > 0 else 1
    for i in range(ns):
        for j in range(nk):
            if plan[i, j] > 1e-6:
                fig.add_trace(go.Scatter(
                    x=[sources[i, 0], sinks[j, 0]], y=[sources[i, 1], sinks[j, 1]],
                    mode="lines", line=dict(width=1 + 9 * plan[i, j] / maxm, color=SKY),
                    opacity=0.75, showlegend=False, hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=sources[:, 0], y=sources[:, 1], mode="markers+text",
                             marker=dict(size=18 + np.asarray(source_mass) * 1.2, color=BLUE),
                             text=[f" F{i+1}<br>{m:.1f}" for i, m in enumerate(source_mass)],
                             textposition="top center", name="Fuentes (cúmulos de datos)",
                             hovertemplate="%{text}<extra></extra>"))
    fig.add_trace(go.Scatter(x=sinks[:, 0], y=sinks[:, 1], mode="markers+text",
                             marker=dict(size=18 + np.asarray(sink_mass) * 1.2, color=ORANGE, symbol="square"),
                             text=[f" D{j+1}<br>{m:.1f}" for j, m in enumerate(sink_mass)],
                             textposition="bottom center", name="Destinos (escenario desplazado)",
                             hovertemplate="%{text}<extra></extra>"))
    fig.update_layout(
        title=dict(text=f"Problema de transporte óptimo · costo mínimo W = Σ masa × distancia = "
                        f"<b>{total_cost:.2f}</b>", font=dict(size=15, color=NAVY), x=0.02),
        height=460, **LAYOUT, legend=dict(orientation="h", y=1.1))
    fig.update_xaxes(visible=False); fig.update_yaxes(visible=False, scaleanchor="x")
    return fig, total_cost


def fig_transport_matrix(plan: np.ndarray) -> go.Figure:
    fig = go.Figure(go.Heatmap(z=plan, colorscale="Blues", showscale=True,
                               colorbar=dict(title="masa"),
                               hovertemplate="F%{y} → D%{x}<br>masa = %{z:.2f}<extra></extra>"))
    fig.update_layout(title=dict(text="Plan de transporte π (acoplamiento óptimo)",
                                 font=dict(size=14, color=NAVY), x=0.02),
                      height=320, xaxis_title="Destino", yaxis_title="Fuente", **LAYOUT)
    return fig


# ---------------------------------------------------------------------------
# 5. Calibración conformal (CP)
# ---------------------------------------------------------------------------
def cp_demo(n_cal: int, alpha: float, seed: int = 7) -> dict:
    """Simula scores de no conformidad y calcula q̂ + cobertura Monte Carlo."""
    rng = np.random.default_rng(seed)
    # scores: magnitud de error con cola pesada (así es en pronósticos reales)
    def draw(n):
        return np.abs(rng.standard_t(df=4, size=n)) * 1.15
    scores = draw(n_cal)
    level = min(1.0, np.ceil((n_cal + 1) * (1 - alpha)) / n_cal)
    q_hat = float(np.quantile(scores, level, method="higher"))
    # cobertura teórica y Monte Carlo
    trials = 2000
    covs = np.empty(trials)
    for t in range(trials):
        sc = draw(n_cal)
        q = np.quantile(sc, level, method="higher")
        covs[t] = np.mean(draw(30) <= q)          # 30 puntos de prueba por réplica
    return dict(scores=scores, q_hat=q_hat, level=level, cov_mean=float(covs.mean()),
                cov_std=float(covs.std()), covs=covs, alpha=alpha, n_cal=n_cal)


def fig_cp_calibration(demo: dict) -> go.Figure:
    scores, q_hat, alpha = demo["scores"], demo["q_hat"], demo["alpha"]
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=scores, nbinsx=42, name="Scores de no conformidad (calibración)",
                               marker_color=SKY, opacity=0.8,
                               hovertemplate="score=%{x:.2f}<br>conteo=%{y}<extra></extra>"))
    fig.add_vline(x=q_hat, line=dict(color=RED, width=3, dash="dash"),
                  annotation_text=f" q̂ = {q_hat:.2f} (umbral conforme)",
                  annotation_position="top right", annotation_font_color=RED)
    fig.add_vrect(x0=q_hat, x1=float(scores.max()) * 1.02, fillcolor="rgba(178,58,72,0.12)",
                  line_width=0, annotation_text=f"zona de error α = {alpha:.2f}",
                  annotation_position="top left", annotation_font_color=RED)
    fig.update_layout(title=dict(text=f"Calibración conformal · n = {demo['n_cal']} · "
                                     f"α = {alpha:.2f} → q̂ = {q_hat:.2f}",
                                 font=dict(size=15, color=NAVY), x=0.02),
                      height=400, **LAYOUT, bargap=0.05, showlegend=False)
    fig.update_xaxes(title="Score sᵢ = ‖eᵢ‖ (magnitud del error)", **GRID)
    fig.update_yaxes(title="Frecuencia", **GRID)
    return fig


def fig_cp_coverage(demo: dict, target: float) -> go.Figure:
    covs = demo["covs"]
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=covs, nbinsx=36, marker_color=GREEN, opacity=0.8,
                               name="Cobertura lograda en 2000 réplicas",
                               hovertemplate="cobertura=%{x:.3f}<br>réplicas=%{y}<extra></extra>"))
    fig.add_vline(x=target, line=dict(color=NAVY, width=3, dash="dash"),
                  annotation_text=f" objetivo 1−α = {target:.2f}",
                  annotation_position="top", annotation_font_color=NAVY)
    fig.update_layout(title=dict(text=f"Verificación Monte Carlo · cobertura media = "
                                     f"{demo['cov_mean']:.3f} ± {demo['cov_std']:.3f}",
                                 font=dict(size=15, color=NAVY), x=0.02),
                      height=360, **LAYOUT, showlegend=False)
    fig.update_xaxes(title="Cobertura empírica", **GRID)
    fig.update_yaxes(title="Réplicas", **GRID)
    return fig


# ---------------------------------------------------------------------------
# 6. Cadena CP → ε → DRO → RL (diagrama de flujo)
# ---------------------------------------------------------------------------
def fig_architecture_flow(highlight: int = -1) -> go.Figure:
    boxes = [
        ("Datos XM\n+ IEEE 39", 0.06, 0.72, SKY),
        ("Pronóstico\npuntual", 0.22, 0.72, SKY),
        ("Residuos\n(errores)", 0.38, 0.72, SKY),
        ("CP: scores\n→ q̂(n, α)", 0.54, 0.72, PURPLE),
        ("Radio ε\nbola W₁(ε)", 0.70, 0.72, PURPLE),
        ("DRO día\nsiguiente", 0.70, 0.28, BLUE),
        ("RL ajuste\nintradía (ms)", 0.38, 0.28, GREEN),
        ("Operación\ncon garantías", 0.10, 0.28, GREEN),
    ]
    fig = go.Figure()
    arrows = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7)]
    for a, b in arrows:
        x0, y0 = boxes[a][1] + 0.065, boxes[a][2]
        x1, y1 = boxes[b][1] + 0.065, boxes[b][2]
        fig.add_annotation(x=x1, y=y1 + (0.10 if y1 > y0 else (-0.10 if y1 < y0 else 0)),
                           ax=x0, ay=y0 + (0.10 if y0 >= y1 else -0.10),
                           xref="x", yref="y", axref="x", ayref="y",
                           arrowhead=3, arrowwidth=2.5, arrowcolor="#486581",
                           standoff=6, startstandoff=6)
    for i, (label, x, y, color) in enumerate(boxes):
        is_hi = (highlight == i)
        fig.add_shape(type="rect", x0=x, y0=y - 0.115, x1=x + 0.13, y1=y + 0.115,
                      fillcolor=color, line=dict(color="white", width=3 if is_hi else 1),
                      opacity=1.0 if is_hi else 0.88)
        fig.add_annotation(x=x + 0.065, y=y, text=f"<b>{label}</b>", showarrow=False,
                           font=dict(color="white", size=12.5), align="center")
    fig.update_layout(title=dict(text="Arquitectura integrada CP → DRO → RL (2 escalas temporales)",
                                 font=dict(size=16, color=NAVY), x=0.02),
                      height=430, **LAYOUT)
    fig.update_xaxes(visible=False, range=[0, 1]); fig.update_yaxes(visible=False, range=[0, 1])
    return fig


def fig_timeline_decision() -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[0, 24], y=[2, 2], mode="lines", line=dict(color=BLUE, width=18),
                             name="DRO · programa del día siguiente (24 pasos horarios)",
                             hovertemplate="resuelto 1 vez / día (%{x} h)<extra></extra>"))
    for h in np.arange(0.25, 24, 0.25):
        fig.add_trace(go.Scatter(x=[h, h], y=[1, 1], mode="lines",
                                 line=dict(color=GREEN, width=4), showlegend=False,
                                 hovertemplate=f"decisión RL cada 15 min ({h:.2f} h)<extra></extra>"))
    fig.add_trace(go.Scatter(x=[0, 24], y=[1, 1], mode="lines", line=dict(color="white", width=1),
                             name="RL · ajuste intradía cada 15 min (milisegundos)",
                             hovertemplate="ajuste RL<extra></extra>"))
    fig.add_trace(go.Scatter(x=[0, 24], y=[0.35, 0.35], mode="lines",
                             line=dict(color=GREY, width=2, dash="dash"),
                             name="Tiempo real (AGC/EMS) — fuera de alcance de la tesis"))
    fig.update_layout(title=dict(text="Escalas de decisión de la tesis",
                                 font=dict(size=16, color=NAVY), x=0.02),
                      height=330, **LAYOUT, legend=dict(orientation="h", y=-0.25))
    fig.update_xaxes(title="Horas del día operativo", range=[-0.5, 24.5], **GRID)
    fig.update_yaxes(visible=False, range=[0, 2.8])
    return fig


# ---------------------------------------------------------------------------
# 7. Resultados preliminares y laboratorio de corrección
# ---------------------------------------------------------------------------
def fig_prelim_costs() -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["Optimización estocástica", "DRO (momentos)"], y=[1_092_300, 1_202_100],
        marker_color=[BLUE, RED], text=["$1.092.300", "$1.202.100"], textposition="outside",
        hovertemplate="%{x}<br>costo total = %{y:,.0f}<extra></extra>"))
    fig.add_annotation(x=1, y=1_260_000, text="Prima de robustez<br><b>+$109.800 (+10,05 %)</b>",
                       showarrow=True, arrowhead=2, arrowcolor=ORANGE, font_color=ORANGE)
    fig.update_layout(title=dict(text="Costo total mínimo · ejercicio preliminar (unidades monetarias del modelo)",
                                 font=dict(size=15, color=NAVY), x=0.02),
                      height=380, **LAYOUT, showlegend=False)
    fig.update_yaxes(title="Costo total (inversión + operación esperada)", **GRID)
    return fig


def fig_portfolio_reported() -> go.Figure:
    names = ["Nueva eólica (Gw)", "Nueva solar (Gf)", "Nueva planta A", "Nueva planta B", "Nueva planta C"]
    vals = [0, 100, 190, 120, 190]
    limits = [100, 100, 200, 180, 150]
    colors = [GREEN if v <= l else RED for v, l in zip(vals, limits)]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=names, y=vals, marker_color=colors,
                         text=[f"{v:.0f} MW" for v in vals], textposition="outside",
                         name="Reportado", hovertemplate="%{x}: %{y} MW<extra>Reportado</extra>"))
    fig.add_trace(go.Bar(x=names, y=limits, marker_color="rgba(130,154,177,0.35)",
                         name="Límite técnico (Tabla 10)",
                         hovertemplate="%{x}: límite %{y} MW<extra></extra>"))
    fig.add_trace(go.Bar(x=["Nueva planta C"], y=[150], marker_color=RED, opacity=0.0,
                         showlegend=False, hoverinfo="skip"))
    fig.add_hline(y=150, line=dict(color=RED, width=2, dash="dot"),
                  annotation_text="Límite declarado de la Planta C = 150 MW  ⚠ el valor reportado (190 MW) lo excede",
                  annotation_font_color=RED, annotation_position="top left")
    fig.update_layout(title=dict(text="Portafolio reportado vs. límites técnicos declarados",
                                 font=dict(size=15, color=NAVY), x=0.02),
                      height=430, barmode="overlay", **LAYOUT,
                      legend=dict(orientation="h", y=1.12))
    fig.update_yaxes(title="Capacidad (MW)", **GRID)
    return fig


def fig_gantt(tasks: list[dict], hoy: int, show_states: list[str]) -> go.Figure:
    color = {"Realizado": GREEN, "En curso": ORANGE, "Pendiente": GREY}
    fig = go.Figure()
    shown = [t for t in tasks if t["estado"] in show_states]
    for t in shown:
        fig.add_trace(go.Bar(
            x=[t["duracion"]], y=[t["tarea"]], base=[t["inicio"]], orientation="h",
            marker_color=color[t["estado"]], name=t["estado"],
            legendgroup=t["estado"], showlegend=t["estado"] not in [s.name for s in fig.data],
            hovertemplate=(f"<b>{t['tarea']}</b><br>{t['fase']}<br>"
                           f"M{t['inicio']}–M{t['inicio'] + t['duracion']}<br>"
                           f"Producto: {t['producto']}<br>Estado: {t['estado']}<extra></extra>")))
    for h in tasks[0:0]:
        pass
    fig.add_vline(x=hoy, line=dict(color=RED, width=3),
                  annotation_text=f" Hoy (M{hoy})", annotation_font_color=RED,
                  annotation_position="top")
    fig.update_layout(title=dict(text="Cronograma actualizado · horizonte 48 meses · estados verificables",
                                 font=dict(size=15, color=NAVY), x=0.02),
                      height=560, barmode="stack", **LAYOUT,
                      legend=dict(orientation="h", y=1.1))
    fig.update_xaxes(title="Meses desde el inicio (M0)", range=[-1, 49], **GRID)
    fig.update_yaxes(autorange="reversed", **GRID)
    return fig


def fig_milestones(hitos: list[dict], hoy: int) -> go.Figure:
    fig = go.Figure()
    color = {"En curso": ORANGE, "Pendiente": GREY, "Realizado": GREEN}
    fig.add_trace(go.Scatter(
        x=[h["mes"] for h in hitos], y=[1] * len(hitos), mode="markers+text",
        marker=dict(size=22, color=[color[h["estado"]] for h in hitos], symbol="diamond"),
        text=[h["id"] for h in hitos], textposition="middle center",
        hovertemplate=[f"<b>{h['nombre']}</b><br>M{h['mes']}<br>{h['estado']}<extra></extra>" for h in hitos]))
    for h in hitos:
        fig.add_annotation(x=h["mes"], y=0.82, text=h["nombre"], showarrow=False,
                           font=dict(size=10.5, color="#486581"), textangle=0)
    fig.add_vline(x=hoy, line=dict(color=RED, width=3))
    fig.update_layout(title=dict(text="Hitos de validación, escritura y sustentación",
                                 font=dict(size=15, color=NAVY), x=0.02),
                      height=300, **LAYOUT, showlegend=False)
    fig.update_xaxes(title="Mes", range=[-1, 51], **GRID)
    fig.update_yaxes(visible=False, range=[0.5, 1.25])
    return fig


def fig_budget_donut(items: list[dict]) -> go.Figure:
    from collections import defaultdict
    agg = defaultdict(float)
    for it in items:
        agg[it["tipo"]] += it["monto"]
    colors = {"Confirmado": GREEN, "En especie": SKY, "Por gestionar": ORANGE}
    fig = go.Figure(go.Pie(labels=list(agg.keys()), values=list(agg.values()),
                           hole=0.55, marker=dict(colors=[colors[k] for k in agg]),
                           textinfo="label+percent",
                           hovertemplate="%{label}<br>$%{value:,.0f} COP<extra></extra>"))
    fig.update_layout(title=dict(text="Composición del presupuesto por tipo de financiación",
                                 font=dict(size=15, color=NAVY), x=0.02),
                      height=380, **LAYOUT)
    return fig


# ---------------------------------------------------------------------------
# 8. Examen: curva de pato y reservas
# ---------------------------------------------------------------------------
def fig_duck_curve(solar_pct: float, wind_pct: float, variability: float) -> go.Figure:
    h = np.arange(0, 24, 0.25)
    demand = 0.62 + 0.13 * np.exp(-0.5 * ((h - 10) / 3.2) ** 2) + 0.32 * np.exp(-0.5 * ((h - 19.2) / 2.1) ** 2)
    solar = solar_pct * np.exp(-0.5 * ((h - 12.6) / 3.4) ** 2)
    wind = wind_pct * (0.55 + 0.45 * np.sin(h / 3.1 + 1.2) ** 2)
    net = demand - solar - wind
    rng = np.random.default_rng(3)
    net_obs = net + rng.normal(0, variability * 0.012, size=h.shape)

    ramp = np.diff(net_obs) / 0.25
    up = float(np.max(ramp)); down = float(np.min(ramp))
    i_up = int(np.argmax(ramp)) + 1

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=h, y=demand, name="Demanda", line=dict(color=BLUE, width=2.5),
                             hovertemplate="%{x:.2f} h<br>%{y:.2f} p.u.<extra></extra>"))
    fig.add_trace(go.Scatter(x=h, y=demand, name="Generación renovable (viento + sol)",
                             stackgroup="r", line=dict(width=0.5, color=GREEN),
                             fillcolor="rgba(46,125,79,0.35)", hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=h, y=demand - solar - wind, name="Renovable", stackgroup="r",
                             line=dict(width=0.5, color=GREEN), showlegend=False, hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=h, y=net_obs, name="Demanda neta (con incertidumbre)",
                             line=dict(color=RED, width=3),
                             hovertemplate="%{x:.2f} h<br>neto=%{y:.2f} p.u.<extra></extra>"))
    fig.add_trace(go.Scatter(x=[h[i_up]], y=[net_obs[i_up]], mode="markers+text",
                             marker=dict(size=14, color=ORANGE, symbol="triangle-up"),
                             text=[f" rampa ↑ máx: {up:.3f} p.u./h"], textposition="top right",
                             name="Punto crítico de rampa", showlegend=False))
    fig.update_layout(title=dict(text=f"Curva de pato · solar {solar_pct:.0%} · viento {wind_pct:.0%} · "
                                     f"variabilidad {variability:.0%} — la reserva debe cubrir la rampa, no solo el pico",
                                 font=dict(size=14, color=NAVY), x=0.02),
                      height=440, **LAYOUT, legend=dict(orientation="h", y=1.14))
    fig.update_xaxes(title="Hora del día", **GRID)
    fig.update_yaxes(title="Potencia (p.u.)", **GRID)
    return fig, up, down


def fig_reserves_vs_penetration(penetration: float, alpha: float) -> go.Figure:
    pens = np.linspace(0.05, 0.8, 60)
    # requerimiento ilustrativo: desviación de la demanda neta crece con la penetración
    sigma = 0.02 + 0.22 * pens ** 1.25
    z = abs(np.sqrt(2) * erfinv_approx(1 - 2 * alpha / 2)) if alpha > 0 else 2.0
    reserve = z * sigma
    ramp = (0.03 + 0.30 * pens ** 1.15)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=pens, y=reserve, name=f"Reserva de capacidad (cuantil 1−α, α={alpha:.2f})",
                             line=dict(color=BLUE, width=3),
                             hovertemplate="penetración=%{x:.0%}<br>reserva=%{y:.3f} p.u.<extra></extra>"))
    fig.add_trace(go.Scatter(x=pens, y=ramp, name="Reserva de rampa (banda de respuesta)",
                             line=dict(color=ORANGE, width=3, dash="dash"),
                             hovertemplate="penetración=%{x:.0%}<br>rampa=%{y:.3f} p.u.<extra></extra>"))
    fig.add_trace(go.Scatter(x=[penetration], y=[float(np.interp(penetration, pens, reserve))],
                             mode="markers", marker=dict(size=14, color=RED),
                             name="Escenario seleccionado",
                             hovertemplate="penetración=%{x:.0%}<br>reserva=%{y:.3f} p.u.<extra></extra>"))
    fig.update_layout(title=dict(text="Reservas vs. penetración renovable: capacidad, rampa y nivel de confianza",
                                 font=dict(size=15, color=NAVY), x=0.02),
                      height=420, **LAYOUT, legend=dict(orientation="h", y=1.13))
    fig.update_xaxes(title="Penetración renovable (% de energía)", tickformat=".0%", **GRID)
    fig.update_yaxes(title="Requerimiento (p.u. de capacidad del sistema)", **GRID)
    return fig


def erfinv_approx(y: float) -> float:
    """Aproximación de la inversa de erf (Winitzki) para cuantiles normales."""
    import math
    a = 0.147
    ln = math.log(1 - y * y)
    t1 = 2 / (math.pi * a) + ln / 2
    return math.copysign(math.sqrt(math.sqrt(t1 * t1 - ln / a) - t1), y)


# ---------------------------------------------------------------------------
# 9. Mapa de brecha científica
# ---------------------------------------------------------------------------
def fig_gap_map() -> go.Figure:
    pts = [
        ("Optimización estocástica (escenarios)", 0.05, 0.15, 26, GREY),
        ("Robust optimization (caja)", 0.02, 0.12, 26, GREY),
        ("W-DRO aplicado (p. ej. [6], [7], [49])", 0.18, 0.22, 34, SKY),
        ("RL para despacho/UC ([8], [25], [26])", 0.10, 0.82, 34, SKY),
        ("CP para pronósticos ([10]–[12])", 0.62, 0.18, 30, PURPLE),
        ("CP + optimización (inventario [42])", 0.72, 0.30, 30, PURPLE),
        ("DRO + RL (resiliencia [18])", 0.22, 0.62, 32, SKY),
        ("Propuesta: CP + W-DRO + RL (esta tesis)", 0.92, 0.90, 46, RED),
    ]
    fig = go.Figure()
    for name, x, y, size, color in pts:
        fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers+text", name=name,
                                 marker=dict(size=size, color=color, opacity=0.85),
                                 text=[name.split("(")[0].strip() if color != RED else "★ " + name],
                                 textposition="top center" if color != RED else "middle right",
                                 hovertemplate=f"<b>{name}</b><br>calibración estadística: {x:.0%}"
                                               f"<br>integración decisión-aprendizaje: {y:.0%}<extra></extra>"))
    fig.add_shape(type="rect", x0=0.75, y0=0.72, x1=1.02, y1=1.02,
                  fillcolor="rgba(178,58,72,0.10)", line=dict(color=RED, width=1.5, dash="dot"))
    fig.add_annotation(x=0.885, y=0.755, text="zona de la brecha científica",
                       showarrow=False, font=dict(color=RED, size=11.5))
    fig.update_layout(title=dict(text="Mapa de posicionamiento · la brecha está donde se cruzan garantía estadística y decisión aprendida",
                                 font=dict(size=14.5, color=NAVY), x=0.02),
                      height=520, **LAYOUT, legend=dict(font=dict(size=11)))
    fig.update_xaxes(title="Calibración estadística del riesgo (baja → alta)", range=[-0.05, 1.08], **GRID)
    fig.update_yaxes(title="Integración decisión-aprendizaje (baja → alta)", range=[-0.05, 1.12], **GRID)
    return fig


def fig_solve_times() -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["Solver UC-DRO\n(re-resolución intradía)", "Política RL\n(inferencia)"],
        y=[240, 0.02], marker_color=[RED, GREEN],
        text=["≈ 4 min", "≈ 20 ms"], textposition="outside",
        hovertemplate="%{x}: %{y} s<extra></extra>"))
    fig.update_layout(title=dict(text="Latencia de decisión en operación (valores ilustrativos del estado del arte)",
                                 font=dict(size=15, color=NAVY), x=0.02),
                      height=360, **LAYOUT, showlegend=False)
    fig.update_yaxes(title="Segundos por decisión (escala log)", type="log", **GRID)
    return fig


def fig_traceability_matrix() -> go.Figure:
    """Heatmap de trazabilidad objetivo × artefacto."""
    rows = ["OE1 · Modelar incertidumbre", "OE2 · Integrar DRO–RL + CP", "OE3 · Evaluar desempeño"]
    cols = ["Pregunta", "Hipótesis", "Actividad (WBS)", "Métrica", "Comparador"]
    z = [[1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1]]
    text = [["P1", "H2", "A1–A2", "Cobertura 1−α", "C3 vs C4"],
            ["P1", "H1/H2", "A3–A5", "Costo · latencia", "C4 vs C5"],
            ["P1", "H1/H3", "A6–A7", "Costo · CVaR · violación", "C0–C5"]]
    fig = go.Figure(go.Heatmap(z=z, text=text, texttemplate="%{text}", colorscale=[[0, "#e8f0f8"], [1, "#cfe0f0"]],
                               showscale=False, xgap=4, ygap=4,
                               hovertemplate="%{y} ↔ %{x}: %{text}<extra></extra>"))
    fig.update_layout(title=dict(text="Matriz de trazabilidad (única fuente de verdad del documento revisado)",
                                 font=dict(size=15, color=NAVY), x=0.02),
                      height=330, **LAYOUT)
    fig.update_xaxes(side="top", **GRID); fig.update_yaxes(autorange="reversed", **GRID)
    return fig
