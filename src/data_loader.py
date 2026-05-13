#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Carga y procesamiento de datos del cache de Mercado Libre."""

import json
import os
import pandas as pd
from src.config import CACHE_FILE


def load_cache():
    """Carga el archivo de cache JSON."""
    if not os.path.exists(CACHE_FILE):
        return None
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def load_data():
    """
    Carga y procesa los datos del cache.
    Retorna: df_summary, df_competitors, df_positions, df_no_catalog, cache
    """
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

        # Link del competidor más barato
        cheapest_link = ""
        if analysis:
            top5 = analysis.get("top_5", [])
            if top5:
                cheapest_comp = min(top5, key=lambda x: x.get("price", float("inf")))
                cheapest_link = cheapest_comp.get("permalink", "")

        row = {
            "SKU": item.get("sku", "N/A"),
            "ML_Item_ID": item["id"],
            "Título": item["title"],
            "Precio Actual": item["price"],
            "% Descuento": f"{item.get('discount_pct', 0)}%" if item.get("discount_pct", 0) > 0 else "—",
            "Precio Original": item.get("original_price") if item.get("discount_pct", 0) > 0 else "—",
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
            "Link": item.get("permalink", ""),
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
                    "Link": comp.get("permalink", ""),
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
                "Link": item.get("permalink", ""),
            })

    df_summary = pd.DataFrame(summary_rows)
    df_competitors = pd.DataFrame(competitor_rows)
    df_positions = pd.DataFrame([
        {"Posición": k, "Cantidad": v}
        for k, v in sorted(position_counts.items(), key=lambda x: x[1], reverse=True)
    ])
    df_no_catalog = pd.DataFrame(no_catalog_rows)

    return df_summary, df_competitors, df_positions, df_no_catalog, cache


def apply_filters(df, filters):
    """Aplica filtros al dataframe."""
    df_filtered = df.copy()

    if filters.get("position") and filters["position"] != "Todas":
        df_filtered = df_filtered[df_filtered["Posición"] == filters["position"]]

    if filters.get("catalog") == "Con Catálogo ML":
        df_filtered = df_filtered[df_filtered["Catálogo ML"] == "Sí"]
    elif filters.get("catalog") == "Sin Catálogo ML":
        df_filtered = df_filtered[df_filtered["Catálogo ML"] == "No"]

    if filters.get("method") and filters["method"] != "Todos":
        df_filtered = df_filtered[df_filtered["Método"] == filters["method"]]

    if filters.get("category") and filters["category"] != "Todas":
        df_filtered = df_filtered[df_filtered["Categoría"] == filters["category"]]

    if filters.get("search"):
        search = filters["search"]
        mask = (
            df_filtered["SKU"].str.contains(search, case=False, na=False) |
            df_filtered["Título"].str.contains(search, case=False, na=False) |
            df_filtered["ML_Item_ID"].str.contains(search, case=False, na=False)
        )
        df_filtered = df_filtered[mask]

    if filters.get("price_range"):
        min_p, max_p = filters["price_range"]
        df_filtered = df_filtered[
            (df_filtered["Precio Actual"] >= min_p) &
            (df_filtered["Precio Actual"] <= max_p)
        ]

    return df_filtered


def sort_dataframe(df, sort_by):
    """Ordena el dataframe según la selección."""
    sort_map = {
        "Diff % vs Prom (más caros primero)": ("Diff % vs Prom", False),
        "Diff % vs Prom (más baratos primero)": ("Diff % vs Prom", True),
        "Precio (más caro → más barato)": ("Precio Actual", False),
        "Precio (más barato → más caro)": ("Precio Actual", True),
        "Título (A-Z)": ("Título", True),
        "Título (Z-A)": ("Título", False),
        "SKU (A-Z)": ("SKU", True),
        "Competidores (más → menos)": ("Competidores", False),
    }
    col, asc = sort_map.get(sort_by, ("Diff % vs Prom", False))
    return df.sort_values(col, ascending=asc, na_position="last")
