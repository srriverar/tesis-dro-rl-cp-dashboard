"""CSS global del dashboard (tema claro, tarjetas y badges)."""
import streamlit as st

CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

    html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }

    .thesis-hero {
        background: linear-gradient(135deg, #0b2545 0%, #13315c 45%, #1d6094 100%);
        padding: 2.2rem 2.4rem; border-radius: 18px; color: #ffffff;
        box-shadow: 0 10px 30px rgba(11, 37, 69, 0.25); margin-bottom: 1.2rem;
    }
    .thesis-hero h1 { color: #ffffff; font-weight: 800; font-size: 2.05rem; line-height: 1.22; margin: 0 0 .6rem 0; }
    .thesis-hero h3 { color: #c6ddf1; font-weight: 400; margin: .25rem 0; font-size: 1.02rem; }
    .thesis-hero .chip {
        display: inline-block; background: rgba(255,255,255,0.14); border: 1px solid rgba(255,255,255,0.28);
        border-radius: 999px; padding: .28rem .85rem; margin: .22rem .32rem .22rem 0; font-size: .82rem;
    }

    .thesis-card {
        background: #ffffff; border: 1px solid #dde6f0; border-left: 6px solid #1d6094;
        border-radius: 12px; padding: 1.05rem 1.25rem; margin: .55rem 0 1rem 0;
        box-shadow: 0 3px 10px rgba(19, 49, 92, 0.07);
    }
    .thesis-card h4 { margin: 0 0 .45rem 0; color: #0b2545; font-size: 1.02rem; font-weight: 700; }
    .thesis-card p, .thesis-card li { color: #243b53; font-size: .93rem; line-height: 1.55; }
    .thesis-card.green { border-left-color: #2e7d4f; }
    .thesis-card.orange { border-left-color: #c47f17; }
    .thesis-card.red { border-left-color: #b23a48; }
    .thesis-card.purple { border-left-color: #5b3a8e; }

    .kpi-box {
        background: #f4f8fc; border: 1px solid #dde6f0; border-radius: 12px;
        padding: .95rem 1.15rem; text-align: center; height: 100%;
    }
    .kpi-box .kpi-value { font-size: 1.72rem; font-weight: 800; color: #0b2545; line-height: 1.15; }
    .kpi-box .kpi-label { font-size: .82rem; color: #486581; margin-top: .3rem; font-weight: 600; letter-spacing: .01em; }
    .kpi-box .kpi-delta { font-size: .78rem; margin-top: .25rem; color: #2e7d4f; }

    .badge-sq { display: inline-block; padding: .18rem .72rem; border-radius: 999px; font-size: .78rem; font-weight: 700; color: #fff; }
    .b-insuficiente { background: #b23a48; }
    .b-aceptable   { background: #c47f17; }
    .b-bueno       { background: #1d6094; }
    .b-excelente   { background: #2e7d4f; }

    .chip-estado { display: inline-block; padding: .16rem .66rem; border-radius: 999px; font-size: .76rem; font-weight: 700; margin: .12rem .22rem .12rem 0; }
    .e-hecho     { background: #e2f2e8; color: #215f3c; border: 1px solid #9dcfb2; }
    .e-curso     { background: #fff3d9; color: #8a5a00; border: 1px solid #ecc987; }
    .e-pendiente { background: #eef2f7; color: #486581; border: 1px solid #c3cfdd; }

    .quote-jury {
        background: #f8fafc; border-left: 5px solid #5b3a8e; border-radius: 8px;
        padding: .85rem 1.15rem; font-style: italic; color: #334e68; font-size: .93rem; line-height: 1.6;
    }
    .quote-jury::before { content: '🗣️  Observación del jurado · '; font-style: normal; font-weight: 700; color: #5b3a8e; }

    .formula-note {
        background: #eef4fb; border: 1px dashed #7fa8d4; border-radius: 10px;
        padding: .8rem 1.1rem; color: #13315c; font-size: .9rem; line-height: 1.6;
    }
    .warn-box {
        background: #fff6e8; border-left: 5px solid #d98c1f; border-radius: 8px;
        padding: .85rem 1.1rem; color: #6b4a08; font-size: .92rem; line-height: 1.6;
    }
    .ok-box {
        background: #edf7f0; border-left: 5px solid #2e7d4f; border-radius: 8px;
        padding: .85rem 1.1rem; color: #215f3c; font-size: .92rem; line-height: 1.6;
    }

    .small-muted { color: #829ab1; font-size: .79rem; }
    div[data-testid="stExpander"] { border: 1px solid #dde6f0 !important; border-radius: 12px !important; }
    div[data-testid="stMetric"] { background: #f4f8fc; border: 1px solid #dde6f0; border-radius: 12px; padding: .6rem .9rem; }
    section[data-testid="stSidebar"] .stMarkdown h1 { font-size: 1.25rem; }
</style>
"""


def load_css() -> None:
    """Inyecta el CSS global en cada ejecución de página (el DOM se reconstruye al navegar)."""
    st.markdown(CSS, unsafe_allow_html=True)
