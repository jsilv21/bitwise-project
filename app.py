import streamlit as st
import pandas as pd
import snowflake.connector

# --- PAGE CONFIG ---
st.set_page_config(page_title="Bitwise GTM Analytics Demo", layout="wide")

# --- SNOWFLAKE CONNECTION ---
creds = st.secrets["snowflake"]
conn = snowflake.connector.connect(**creds)


# --- QUERY ---
@st.cache_data(ttl=300)
def load_data():
    query = """
    SELECT 
        d.date,
        c.client_type,
        ch.channel_name,
        ca.campaign_name,
        SUM(f.impressions) AS impressions,
        SUM(f.clicks) AS clicks,
        SUM(f.leads) AS leads,
        SUM(f.new_signups) AS new_signups,
        SUM(f.assets_under_management) AS total_aum
    FROM gtm_fact f
    JOIN date_dim d ON f.date_id = d.id
    JOIN client_dim c ON f.client_id = c.id
    JOIN campaign_dim ca ON f.campaign_id = ca.id
    JOIN channel_dim ch ON ca.channel_id = ch.id
    GROUP BY 1, 2, 3, 4
    ORDER BY 1 DESC;
    """
    return pd.read_sql(query, conn)


df = load_data()

# --- UI ---
st.title("📊 Bitwise GTM Analytics Demo")
st.markdown("### Marketing Performance Overview")

col1, col2 = st.columns(2)
col1.metric("Total Impressions", f"{df['impressions'].sum():,}")
col2.metric("Total AUM", f"${df['total_aum'].sum():,.0f}")

st.line_chart(df.groupby("date")["new_signups"].sum(), height=300)

st.bar_chart(df.groupby("channel_name")[["impressions", "clicks"]].sum())

st.dataframe(df.sample(20))
