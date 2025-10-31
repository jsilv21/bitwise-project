import pandas as pd
import numpy as np

# ---------------------------
# Load dimension CSVs
# ---------------------------
date_dim = pd.read_csv("date_dim.csv")
client_dim = pd.read_csv("client_dim.csv")
campaign_dim = pd.read_csv("campaign_dim.csv")
fund_dim = pd.read_csv("fund_dim.csv")


# ---------------------------
# Helper function to generate daily metrics
# ---------------------------
def generate_metrics(n_rows, client_au):
    impressions = np.random.randint(4000, 10000, size=n_rows)
    clicks = (impressions * np.random.uniform(0.02, 0.05, size=n_rows)).astype(int)
    leads = (clicks * np.random.uniform(0.1, 0.15, size=n_rows)).astype(int)
    new_signups = (leads * np.random.uniform(0.3, 0.5, size=n_rows)).astype(int)
    assets_under_management = (
        client_au * np.random.uniform(0.002, 0.005, size=n_rows)
    ).round(0)
    weight = np.random.uniform(0.1, 0.5, size=n_rows).round(2)
    price_usd = np.random.uniform(20, 80, size=n_rows).round(2)
    return (
        impressions,
        clicks,
        leads,
        new_signups,
        assets_under_management,
        weight,
        price_usd,
    )


# ---------------------------
# Generate GTM Fact Table
# ---------------------------
rows = []
id_counter = 1

for _, date_row in date_dim.iterrows():
    date_id = date_row["id"]
    for _, client_row in client_dim.iterrows():
        client_id = client_row["id"]
        client_au = client_row["total_assets_under_management"]
        # Filter campaigns active on this date
        active_campaigns = campaign_dim[
            (
                pd.to_datetime(campaign_dim["start_date"])
                <= pd.to_datetime(date_row["date"])
            )
            & (
                pd.to_datetime(campaign_dim["end_date"])
                >= pd.to_datetime(date_row["date"])
            )
        ]
        for _, campaign_row in active_campaigns.iterrows():
            campaign_id = campaign_row["id"]
            for _, fund_row in fund_dim.iterrows():
                fund_id = fund_row["id"]
                # Generate metrics
                impressions, clicks, leads, new_signups, aum, weight, price_usd = (
                    generate_metrics(1, client_au)
                )
                rows.append(
                    [
                        id_counter,
                        date_id,
                        client_id,
                        campaign_id,
                        fund_id,
                        impressions[0],
                        clicks[0],
                        leads[0],
                        new_signups[0],
                        aum[0],
                        weight[0],
                        price_usd[0],
                    ]
                )
                id_counter += 1

gtm_fact = pd.DataFrame(
    rows,
    columns=[
        "id",
        "date_id",
        "client_id",
        "campaign_id",
        "fund_id",
        "impressions",
        "clicks",
        "leads",
        "new_signups",
        "assets_under_management",
        "weight",
        "price_usd",
    ],
)

# ---------------------------
# Export to CSV
# ---------------------------
gtm_fact.to_csv("gtm_fact.csv", index=False)
print("gtm_fact.csv generated with", len(gtm_fact), "rows")
