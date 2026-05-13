#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dashboard de Análisis de Mercado - MOREKA SHOP
Streamlit App con diseño azul/blanco elegante
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# ─── Configuración de página ───
st.set_page_config(
    page_title="MOREKA SHOP — Análisis de Mercado",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Paths ───
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_FILE = os.path.join(BASE_DIR, "market_cache.json")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

# ─── Estilos CSS Azul/Blanco ───
st.markdown("""
<style>
    /* ===== Global ===== */
    .main { background-color: #f8fafc !important; }
    
    /* ===== Header ===== */
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 0.3rem;
        letter-spacing: -0.02em;
    }
    .sub-header {
        font-size: 0.95rem;
        color: #64748b;
        margin-bottom: 1.5rem;
        font-weight: 400;
    }
    .header-bar {
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 50%, #3b82f6 100%);
        border-radius: 12px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        color: white;
        box-shadow: 0 4px 20px rgba(37, 99, 235, 0.25);
    }
    .header-bar h1 {
        margin: 0;
        font-size: 1.6rem;
        font-weight: 700;
    }
    .header-bar p {
        margin: 0.3rem 0 0 0;
        opacity: 0.85;
        font-size: 0.9rem;
    }
    
    /* ===== Metric Cards ===== */
    .metric-row {
        display: flex;
        gap: 0.75rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 1.2rem;
        text-align: center;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        flex: 1;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.12);
    }
    .metric-number {
        font-size: 1.8rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
    .metric-label {
        font-size: 0.78rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }
    
    /* Position colors */
    .pos-green .metric-number { color: #059669; }
    .pos-green .metric-label { color: #047857; }
    .pos-green { border-top: 3px solid #059669; }
    
    .pos-yellow .metric-number { color: #ca8a04; }
    .pos-yellow .metric-label { color: #a16207; }
    .pos-yellow { border-top: 3px solid #eab308; }
    
    .pos-gray .metric-number { color: #64748b; }
    .pos-gray .metric-label { color: #475569; }
    .pos-gray { border-top: 3px solid #94a3b8; }
    
    .pos-orange .metric-number { color: #ea580c; }
    .pos-orange .metric-label { color: #c2410c; }
    .pos-orange { border-top: 3px solid #f97316; }
    
    .pos-red .metric-number { color: #dc2626; }
    .pos-red .metric-label { color: #b91c1c; }
    .pos-red { border-top: 3px solid #ef4444; }
    
    /* ===== Section Headers ===== */
    .section-header {
        color: #1e3a8a;
        font-size: 1.15rem;
        font-weight: 700;
        margin: 1.5rem 0 0.8rem 0;
        padding-bottom: 0.4rem;
        border-bottom: 2px solid #e2e8f0;
    }
    
    /* ===== Tables ===== */
    .stDataFrame { font-size: 0.82rem; }
    
    /* ===== Sidebar ===== */
    [data-testid="stSidebar"] {
        background-color: #f1f5f9 !important;
        border-right: 1px solid #e2e8f0;
    }
    [data-testid="stSidebar"] h2 {
        color: #1e3a8a !important;
    }
    
    /* ===== Links ===== */
    a { color: #2563eb !important; text-decoration: none !important; }
    a:hover { color: #1d4ed8 !important; text-decoration: underline !important; }
    
    /* ===== Competitor Detail Box ===== */
    .competitor-box {
        background: white;
        border-radius: 12px;
        padding: 1.2rem;
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }
    .competitor-box h4 {
        color: #1e3a8a;
        margin: 0 0 0.5rem 0;
        font-size: 0.95rem;
    }
    
    /* ===== Footer ===== */
    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 0.78rem;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #e2e8f0;
    }
    
    /* ===== Scrollbar ===== */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #f1f5f9; }
    ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
</style>
""", unsafe_allow_html=True)

# ─── Funciones ───
def load_cache():
    if not os.path.exists(CACHE_FILE):
        return None
    try:
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    except:
        return None

def load_data():
    cache = load_cache()
    if not cache:
        return None, None, None, None, None
    
    data = cache.get("data", [])
    
    summary_rows = []
    competitor_rows = []
    position_counts = {}
    no_catalog_rows = []
    
    for entry in data:
        item = entry["item"]
        analysis = entry.get("analysis")
        source = entry.get("source", "Desconocido")
        
        cheapest_link = ""
        if analysis:
            # Get permalink of cheapest competitor
            top5 = analysis.get("top_5", [])
            if top5:
                cheapest_comp = min(top5, key=lambda x: x.get("price", float('inf')))
                cheapest_link = cheapest_comp.get("permalink", "")
        
        row = {
            "SKU": item.get("sku", "N/A"),
            "ML_Item_ID": item["id"],
            "Título": item["title"],
            "Precio Actual": item["price"],
            "% Descuento": f"{item.get('discount_pct', 0)}%" if item.get('discount_pct', 0) > 0 else "—",
            "Precio Original": item.get('original_price') if item.get('discount_pct', 0) > 0 else "—",
            "Catálogo ML": "Sí" if item.get("catalog_product_id") else "No",
            "Método": source,
            "Competidores": analysis["comp_count"] if analysis else 0,
            "Precio Mín": analysis["min_price"] if analysis else None,
            "Precio Máx": analysis["max_price"] if analysis else None,
            "Precio Prom": analysis["avg_price"] if analysis else None,
            "Diff vs Mín": analysis["diff_vs_min"] if analysis else None,
            "Diff % vs Mín": analysis["diff_pct_min"] if analysis else None,
            "Diff vs Prom": analysis["diff_vs_avg"] if analysis else None,
            "Diff % vs Prom": analysis["diff_pct_avg"] if analysis else None,
            "Posición": analysis["position"] if analysis else "Sin datos",
            "Vendedor Más Barato": analysis["cheapest_seller"] if analysis else None,
            "Precio Más Barato": analysis["cheapest_price"] if analysis else None,
            "Link Competidor Más Barato": cheapest_link,
            "Mejor Vendedor": analysis["best_seller_id"] if analysis else None,
            "Ventas Mejor": analysis["best_seller_qty"] if analysis else None,
            "Categoría": item.get("category_id", ""),
            "Vendidos": item.get("sold_quantity", 0),
            "Stock": item.get("available_quantity", 0),
            "Link": item.get("permalink", "")
        }
        summary_rows.append(row)
        
        if analysis and analysis.get("top_5"):
            for idx, comp in enumerate(analysis["top_5"], 1):
                competitor_rows.append({
                    "SKU Nuestro": item.get("sku", "N/A"),
                    "ML_Item_ID": item["id"],
                    "Título Nuestro": item["title"],
                    "Nuestro Precio": item["price"],
                    "Método": source,
                    "Ranking": idx,
                    "Vendedor": comp["seller_id"],
                    "Precio Competidor": comp["price"],
                    "Diferencia": item["price"] - comp["price"],
                    "Diferencia %": round(((item["price"] - comp["price"]) / comp["price"] * 100), 1) if comp["price"] > 0 else 0,
                    "Vendidos": comp.get("sold_quantity", 0),
                    "Stock": comp.get("available_quantity", 0),
                    "Envío Gratis": "Sí" if comp.get("shipping_free") else "No",
                    "Link": comp.get("permalink", "")
                })
        
        if analysis:
            pos = analysis["position"]
            position_counts[pos] = position_counts.get(pos, 0) + 1
        
        if not item.get("catalog_product_id"):
            no_catalog_rows.append({
                "SKU": item.get("sku", "N/A"),
                "ML_Item_ID": item["id"],
                "Título": item["title"],
                "Precio": item["price"],
                "Categoría": item.get("category_id", ""),
                "Vendidos": item.get("sold_quantity", 0),
                "Stock": item.get("available_quantity", 0),
                "Competencia Encontrada": "Sí" if analysis else "No",
                "Método": source,
                "Link": item.get("permalink", "")
            })
    
    df_summary = pd.DataFrame(summary_rows)
    df_competitors = pd.DataFrame(competitor_rows)
    df_positions = pd.DataFrame([
        {"Posición": k, "Cantidad": v}
        for k, v in sorted(position_counts.items(), key=lambda x: x[1], reverse=True)
    ])
    df_no_catalog = pd.DataFrame(no_catalog_rows)
    
    return df_summary, df_competitors, df_positions, df_no_catalog, cache

def get_position_color(pos):
    if "🟢" in pos: return "green"
    elif "🔴" in pos: return "red"
    elif "🟡" in pos: return "yellow"
    elif "🟠" in pos: return "orange"
    return "gray"

# ═══════════════════════════════════════
# HEADER
# ═══════════════════════════════════════
st.markdown('''
<div class="header-bar">
    <h1>📊 MOREKA SHOP — Análisis de Mercado</h1>
    <p>Comparación de precios vs competencia en Mercado Libre México</p>
</div>
''', unsafe_allow_html=True)

# ─── LOAD DATA ───
df_summary, df_competitors, df_positions, df_no_catalog, cache = load_data()

if df_summary is None:
    st.error("❌ No hay datos de análisis disponibles. Ejecuta `analisis_mercado_completo.py` primero.")
    st.info("""
    **Para generar datos:**
    1. Ve a la terminal
    2. Corre: `python3 analisis_mercado_completo.py`
    3. Espera a que termine (puede tardar 30-40 minutos para 364 productos)
    4. Refresca esta página
    """)
    st.stop()

# ─── SIDEBAR FILTROS ───
st.sidebar.header("🔍 Filtros")

positions = ["Todas"] + sorted(df_summary["Posición"].dropna().unique().tolist())
selected_position = st.sidebar.selectbox("Posición en mercado", positions)

catalog_options = ["Todos", "Con Catálogo ML", "Sin Catálogo ML"]
selected_catalog = st.sidebar.selectbox("Tipo de catálogo", catalog_options)

methods = ["Todos"] + sorted(df_summary["Método"].dropna().unique().tolist())
selected_method = st.sidebar.selectbox("Método de análisis", methods)

categories = ["Todas"] + sorted(df_summary["Categoría"].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("Categoría ML", categories)

sku_search = st.sidebar.text_input("Buscar por SKU o título")

price_range = st.sidebar.slider(
    "Rango de precio (MXN)",
    float(df_summary["Precio Actual"].min()),
    float(df_summary["Precio Actual"].max()),
    (float(df_summary["Precio Actual"].min()), float(df_summary["Precio Actual"].max()))
)

# ─── Aplicar filtros ───
df_filtered = df_summary.copy()

if selected_position != "Todas":
    df_filtered = df_filtered[df_filtered["Posición"] == selected_position]

if selected_catalog == "Con Catálogo ML":
    df_filtered = df_filtered[df_filtered["Catálogo ML"] == "Sí"]
elif selected_catalog == "Sin Catálogo ML":
    df_filtered = df_filtered[df_filtered["Catálogo ML"] == "No"]

if selected_method != "Todos":
    df_filtered = df_filtered[df_filtered["Método"] == selected_method]

if selected_category != "Todas":
    df_filtered = df_filtered[df_filtered["Categoría"] == selected_category]

if sku_search:
    mask = df_filtered["SKU"].str.contains(sku_search, case=False, na=False) | \
           df_filtered["Título"].str.contains(sku_search, case=False, na=False) | \
           df_filtered["ML_Item_ID"].str.contains(sku_search, case=False, na=False)
    df_filtered = df_filtered[mask]

df_filtered = df_filtered[
    (df_filtered["Precio Actual"] >= price_range[0]) & 
    (df_filtered["Precio Actual"] <= price_range[1])
]

# ═══════════════════════════════════════
# INFO BAR
# ═══════════════════════════════════════
timestamp = cache.get("timestamp", "Desconocido") if cache else "Desconocido"

with_comp = len(df_summary[df_summary["Competidores"] > 0])
without_comp = len(df_summary) - with_comp

st.markdown('''
<div style="display: flex; gap: 1rem; margin-bottom: 1rem;">
    <div style="background: white; border-radius: 8px; padding: 0.8rem 1.2rem; border: 1px solid #e2e8f0; flex: 1; text-align: center;">
        <div style="font-size: 1.4rem; font-weight: 800; color: #1e3a8a;">''' + str(len(df_summary)) + '''</div>
        <div style="font-size: 0.75rem; color: #64748b; text-transform: uppercase;">Total Productos</div>
    </div>
    <div style="background: white; border-radius: 8px; padding: 0.8rem 1.2rem; border: 1px solid #e2e8f0; flex: 1; text-align: center;">
        <div style="font-size: 1.4rem; font-weight: 800; color: #2563eb;">''' + str(with_comp) + ''' <span style="font-size: 0.85rem; font-weight: 500;">(''' + str(round(with_comp/len(df_summary)*100)) + '''%)</span></div>
        <div style="font-size: 0.75rem; color: #64748b; text-transform: uppercase;">Con Competencia</div>
    </div>
    <div style="background: white; border-radius: 8px; padding: 0.8rem 1.2rem; border: 1px solid #e2e8f0; flex: 1; text-align: center;">
        <div style="font-size: 1.4rem; font-weight: 800; color: #64748b;">''' + str(without_comp) + '''</div>
        <div style="font-size: 0.75rem; color: #64748b; text-transform: uppercase;">Sin Competencia</div>
    </div>
    <div style="background: white; border-radius: 8px; padding: 0.8rem 1.2rem; border: 1px solid #e2e8f0; flex: 1; text-align: center;">
        <div style="font-size: 1.1rem; font-weight: 700; color: #1e3a8a;">''' + (timestamp[:16] if timestamp != "Desconocido" else "N/A") + '''</div>
        <div style="font-size: 0.75rem; color: #64748b; text-transform: uppercase;">Última Actualización</div>
    </div>
</div>
''', unsafe_allow_html=True)

# ═══════════════════════════════════════
# MÉTRICAS POR POSICIÓN
# ═══════════════════════════════════════
st.markdown('<div class="section-header">📈 Distribución de Posiciones</div>', unsafe_allow_html=True)

pos_counts = df_summary["Posición"].value_counts()

cols = st.columns(5)
positions_config = [
    ("🟢 Más barato", "pos-green", pos_counts.get("🟢 Más barato", 0)),
    ("🟡 Bajo promedio", "pos-yellow", pos_counts.get("🟡 Bajo promedio", 0)),
    ("⚪ En promedio", "pos-gray", pos_counts.get("⚪ En promedio", 0)),
    ("🟠 Sobre promedio", "pos-orange", pos_counts.get("🟠 Sobre promedio", 0)),
    ("🔴 Más caro", "pos-red", pos_counts.get("🔴 Más caro", 0)),
]

for i, (label, css_class, count) in enumerate(positions_config):
    with cols[i]:
        st.markdown(f'''
        <div class="metric-card {css_class}">
            <div class="metric-number">{count}</div>
            <div class="metric-label">{label}</div>
        </div>
        ''', unsafe_allow_html=True)

# ═══════════════════════════════════════
# GRÁFICOS
# ═══════════════════════════════════════
st.markdown('<div class="section-header">📊 Visualización</div>', unsafe_allow_html=True)

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    if not df_positions.empty:
        fig = px.pie(
            df_positions, 
            values="Cantidad", 
            names="Posición",
            color="Posición",
            color_discrete_map={
                "🟢 Más barato": "#059669",
                "🟡 Bajo promedio": "#eab308",
                "⚪ En promedio": "#94a3b8",
                "🟠 Sobre promedio": "#f97316",
                "🔴 Más caro": "#dc2626",
            },
            hole=0.55
        )
        fig.update_layout(
            height=380,
            font=dict(family="Inter, sans-serif", size=12),
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
            margin=dict(t=20, b=20, l=20, r=20)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Sin datos de posiciones")

with col_chart2:
    df_with_analysis = df_summary[df_summary["Diff % vs Prom"].notna()].copy()
    if not df_with_analysis.empty:
        fig2 = px.histogram(
            df_with_analysis,
            x="Diff % vs Prom",
            nbins=30,
            color_discrete_sequence=["#2563eb"],
            labels={"Diff % vs Prom": "Diferencia % vs Promedio de Mercado"}
        )
        fig2.add_vline(x=0, line_dash="dash", line_color="#ef4444", line_width=2,
                       annotation_text="Promedio del mercado", annotation_position="top")
        fig2.update_layout(
            height=380,
            font=dict(family="Inter, sans-serif"),
            xaxis_title="Diferencia % vs Promedio",
            yaxis_title="Cantidad de Productos",
            margin=dict(t=20, b=20, l=20, r=20)
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Sin datos de diferencia vs promedio")

# ═══════════════════════════════════════
# TABLA DE PRODUCTOS
# ═══════════════════════════════════════
st.markdown(f'<div class="section-header">📋 Productos ({len(df_filtered)} filtrados de {len(df_summary)})</div>', unsafe_allow_html=True)

# Ordenamiento
sort_col1, sort_col2 = st.columns([1, 1])
with sort_col1:
    sort_by = st.selectbox(
        "📊 Ordenar por",
        ["Diff % vs Prom (más caros primero)", "Diff % vs Prom (más baratos primero)", 
         "Precio (más caro → más barato)", "Precio (más barato → más caro)",
         "Título (A-Z)", "Título (Z-A)", "SKU (A-Z)", "Competidores (más → menos)"],
        index=0
    )
with sort_col2:
    pass  # placeholder for layout balance

display_cols = [
    "SKU", "Título", "Precio Actual", "Precio Original", "% Descuento", "Catálogo ML", "Método", 
    "Competidores", "Precio Mín", "Precio Máx", "Precio Prom",
    "Diff % vs Prom", "Posición", "Vendedor Más Barato", 
    "Precio Más Barato", "Link Competidor Más Barato",
    "Ventas Mejor", "Link"
]

df_display = df_filtered[display_cols].copy()

# Links clickeables
df_display["Link"] = df_display["Link"].apply(
    lambda x: f'<a href="{x}" target="_blank" title="Ver en Mercado Libre">🔗 Ver producto</a>' if x else ""
)
df_display["Link Competidor Más Barato"] = df_display["Link Competidor Más Barato"].apply(
    lambda x: f'<a href="{x}" target="_blank" title="Ver competidor más barato">🔗 Ver competidor</a>' if x else ""
)

# Aplicar ordenamiento según selección
if sort_by == "Diff % vs Prom (más caros primero)":
    df_display = df_display.sort_values("Diff % vs Prom", ascending=False, na_position="last")
elif sort_by == "Diff % vs Prom (más baratos primero)":
    df_display = df_display.sort_values("Diff % vs Prom", ascending=True, na_position="last")
elif sort_by == "Precio (más caro → más barato)":
    df_display = df_display.sort_values("Precio Actual", ascending=False, na_position="last")
elif sort_by == "Precio (más barato → más caro)":
    df_display = df_display.sort_values("Precio Actual", ascending=True, na_position="last")
elif sort_by == "Título (A-Z)":
    df_display = df_display.sort_values("Título", ascending=True, na_position="last")
elif sort_by == "Título (Z-A)":
    df_display = df_display.sort_values("Título", ascending=False, na_position="last")
elif sort_by == "SKU (A-Z)":
    df_display = df_display.sort_values("SKU", ascending=True, na_position="last")
elif sort_by == "Competidores (más → menos)":
    df_display = df_display.sort_values("Competidores", ascending=False, na_position="last")

st.write(df_display.to_html(escape=False, index=False), unsafe_allow_html=True)

# ═══════════════════════════════════════
# DESCARGAR EXCEL
# ═══════════════════════════════════════
st.markdown('<div class="section-header">📥 Descargar Reporte</div>', unsafe_allow_html=True)

excel_files = sorted([
    f for f in os.listdir(REPORTS_DIR) 
    if f.startswith("ML_Analisis_Mercado_") and f.endswith(".xlsx")
], reverse=True)

if excel_files:
    latest_excel = os.path.join(REPORTS_DIR, excel_files[0])
    with open(latest_excel, "rb") as f:
        st.download_button(
            label=f"📥 Descargar Excel ({excel_files[0]})",
            data=f,
            file_name=excel_files[0],
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
else:
    st.info("No hay archivos Excel disponibles. Ejecuta el análisis primero.")

# ═══════════════════════════════════════
# DETALLE DE COMPETIDORES
# ═══════════════════════════════════════
st.markdown('<div class="section-header">🔍 Detalle de Competidores por Producto</div>', unsafe_allow_html=True)

if not df_filtered.empty:
    # Opciones ordenadas por precio más alto (los más caros primero para revisión)
    sorted_items = df_filtered.sort_values("Precio", ascending=False)
    
    selected_item = st.selectbox(
        "Selecciona un producto para ver sus competidores",
        options=sorted_items["Título"].tolist(),
        index=0
    )
    
    item_id = df_filtered[df_filtered["Título"] == selected_item]["ML_Item_ID"].iloc[0]
    item_data = df_filtered[df_filtered["ML_Item_ID"] == item_id].iloc[0]
    
    # Producto info
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
    
    col_item1, col_item2, col_item3, col_item4 = st.columns(4)
    with col_item1:
        st.metric("💰 Precio Actual", f"${item_data['Precio Actual']}")
    with col_item2:
        orig_price = item_data.get('Precio Original', '—')
        if orig_price != '—':
            st.metric("🏷️ Precio Original", f"${orig_price}")
        else:
            st.metric("🏷️ Precio Original", "Sin descuento")
    with col_item3:
        min_price = item_data['Precio Mín']
        st.metric("📉 Precio Mín Competencia", f"${min_price}" if pd.notna(min_price) else "N/A")
    with col_item4:
        st.metric("🏆 Posición", item_data['Posición'])
    
    # Link al competidor más barato
    cheapest_link = item_data.get("Link Competidor Más Barato", "")
    if cheapest_link:
        st.markdown(f'''
        <div style="background: #eff6ff; border-left: 4px solid #2563eb; padding: 0.8rem 1rem; border-radius: 0 8px 8px 0; margin: 0.5rem 0;">
            🔗 <strong>Competidor más barato:</strong> 
            <a href="{cheapest_link}" target="_blank" style="color: #2563eb; font-weight: 600;">
                Ver en Mercado Libre →
            </a>
        </div>
        ''', unsafe_allow_html=True)
    
    # Competidores tabla
    item_competitors = df_competitors[df_competitors["ML_Item_ID"] == item_id].copy()
    
    if not item_competitors.empty:
        st.markdown(f'<div style="color: #1e3a8a; font-weight: 600; margin: 1rem 0 0.5rem 0;">Top {len(item_competitors)} Competidores</div>', unsafe_allow_html=True)
        
        # Gráfico comparativo
        fig_comp = go.Figure()
        
        comp_sorted = item_competitors.sort_values("Precio Competidor")
        all_sellers = ["Nosotros"] + comp_sorted["Vendedor"].tolist()
        all_prices = [item_data["Precio Actual"]] + comp_sorted["Precio Competidor"].tolist()
        colors = ["#1e3a8a"] + ["#60a5fa"] * len(comp_sorted)
        
        fig_comp.add_trace(go.Bar(
            x=all_sellers,
            y=all_prices,
            marker_color=colors,
            text=[f"${p}" for p in all_prices],
            textposition="outside",
            textfont=dict(size=11, color="#1e3a8a")
        ))
        
        fig_comp.update_layout(
            height=350,
            title=dict(
                text="Comparación de Precios",
                font=dict(size=14, color="#1e3a8a"),
                x=0.5
            ),
            xaxis_title="Vendedor",
            yaxis_title="Precio (MXN)",
            font=dict(family="Inter, sans-serif", color="#334155"),
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(t=50, b=20, l=20, r=20),
            showlegend=False
        )
        fig_comp.update_xaxes(tickangle=-30)
        st.plotly_chart(fig_comp, use_container_width=True)
        
        # Ordenamiento competidores
        sort_comp = st.selectbox(
            "📊 Ordenar competidores por",
            ["Ranking (más barato primero)", "Precio (más caro primero)", "Vendidos (más → menos)"],
            index=0,
            key="sort_comp"
        )
        
        # Tabla competidores
        comp_display = item_competitors[[
            "Ranking", "Vendedor", "Precio Competidor", "Diferencia", 
            "Diferencia %", "Vendidos", "Stock", "Envío Gratis", "Link"
        ]].copy()
        
        # Aplicar ordenamiento
        if sort_comp == "Ranking (más barato primero)":
            comp_display = comp_display.sort_values("Ranking", ascending=True)
        elif sort_comp == "Precio (más caro primero)":
            comp_display = comp_display.sort_values("Precio Competidor", ascending=False)
        elif sort_comp == "Vendidos (más → menos)":
            comp_display = comp_display.sort_values("Vendidos", ascending=False)
        
        comp_display["Link"] = comp_display["Link"].apply(
            lambda x: f'<a href="{x}" target="_blank" title="Ver producto del competidor">🔗 Ver</a>' if x else ""
        )
        st.write(comp_display.to_html(escape=False, index=False), unsafe_allow_html=True)
    else:
        st.info("No hay datos de competidores para este producto")

# ═══════════════════════════════════════
# PRODUCTOS SIN CATÁLOGO
# ═══════════════════════════════════════
st.markdown(f'<div class="section-header">📦 Productos Sin Catálogo ML ({len(df_no_catalog)})</div>', unsafe_allow_html=True)

if not df_no_catalog.empty:
    st.markdown('''
    <div style="background: #fffbeb; border-left: 4px solid #f59e0b; padding: 0.8rem 1rem; border-radius: 0 8px 8px 0; margin-bottom: 1rem; color: #92400e; font-size: 0.9rem;">
        💡 <strong>Recomendación:</strong> Registrar estos productos en el catálogo oficial de Mercado Libre permite comparación de precios más precisa, mayor visibilidad en búsquedas y acceso a "Price to Win".
    </div>
    ''', unsafe_allow_html=True)
    
    # Ordenamiento sin catálogo
    sort_nc = st.selectbox(
        "📊 Ordenar sin catálogo por",
        ["Precio (más caro primero)", "Precio (más barato primero)", "Título (A-Z)", "Título (Z-A)", "SKU (A-Z)", "Vendidos (más → menos)"],
        index=0,
        key="sort_nc"
    )
    
    no_catalog_display = df_no_catalog[[
        "SKU", "Título", "Precio", "Categoría", "Vendidos", 
        "Stock", "Competencia Encontrada", "Método", "Link"
    ]].copy()
    
    # Aplicar ordenamiento
    if sort_nc == "Precio (más caro primero)":
        no_catalog_display = no_catalog_display.sort_values("Precio", ascending=False)
    elif sort_nc == "Precio (más barato primero)":
        no_catalog_display = no_catalog_display.sort_values("Precio", ascending=True)
    elif sort_nc == "Título (A-Z)":
        no_catalog_display = no_catalog_display.sort_values("Título", ascending=True)
    elif sort_nc == "Título (Z-A)":
        no_catalog_display = no_catalog_display.sort_values("Título", ascending=False)
    elif sort_nc == "SKU (A-Z)":
        no_catalog_display = no_catalog_display.sort_values("SKU", ascending=True)
    elif sort_nc == "Vendidos (más → menos)":
        no_catalog_display = no_catalog_display.sort_values("Vendidos", ascending=False)
    
    no_catalog_display["Link"] = no_catalog_display["Link"].apply(
        lambda x: f'<a href="{x}" target="_blank">🔗 Ver</a>' if x else ""
    )
    st.write(no_catalog_display.to_html(escape=False, index=False), unsafe_allow_html=True)
else:
    st.success("✅ Todos los productos están en el catálogo ML")

# ═══════════════════════════════════════
# ACTUALIZAR
# ═══════════════════════════════════════
st.markdown('<div class="section-header">🔄 Actualizar Datos</div>', unsafe_allow_html=True)

st.markdown('''
<div style="background: white; border: 1px solid #e2e8f0; border-radius: 10px; padding: 1rem;">
    <p style="margin: 0 0 0.5rem 0; color: #475569;">
        El análisis se actualiza automáticamente cada <strong>3 días</strong> vía cron job (7:00 AM).
    </p>
    <p style="margin: 0; color: #64748b; font-size: 0.85rem;">
        Para actualizar manualmente, ejecuta en terminal:<br>
        <code style="background: #f1f5f9; padding: 0.2rem 0.4rem; border-radius: 4px;">
            cd /root/.openclaw/workspace/mercadolibre-sales && python3 analisis_mercado_completo.py
        </code>
    </p>
</div>
''', unsafe_allow_html=True)

# ═══════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════
st.markdown('''
<div class="footer">
    <strong>MOREKA SHOP Analytics</strong> · Mercado Libre México · 
    Generado: ''' + datetime.now().strftime('%Y-%m-%d %H:%M') + '''
</div>
''', unsafe_allow_html=True)
