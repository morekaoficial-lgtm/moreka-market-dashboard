#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gráficos y visualizaciones del dashboard."""

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def render_pie_chart(df_positions):
    """Renderiza gráfico de pastel de posiciones."""
    if df_positions.empty:
        st.info("Sin datos de posiciones")
        return

    color_map = {
        "🟢 Más barato": "#059669",
        "🟡 Bajo promedio": "#eab308",
        "⚪ En promedio": "#94a3b8",
        "🟠 Sobre promedio": "#f97316",
        "🔴 Más caro": "#dc2626",
    }

    fig = px.pie(
        df_positions,
        values="Cantidad",
        names="Posición",
        color="Posición",
        color_discrete_map=color_map,
        hole=0.55,
    )
    fig.update_layout(
        height=380,
        font=dict(family="Inter, sans-serif", size=12),
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
        margin=dict(t=20, b=20, l=20, r=20),
    )
    st.plotly_chart(fig, use_container_width=True)


def render_histogram(df_summary):
    """Renderiza histograma de diferencias vs promedio."""
    df_with_analysis = df_summary[df_summary["Diff % vs Prom"].notna()].copy()
    if df_with_analysis.empty:
        st.info("Sin datos de diferencia vs promedio")
        return

    fig = px.histogram(
        df_with_analysis,
        x="Diff % vs Prom",
        nbins=30,
        color_discrete_sequence=["#2563eb"],
        labels={"Diff % vs Prom": "Diferencia % vs Promedio de Mercado"},
    )
    fig.add_vline(
        x=0, line_dash="dash", line_color="#ef4444", line_width=2,
        annotation_text="Promedio del mercado", annotation_position="top"
    )
    fig.update_layout(
        height=380,
        font=dict(family="Inter, sans-serif"),
        xaxis_title="Diferencia % vs Promedio",
        yaxis_title="Cantidad de Productos",
        margin=dict(t=20, b=20, l=20, r=20),
    )
    st.plotly_chart(fig, use_container_width=True)
