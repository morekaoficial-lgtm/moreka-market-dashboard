#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Componentes reutilizables del dashboard."""

import streamlit as st
import pandas as pd
import os
from src.config import REPORTS_DIR, POSITIONS


def load_css():
    """Carga los estilos CSS personalizados."""
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "styles.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def render_header():
    """Renderiza el header principal."""
    st.markdown('''
    <div class="header-bar">
        <h1>📊 MOREKA SHOP — Análisis de Mercado</h1>
        <p>Comparación de precios vs competencia en Mercado Libre México</p>
    </div>
    ''', unsafe_allow_html=True)


def render_info_bar(df_summary, with_comp, without_comp, timestamp):
    """Renderiza la barra de métricas superiores."""
    total = len(df_summary)
    comp_pct = round(with_comp / total * 100) if total else 0
    ts_str = timestamp[:16] if timestamp != "Desconocido" else "N/A"

    st.markdown(f'''
    <div style="display: flex; gap: 1rem; margin-bottom: 1rem;">
        <div style="background: white; border-radius: 8px; padding: 0.8rem 1.2rem; border: 1px solid #e2e8f0; flex: 1; text-align: center;">
            <div style="font-size: 1.4rem; font-weight: 800; color: #1e3a8a;">{total}</div>
            <div style="font-size: 0.75rem; color: #64748b; text-transform: uppercase;">Total Productos</div>
        </div>
        <div style="background: white; border-radius: 8px; padding: 0.8rem 1.2rem; border: 1px solid #e2e8f0; flex: 1; text-align: center;">
            <div style="font-size: 1.4rem; font-weight: 800; color: #2563eb;">{with_comp} <span style="font-size: 0.85rem; font-weight: 500;">({comp_pct}%)</span></div>
            <div style="font-size: 0.75rem; color: #64748b; text-transform: uppercase;">Con Competencia</div>
        </div>
        <div style="background: white; border-radius: 8px; padding: 0.8rem 1.2rem; border: 1px solid #e2e8f0; flex: 1; text-align: center;">
            <div style="font-size: 1.4rem; font-weight: 800; color: #64748b;">{without_comp}</div>
            <div style="font-size: 0.75rem; color: #64748b; text-transform: uppercase;">Sin Competencia</div>
        </div>
        <div style="background: white; border-radius: 8px; padding: 0.8rem 1.2rem; border: 1px solid #e2e8f0; flex: 1; text-align: center;">
            <div style="font-size: 1.1rem; font-weight: 700; color: #1e3a8a;">{ts_str}</div>
            <div style="font-size: 0.75rem; color: #64748b; text-transform: uppercase;">Última Actualización</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)


def render_metrics(df_summary):
    """Renderiza las tarjetas de métricas principales."""
    total = len(df_summary)
    with_discount = len(df_summary[df_summary["Precio Original"] != "—"])
    avg_price = df_summary["Precio Actual"].mean()
    max_diff = df_summary["Diff % vs Prom"].max()
    min_diff = df_summary["Diff % vs Prom"].min()

    metrics = [
        ("💰 Precio Promedio", f"${avg_price:,.0f}", "#2563eb"),
        ("🏷️ Con Descuento", f"{with_discount} <span style='font-size:0.8rem'>({round(with_discount/total*100)}%)</span>" if total else "0", "#059669"),
        ("📉 Diferencia Máx", f"+{max_diff:.0f}%" if pd.notna(max_diff) else "N/A", "#dc2626"),
        ("📈 Diferencia Mín", f"{min_diff:.0f}%" if pd.notna(min_diff) else "N/A", "#059669"),
    ]

    cols = st.columns(4)
    for i, (label, value, color) in enumerate(metrics):
        with cols[i]:
            st.markdown(f'''
            <div class="metric-card" style="border-top: 3px solid {color};">
                <div class="metric-number" style="color: {color};">{value}</div>
                <div class="metric-label" style="color: {color};">{label}</div>
            </div>
            ''', unsafe_allow_html=True)


def render_position_metrics(pos_counts):
    """Renderiza las métricas de posición."""
    st.markdown('<div class="section-header">📈 Distribución de Posiciones</div>', unsafe_allow_html=True)

    cols = st.columns(5)
    for i, (label, css_class, _) in enumerate(POSITIONS):
        count = pos_counts.get(label, 0)
        with cols[i]:
            st.markdown(f'''
            <div class="metric-card {css_class}">
                <div class="metric-number">{count}</div>
                <div class="metric-label">{label}</div>
            </div>
            ''', unsafe_allow_html=True)


def render_sidebar_filters(df_summary):
    """Renderiza los filtros de la sidebar."""
    st.sidebar.header("🔍 Filtros")

    filters = {}

    positions = ["Todas"] + sorted(df_summary["Posición"].dropna().unique().tolist())
    filters["position"] = st.sidebar.selectbox("Posición en mercado", positions)

    catalog_options = ["Todos", "Con Catálogo ML", "Sin Catálogo ML"]
    filters["catalog"] = st.sidebar.selectbox("Tipo de catálogo", catalog_options)

    methods = ["Todos"] + sorted(df_summary["Método"].dropna().unique().tolist())
    filters["method"] = st.sidebar.selectbox("Método de análisis", methods)

    categories = ["Todas"] + sorted(df_summary["Categoría"].dropna().unique().tolist())
    filters["category"] = st.sidebar.selectbox("Categoría ML", categories)

    filters["search"] = st.sidebar.text_input("Buscar por SKU o título")

    filters["price_range"] = st.sidebar.slider(
        "Rango de precio (MXN)",
        float(df_summary["Precio Actual"].min()),
        float(df_summary["Precio Actual"].max()),
        (float(df_summary["Precio Actual"].min()), float(df_summary["Precio Actual"].max()))
    )

    return filters


def render_sort_controls():
    """Renderiza los controles de ordenamiento."""
    sort_options = [
        "Diff % vs Prom (más caros primero)",
        "Diff % vs Prom (más baratos primero)",
        "Precio (más caro → más barato)",
        "Precio (más barato → más caro)",
        "Título (A-Z)",
        "Título (Z-A)",
        "SKU (A-Z)",
        "Competidores (más → menos)",
    ]
    return st.selectbox("📊 Ordenar por", sort_options, index=0)


def render_product_table(df_filtered, display_cols):
    """Renderiza la tabla de productos."""
    st.markdown(f'<div class="section-header">📋 Productos ({len(df_filtered)} filtrados)</div>', unsafe_allow_html=True)

    df_display = df_filtered[display_cols].copy()

    # Links clickeables
    df_display["Link"] = df_display["Link"].apply(
        lambda x: f'<a href="{x}" target="_blank">🔗 Ver producto</a>' if x else ""
    )
    df_display["Link Competidor Más Barato"] = df_display["Link Competidor Más Barato"].apply(
        lambda x: f'<a href="{x}" target="_blank">🔗 Ver competidor</a>' if x else ""
    )

    st.write(df_display.to_html(escape=False, index=False), unsafe_allow_html=True)


def render_excel_download():
    """Renderiza el botón de descarga de Excel."""
    st.markdown('<div class="section-header">📥 Descargar Reporte</div>', unsafe_allow_html=True)

    excel_files = sorted([
        f for f in os.listdir(REPORTS_DIR)
        if f.startswith("ML_Analisis_Mercado_") and f.endswith(".xlsx")
    ], reverse=True)

    if excel_files:
        latest = os.path.join(REPORTS_DIR, excel_files[0])
        with open(latest, "rb") as f:
            st.download_button(
                label=f"📥 Descargar Excel ({excel_files[0]})",
                data=f,
                file_name=excel_files[0],
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
    else:
        st.info("No hay archivos Excel disponibles.")


def render_competitor_detail(df_filtered):
    """Renderiza la sección de detalle de competidores."""
    st.markdown('<div class="section-header">🔍 Detalle de Competidores por Producto</div>', unsafe_allow_html=True)

    if df_filtered.empty:
        st.info("No hay productos para mostrar.")
        return

    sorted_items = df_filtered.sort_values("Precio Actual", ascending=False)
    selected = st.selectbox(
        "Selecciona un producto para ver sus competidores",
        options=sorted_items["Título"].tolist(),
        index=0,
    )

    item_id = df_filtered[df_filtered["Título"] == selected]["ML_Item_ID"].iloc[0]
    item_data = df_filtered[df_filtered["ML_Item_ID"] == item_id].iloc[0]

    # Info del producto
    st.markdown(f'''
    <div class="competitor-box">
        <h4>📦 {item_data["Título"][:80]}</h4>
        <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
            <div><strong>SKU:</strong> {item_data.get("SKU", "N/A")}</div>
            <div><strong>Catálogo ML:</strong> {item_data["Catálogo ML"]}</div>
            <div><strong>Método:</strong> {item_data["Método"]}</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    cols = st.columns(4)
    with cols[0]:
        st.metric("💰 Precio Actual", f"${item_data['Precio Actual']}")
    with cols[1]:
        orig = item_data.get("Precio Original", "—")
        if orig != "—":
            st.metric("🏷️ Precio Original", f"${orig}")
        else:
            st.metric("🏷️ Precio Original", "Sin descuento")
    with cols[2]:
        st.metric("📊 Posición", item_data["Posición"])
    with cols[3]:
        st.metric("🏆 Competidores", f"{item_data['Competidores']}")

    return item_data


def render_footer():
    """Renderiza el footer."""
    st.markdown('''
    <div class="footer">
        <p>📊 MOREKA SHOP — Análisis de Mercado v1.0</p>
        <p>Datos actualizados periódicamente vía API de Mercado Libre</p>
    </div>
    ''', unsafe_allow_html=True)
