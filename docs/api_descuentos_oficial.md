# 📚 Documentación Oficial: Descuentos en API de Mercado Libre

## Fuente Oficial
**URL:** https://developers.mercadolibre.com.ar/es_ar/items-y-busquedas  
**Endpoint:** `GET /items/{item_id}`  
**Fecha de consulta:** Mayo 2026

---

## 🔍 Endpoint para obtener datos de un item

```bash
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' \
  https://api.mercadolibre.com/items/{item_id}
```

---

## 📋 Campos relevantes para descuentos

Según la documentación oficial de Mercado Libre, la respuesta JSON del endpoint `/items/{item_id}` incluye estos campos clave:

| Campo | Tipo | Descripción Oficial |
|-------|------|---------------------|
| **`price`** | number | **Precio actual del item** — Es el precio que el comprador paga finalmente. Si hay descuento, este es el precio con descuento aplicado. |
| **`original_price`** | number\|null | **Precio original** — Es el precio antes del descuento. Aparece `null` cuando el item **no tiene descuento activo**. Es el precio que aparece tachado en la web de ML. |
| **`base_price`** | number | Precio base del item. No siempre refleja el descuento. |

---

## 📝 Ejemplo de respuesta de la API (documentación oficial)

```json
{
  "id": "MLA599260060",
  "site_id": "MLA",
  "title": "Item De Test - Por Favor No Ofertar",
  "subtitle": null,
  "seller_id": 303888594,
  "category_id": "MLA401685",
  "official_store_id": null,
  **"price": 130,**
  **"base_price": 130,**
  **"original_price": null,**
  "currency_id": "ARS",
  "initial_quantity": 1,
  "available_quantity": 1,
  "sale_terms": [],
  [...]
}
```

**Nota:** En este ejemplo de la documentación oficial, `original_price` es `null` porque el item **no tiene descuento**.

---

## 🧮 Fórmula del descuento

La documentación no proporciona una fórmula explícita, pero el cálculo estándar es:

```
descuento % = ((original_price - price) / original_price) × 100
```

---

## ✅ Implementación en nuestro código

En `analisis_mercado_completo.py` (línea ~86):

```python
"discount_pct": round(
    (body.get("original_price", body.get("price", 0)) - body.get("price", 0)) 
    / body.get("original_price", body.get("price", 1)) * 100, 1
) if body.get("original_price") and body.get("original_price") != body.get("price", 0) else 0,
```

**Lógica:**
1. Si `original_price` existe y es diferente de `price` → hay descuento → calcular porcentaje
2. Si `original_price` es `null` o igual a `price` → no hay descuento → 0%

---

## 🎯 Ejemplo real de MOREKA SHOP

### Bocina Bluetooth M-337
```json
{
  "price": 274,
  "original_price": 670,
  "base_price": 670
}
```

**Cálculo:** `((670 - 274) / 670) × 100 = 59.1%` ✅

### Producto SIN descuento
```json
{
  "price": 1100,
  "original_price": null,
  "base_price": 1100
}
```

**Resultado:** `discount_pct = 0` (no hay descuento) ✅

---

## 📌 Referencias

1. **Documentación oficial de Items:** https://developers.mercadolibre.com.ar/es_ar/items-y-busquedas
2. **Endpoint de detalle:** `GET https://api.mercadolibre.com/items/{item_id}`
3. **Campo `original_price`:** Documentado como precio antes del descuento, `null` cuando no aplica

---

*Documento generado para MOREKA SHOP — Análisis de Mercado*
*Mayo 2026*
