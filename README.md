# Sample Bitwise Analytics Project

## Table of contents

- [Analytics Dashboard](#analytics-dashboard)
- [Overview](#overview)
- [How it works (high level)](#how-it-works-high-level)
- [Architecture](#architecture)
- [Design Screenshots](#design-screenshots)

## Analytics Dashboard

[Dashboard Link (Streamlit Cloud)](https://bitwise-demo.streamlit.app/)

## Overview

This project demonstrates a simple analytics pipeline:
S3 -> Snowflake -> dbt -> Streamlit.

- Ingest raw CSVs (sample data) into an S3-like stage.
- Load staged data into Snowflake (raw schema).
- Transform raw tables into analytics models using dbt.
- Expose results via a Streamlit app ([app.py](app.py)) for dashboards and exploration.

## How it works (high level)

1. Raw data (examples in CSVs [sample-data](/sample-data/)) is ingested to S3 staging.
2. COPY INTO Snowflake stage or use a small loader to ingest into a raw schema.
3. Run dbt to transform raw tables into analytics-ready models (facts and dims).
4. The Streamlit app ([app.py](app.py)) queries Snowflake to render dashboards.

### Architecture

```mermaid
flowchart TD
    subgraph SOURCES
        A1["Campaign/Channel Data
        (CSV)"]
        A2["Client Data
        (CSV)"]
        A3["Fund Data
        (CSV)"]
    end
    subgraph INGESTION
        B1["S3 Bucket"]
        B2["Snowflake Integration"]
    end
    subgraph WAREHOUSE
        C1["Snowflake Raw Schema"]
        C2["Snowflake Analytics Schema"]
        C3["Dimensional Models
        Fact & Dimensions"]
    end
    subgraph DBT_TRANSFORM
        T1["dbt Models & Transforms"]
    end
    subgraph BI_LAYER
        D1["Streamlit (Or other apps)"]
        D2["Dashboards & Visualizations
        Funnel, AUM, Conversion, Channel ROI"]
    end
    %% Data Flow
    A1 --> B1
    A2 --> B1
    A3 --> B1
    B1 --> B2
    B2 --> C1
    C1 --> T1
    T1 --> C2
    C2 --> C3
    C3 --> D1
    D1 --> D2

    %% Circular reference for dbt
    C2 --> T1
```

### Design Screenshots

**AWS S3, IAM**
![AWS S3](/images/s3.png)
![AWS IAM](/images/aws-iam-1.png)
![AWS IAM](/images/aws-iam-2.png)

**Database Design**
![DB Design](/images/bitwise-db-diagram.png)

**Snowflake**
![Snowflake](/images/snowflake.png)
