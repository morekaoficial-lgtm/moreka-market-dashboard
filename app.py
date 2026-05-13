#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dashboard de Análisis de Mercado - MOREKA SHOP
Punto de entrada para Streamlit Cloud
"""

import sys
import os

# Asegurar que src está en el path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar y ejecutar la app principal
from src.app import *  # noqa: F401,F403
