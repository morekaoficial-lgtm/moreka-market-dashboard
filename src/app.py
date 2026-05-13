#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dashboard de Análisis de Mercado - MOREKA SHOP
App principal - Streamlit Cloud
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from src.config import PAGE_TITLE, PAGE_ICON, DISPLAY_COLS
from src.styles import load_css
from src.data_loader import load_data, apply_filters, sort_dataframe
from src.components import (
    render_header,
    render_info_bar,
    render_metrics,
    render_position_metrics,
    render_sidebar_filters,
    render_sort_controls,
    render_product_table,
    render_excel_download,
    render_competitor_detail,
    render_footer,
)
from src.charts import render_pie_chart, render_histogram

# ─── Configuración de página ───
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Cargar estilos ───
load_css()

# ─── Header ───
render_header()

# ─── Cargar datos ───
df_summary, df_competitors, df_positions, df_no_catalog, cache = load_data()

if df_summary is None:
    st.error("❌ No hay datos de análisis disponibles.")
    st.info("Ejecuta `python3 analisis_mercado_completo.py` para generar datos.")
    st.stop()

# ─── Métricas superiores ───
with_comp = len(df_summary[df_summary["Competidores"] > 0])
without_comp = len(df_summary) - with_comp
timestamp = cache.get("timestamp", "Desconocido") if cache else "Desconocido"

render_info_bar(df_summary, with_comp, without_comp, timestamp)

# ─── Métricas principales ───
render_metrics(df_summary)

# ─── Métricas por posición ───
pos_counts = df_summary["Posición"].value_counts().to_dict()
render_position_metrics(pos_counts)

# ─── Gráficos ───
st.markdown('<div class="section-header">📊 Visualización</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    render_pie_chart(df_positions)
with col2:
    render_histogram(df_summary)

# ─── Filtros ───
st.sidebar.markdown("---")
st.sidebar.markdown("### 📋 Resumen")
st.sidebar.markdown(f"**Total:** {len(df_summary)} productos")
st.sidebar.markdown(f"**Con competencia:** {with_comp}")
st.sidebar.markdown(f"**Sin competencia:** {without_comp}")

filters = render_sidebar_filters(df_summary)

# ─── Aplicar filtros y ordenamiento ───
df_filtered = apply_filters(df_summary, filters)

# Ordenamiento
sort_col1, sort_col2 = st.columns([1, 1])
with sort_col1:
    sort_by = render_sort_controls()
with sort_col2:
    pass

df_filtered = sort_dataframe(df_filtered, sort_by)

# ─── Tabla de productos ───
render_product_table(df_filtered, DISPLAY_COLS)

# ─── Descargar Excel ───
render_excel_download()

# ─── Detalle de competidores ───
render_competitor_detail(df_filtered)

# ─── Footer ───
render_footer()
