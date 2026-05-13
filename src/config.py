#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Configuración global del dashboard."""

import os

# ─── Paths ───
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_FILE = os.path.join(BASE_DIR, "data", "market_cache.json")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
DOCS_DIR = os.path.join(BASE_DIR, "docs")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# ─── App Config ───
PAGE_TITLE = "MOREKA SHOP — Análisis de Mercado"
PAGE_ICON = "📊"

# ─── Colores ───
COLORS = {
    "primary": "#1e3a8a",
    "secondary": "#2563eb",
    "accent": "#3b82f6",
    "success": "#059669",
    "warning": "#ca8a04",
    "danger": "#dc2626",
    "info": "#64748b",
    "bg": "#f8fafc",
    "card": "#ffffff",
    "border": "#e2e8f0",
    "text": "#0f172a",
    "text_muted": "#64748b",
}

# ─── Posiciones ───
POSITIONS = [
    ("🟢 Más barato", "pos-green", "#059669"),
    ("🟡 Bajo promedio", "pos-yellow", "#ca8a04"),
    ("⚪ En promedio", "pos-gray", "#64748b"),
    ("🟠 Sobre promedio", "pos-orange", "#ea580c"),
    ("🔴 Más caro", "pos-red", "#dc2626"),
]

# ─── Display columns ───
DISPLAY_COLS = [
    "SKU", "Título", "Precio Actual", "Precio Original", "% Descuento",
    "Catálogo ML", "Método", "Competidores", "Precio Mín", "Precio Máx",
    "Precio Prom", "Diff % vs Prom", "Posición", "Vendedor Más Barato",
    "Precio Más Barato", "Link Competidor Más Barato", "Ventas Mejor", "Link",
]
