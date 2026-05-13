#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Carga de estilos CSS."""

import os
import streamlit as st


def load_css():
    """Carga los estilos CSS desde assets/styles.css."""
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "styles.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
