import streamlit as st
import pandas as pd
import snowflake.connector

# --- PAGE CONFIG ---
st.set_page_config(page_title="Bitwise GTM Analytics Demo", layout="wide")

# --- SNOWFLAKE CONNECTION ---
creds = st.secrets["snowflake"]
conn = snowflake.connector.connect(**creds)


@st.cache_data(ttl=300)
def load_data(start_date, end_date):
    query = f"""
    SELECT 
        DATE,
        CLIENT_TYPE,
        CAMPAIGN_NAME,
        CHANNEL_NAME,
        CHANNEL_TYPE,
        FUND_NAME,
        TICKER,
        SUM(IMPRESSIONS) AS IMPRESSIONS,
        SUM(CLICKS) AS CLICKS,
        SUM(LEADS) AS LEADS,
        SUM(NEW_SIGNUPS) AS NEW_SIGNUPS,
        SUM(ASSETS_UNDER_MANAGEMENT) AS TOTAL_AUM,
        AVG(PRICE_USD) AS AVG_PRICE_USD,
        AVG(WEIGHT) AS AVG_WEIGHT
    FROM RAW_STG.STG_GTM_FACT
    WHERE DATE BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY 1,2,3,4,5,6,7
    ORDER BY DATE ASC;
    """
    return pd.read_sql(query, conn)


# --- DATE FILTER ---
st.title("📈 Bitwise GTM Analytics Dashboard")

default_start = "2025-02-01"
default_end = "2025-02-28"
start_date, end_date = st.date_input(
    "Select Date Range",
    value=(pd.to_datetime(default_start), pd.to_datetime(default_end)),
)

df = load_data(start_date, end_date)

# --- KPI SECTION ---
st.subheader("Marketing Funnel Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Impressions", f"{df['IMPRESSIONS'].sum():,}")
col2.metric("Total Clicks", f"{df['CLICKS'].sum():,}")
col3.metric("Total New Signups", f"{df['NEW_SIGNUPS'].sum():,}")
col4.metric("Total AUM", f"${df['TOTAL_AUM'].sum():,.0f}")

# --- CHARTS ---
st.markdown("### 📊 Signups Over Time")
signups_over_time = df.groupby("DATE")["NEW_SIGNUPS"].sum()
st.line_chart(signups_over_time)

st.markdown("### 🧲 Impressions vs Clicks by Channel")
channel_perf = df.groupby("CHANNEL_NAME")[["IMPRESSIONS", "CLICKS"]].sum()
st.bar_chart(channel_perf)

st.markdown("### 💼 Average Fund Price by Fund")
fund_price = (
    df.groupby("FUND_NAME")["AVG_PRICE_USD"].mean().sort_values(ascending=False)
)
st.bar_chart(fund_price)

# --- DATA TABLE ---
st.markdown("### Raw Sample Data")
st.dataframe(df.sample(min(30, len(df))))
