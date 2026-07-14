"""Streamlit dashboard for the AI Data Engineering Copilot.

A thin client over the FastAPI backend: pick an agent in the sidebar, chat in the
main panel, view generated code with syntax highlighting and citations, and
download results. All reasoning happens server-side via the /agents API.
"""

from __future__ import annotations

import httpx
import streamlit as st

from copilot.presentation.ui.components import api_client

st.set_page_config(
    page_title="AI Data Engineering Copilot",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

EXAMPLE_PROMPTS = {
    "sql": "Write SQL for the top 10 customers by total revenue in the last 90 days.",
    "pyspark": "Optimize a PySpark job that joins a 1TB fact table with a small dim table.",
    "etl": "Design a Bronze/Silver/Gold pipeline for clickstream events with incremental loads.",
    "data_quality": "Generate a Great Expectations suite for an orders table.",
    "documentation": "Write a README section documenting our ingestion pipeline.",
    "airflow": "Create an Airflow DAG that runs dbt daily with retries and a sensor.",
    "dbt": "Create a dbt staging model and schema tests for a raw_customers source.",
    "rag": "According to my uploaded docs, how is the silver layer defined?",
}


def _init_state() -> None:
    st.session_state.setdefault("history", [])  # list[dict(role, content, citations, agent)]


def _sidebar() -> dict:
    with st.sidebar:
        st.title("🧠 Copilot")
        st.caption("Your data-engineering teammate")

        agents = api_client.list_agents()
        labels = {a["agent"]: a["agent"].replace("_", " ").title() for a in agents}
        agent = st.selectbox(
            "Agent",
            options=[a["agent"] for a in agents],
            format_func=lambda a: labels.get(a, a),
        )
        desc = next((a["description"] for a in agents if a["agent"] == agent), "")
        st.caption(desc)

        dialect = None
        if agent == "sql":
            dialect = st.selectbox(
                "SQL dialect",
                ["ansi", "postgres", "snowflake", "bigquery", "databricks", "duckdb", "sqlite", "spark"],
            )

        with st.expander("Options"):
            model = st.text_input("Model override", value="", placeholder="e.g. llama3.1:8b-instruct")
            temperature = st.slider("Temperature", 0.0, 1.0, 0.1, 0.05)
            use_rag = st.checkbox("Ground with uploaded docs (RAG)", value=(agent == "rag"))

        st.divider()
        st.subheader("Documents")
        uploaded = st.file_uploader("Upload PDF / MD / CSV / TXT", type=["pdf", "md", "csv", "txt"])
        if uploaded is not None and st.button("Index document", use_container_width=True):
            res = api_client.upload_document(uploaded.name, uploaded.getvalue(), uploaded.type or "text/plain")
            if res.get("available"):
                st.success(f"Indexed {uploaded.name}")
            else:
                st.info("Document indexing arrives with the RAG engine (Phase 5).")

        st.divider()
        with st.expander("Backend status"):
            try:
                st.json(api_client.get_health())
            except Exception as exc:  # noqa: BLE001
                st.error(f"API unreachable: {exc}")

        if st.button("Clear conversation", use_container_width=True):
            st.session_state["history"] = []
            st.rerun()

    return {
        "agent": agent,
        "dialect": dialect,
        "model": model or None,
        "temperature": temperature,
        "use_rag": use_rag,
    }


def _render_history() -> None:
    for turn in st.session_state["history"]:
        with st.chat_message(turn["role"]):
            st.markdown(turn["content"])
            if turn.get("citations"):
                with st.expander("Sources"):
                    for c in turn["citations"]:
                        st.markdown(f"- **{c['source']}** — {c['snippet']}")
            if turn["role"] == "assistant":
                st.download_button(
                    "Download",
                    data=turn["content"],
                    file_name=f"{turn.get('agent', 'copilot')}_output.md",
                    key=f"dl_{id(turn)}",
                )


def main() -> None:
    _init_state()
    opts = _sidebar()

    st.title("AI Data Engineering Copilot")
    st.caption(f"Active agent: **{opts['agent']}**")

    if not st.session_state["history"]:
        example = EXAMPLE_PROMPTS.get(opts["agent"])
        if example:
            st.info(f"Try: _{example}_")

    _render_history()

    prompt = st.chat_input("Ask the copilot…")
    if not prompt:
        return

    st.session_state["history"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    payload = {
        "prompt": prompt,
        "model": opts["model"],
        "temperature": opts["temperature"],
        "use_rag": opts["use_rag"],
    }
    if opts["dialect"]:
        payload["dialect"] = opts["dialect"]

    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            try:
                result = api_client.run_agent(opts["agent"], payload)
            except httpx.HTTPError as exc:
                st.error(f"Request failed: {exc}")
                return
        st.markdown(result["content"])
        st.session_state["history"].append(
            {
                "role": "assistant",
                "content": result["content"],
                "citations": result.get("citations", []),
                "agent": opts["agent"],
            }
        )
        st.rerun()


if __name__ == "__main__":
    main()
