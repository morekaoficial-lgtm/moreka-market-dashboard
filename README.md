# MOREKA SHOP — Dashboard de Análisis de Mercado

Dashboard interactivo de análisis de mercado para Mercado Libre México.

![Dashboard Preview](assets/preview.png)

## 🚀 Deploy

La app está configurada para **Streamlit Cloud**.

**URL:** `https://moreka-market-dashboard.streamlit.app`

## 📁 Estructura del Proyecto

```
moreka-market-dashboard/
├── app.py                    # Punto de entrada (Streamlit Cloud)
├── requirements.txt          # Dependencias
├── README.md                 # Este archivo
├── .gitignore               # Archivos ignorados por git
│
├── src/                      # Código fuente
│   ├── __init__.py
│   ├── app.py               # App principal
│   ├── config.py            # Configuración y constantes
│   ├── styles.py            # Carga de CSS
│   ├── data_loader.py       # Carga y procesamiento de datos
│   ├── components.py        # Componentes reutilizables
│   └── charts.py            # Gráficos y visualizaciones
│
├── data/                     # Datos
│   └── market_cache.json    # Cache de análisis de mercado
│
├── docs/                     # Documentación
│   └── docs_descuento.md    # Documentación de descuentos ML
│
├── assets/                   # Recursos estáticos
│   └── styles.css           # Estilos CSS personalizados
│
└── reports/                  # Reportes generados
    └── *.xlsx               # Archivos Excel exportados
```

## 📊 Datos

- **362 productos** analizados
- **57 productos** con descuento activo
- **Comparación vs competencia** en tiempo real
- **Datos actualizados** periódicamente vía API de Mercado Libre

## 🔧 Campos de API ML para Descuentos

| Campo | Significado |
|-------|-------------|
| `price` | Precio actual (con descuento aplicado) |
| `original_price` | Precio original tachado (`null` si no hay descuento) |
| `base_price` | Precio base (raramente usado) |

**Fórmula:** `((original_price - price) / original_price) × 100`

## 🏃 Desarrollo Local

```bash
# Clonar repositorio
git clone https://github.com/morekaoficial-lgtm/moreka-market-dashboard.git
cd moreka-market-dashboard

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar app
streamlit run app.py
```

## 📝 Requisitos

- Python 3.9+
- Streamlit >= 1.28.0
- Pandas >= 2.0.0
- Plotly >= 5.15.0
- OpenPyXL >= 3.1.0

## 🔄 Actualización de Datos

Para actualizar los datos del análisis:

1. Ejecutar `analisis_mercado_completo.py` en tu entorno local
2. El script genera `market_cache.json` con los datos actualizados
3. Copiar el archivo a la carpeta `data/`
4. Commit y push a GitHub
5. Streamlit Cloud redeploya automáticamente

## 📞 Soporte

MOREKA SHOP — Análisis de Mercado v1.0
