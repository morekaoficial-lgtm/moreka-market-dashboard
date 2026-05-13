📊 **De dónde saca la API de Mercado Libre la información del descuento**

La API de Mercado Libre (`GET /items/{item_id}`) devuelve estos campos clave:

| Campo API | Significado | Ejemplo con descuento | Ejemplo sin descuento |
|---|---|---|---|
| **`price`** | **Precio actual** — lo que paga el cliente | `$274` | `$1,100` |
| **`original_price`** | **Precio original** — precio tachado en la web | `$670` | `null` |
| **`base_price`** | Precio base (rara vez usado) | `$670` o `$274` | `$1,100` |

**Fórmula del descuento:**
```
descuento % = ((original_price - price) / original_price) × 100
```

Ejemplo real: Bocina M-337
- Precio original: `$670` ← `original_price`
- Precio actual: `$274` ← `price`
- Descuento: `((670 - 274) / 670) × 100 = 59.1%`

**⚠️ El problema actual:**
En tu app, cuando un producto **NO tiene descuento**, `original_price` viene como `null` en la API. Pero el script guarda `original_price` = `price` como fallback. Entonces la tabla muestra:
- Precio Actual: `$1,100`
- Precio Base: `$1,100` ← **igual que el actual, confuso**
- % Descuento: `—`

Eso hace que parezca que todos los productos tienen dos precios iguales. Voy a arreglar la app para que solo muestre "Precio Original" cuando realmente hay un descuento activo.
