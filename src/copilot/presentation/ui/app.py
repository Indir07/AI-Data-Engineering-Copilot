"""Streamlit UI — Phase 2 skeleton.

Minimal on purpose: it proves the UI container can reach the API. The full
dashboard (agent selector, chat, code view, uploads, downloads) arrives in
Phase 7. Keeping the UI a thin client of the REST API mirrors the container
split described in docs/ARCHITECTURE.md.
"""

from __future__ import annotations

import os

import httpx
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(page_title="AI Data Engineering Copilot", page_icon="🧠", layout="wide")

st.title("🧠 AI Data Engineering Copilot")
st.caption("Phase 2 — skeleton. Agents, chat and RAG arrive in later phases.")

with st.sidebar:
    st.header("Status")
    if st.button("Check API health", use_container_width=True):
        try:
            resp = httpx.get(f"{API_BASE_URL}/health", timeout=5.0)
            resp.raise_for_status()
            st.success("API healthy")
            st.json(resp.json())
        except Exception as exc:  # noqa: BLE001 - surface any connection error to the user
            st.error(f"API unreachable: {exc}")

st.info(
    "This is the foundation build. Use the sidebar to confirm the backend is up. "
    "The interactive copilot lands in Phase 7."
)
