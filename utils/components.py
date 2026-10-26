"""Componentes de interfaz reutilizables del dashboard."""
from __future__ import annotations

import streamlit as st

from .content import SCORE_LABELS, actions_progress


def page_header(icon: str, title: str, subtitle: str = "") -> None:
    st.markdown(f"### {icon} {title}")
    if subtitle:
        st.markdown(f'<p class="small-muted">{subtitle}</p>', unsafe_allow_html=True)
    st.divider()


def kpi_row(items: list[dict]) -> None:
    """items: {value, label, delta?, help?} — se renderizan en columnas iguales."""
    cols = st.columns(len(items))
    for col, it in zip(cols, items):
        with col:
            delta = f'<div class="kpi-delta">{it["delta"]}</div>' if it.get("delta") else ""
            st.markdown(
                f'<div class="kpi-box"><div class="kpi-value">{it["value"]}</div>'
                f'<div class="kpi-label">{it["label"]}</div>{delta}</div>',
                unsafe_allow_html=True)
            if it.get("help"):
                st.caption(it["help"])


def info_card(title: str, body_html: str, tone: str = "") -> None:
    tone_cls = f" {tone}" if tone else ""
    st.markdown(f'<div class="thesis-card{tone_cls}"><h4>{title}</h4>{body_html}</div>',
                unsafe_allow_html=True)


def quote_block(text: str) -> None:
    st.markdown(f'<div class="quote-jury">{text}</div>', unsafe_allow_html=True)


def jury_badge(score: int) -> str:
    label = SCORE_LABELS.get(score, "?")
    cls = {1: "b-insuficiente", 2: "b-aceptable", 3: "b-bueno", 4: "b-excelente"}.get(score, "")
    return f'<span class="badge-sq {cls}">{label}</span>'


def status_chip(estado: str) -> str:
    cls = {"Hecho": "e-hecho", "En curso": "e-curso", "Pendiente": "e-pendiente"}.get(estado, "e-pendiente")
    icon = {"Hecho": "✅", "En curso": "🔄", "Pendiente": "📅"}.get(estado, "•")
    return f'<span class="chip-estado {cls}">{icon} {estado}</span>'


def action_list(actions: list[dict]) -> None:
    done, total, frac = actions_progress(actions)
    st.progress(frac, text=f"Avance del plan de acción: {done}/{total} completadas")
    html = "".join(
        f"<li>{status_chip(a['estado'])} &nbsp;{a['texto']}</li>" for a in actions)
    st.markdown(f'<ul style="list-style:none; padding-left:0;">{html}</ul>',
                unsafe_allow_html=True)


def formula_note(html: str) -> None:
    st.markdown(f'<div class="formula-note">{html}</div>', unsafe_allow_html=True)


def warn_box(html: str) -> None:
    st.markdown(f'<div class="warn-box">⚠️ {html}</div>', unsafe_allow_html=True)


def ok_box(html: str) -> None:
    st.markdown(f'<div class="ok-box">✅ {html}</div>', unsafe_allow_html=True)


def render_response_block(item: dict, resp: dict, key: str) -> None:
    """Renderiza una observación del jurado con su respuesta didáctica."""
    with st.expander(f"**{item['componente']}** — {SCORE_LABELS[item['score']]}  ·  "
                     f"{resp['acciones'][0]['texto'][:40]}…", expanded=False):
        col_a, col_b = st.columns([3, 1])
        with col_a:
            quote_block(item["observacion"])
        with col_b:
            st.markdown("**Calificación del jurado**")
            st.markdown(jury_badge(item["score"]), unsafe_allow_html=True)
            done, total, frac = actions_progress(resp["acciones"])
            st.metric("Plan de acción", f"{done}/{total}", f"{frac:.0%} completado")
        st.markdown("##### 💡 Interpretación didáctica")
        st.markdown(resp["interpretacion"])
        st.markdown("##### ✅ Respuesta y plan de corrección")
        for r in resp["respuesta"]:
            st.markdown(r)
        st.markdown("##### 📋 Acciones verificables")
        action_list(resp["acciones"])
        st.markdown("##### 📦 Productos")
        st.markdown(" · ".join(f"`{p}`" for p in resp["productos"]))


def section_card_grid(cards: list[dict], cols: int = 3) -> None:
    """cards: {titulo, html, tone}"""
    for i in range(0, len(cards), cols):
        row = st.columns(cols)
        for j, col in enumerate(row):
            if i + j < len(cards):
                c = cards[i + j]
                with col:
                    info_card(c["titulo"], c["html"], c.get("tone", ""))
