"""Domain enumerations shared across agents and use cases."""

from __future__ import annotations

from enum import Enum


class AgentType(str, Enum):
    """The specialist agents the copilot can route a request to."""

    SQL = "sql"
    PYSPARK = "pyspark"
    ETL = "etl"
    DATA_QUALITY = "data_quality"
    DOCUMENTATION = "documentation"
    AIRFLOW = "airflow"
    DBT = "dbt"
    RAG = "rag"


class SqlDialect(str, Enum):
    """SQL dialects the SQL agent can target / translate between."""

    ANSI = "ansi"
    POSTGRES = "postgres"
    SNOWFLAKE = "snowflake"
    BIGQUERY = "bigquery"
    DATABRICKS = "databricks"
    DUCKDB = "duckdb"
    SQLITE = "sqlite"
    SPARK = "spark"
