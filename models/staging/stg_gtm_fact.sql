-- stg_gtm_fact.sql
select
    f.id as gtm_event_id,
    d.date,
    c.name as client_name,
    c.client_type,
    ca.campaign_name,
    ch.channel_name,
    ch.channel_type,
    fu.fund_name,
    fu.ticker,
    ROUND(f.impressions/500,0) AS impressions,
    ROUND(f.clicks/100,0) AS clicks,
    ROUND(f.leads/2,0) AS leads,
    ROUND(f.new_signups/10,0) AS new_signups,
    ROUND(f.assets_under_management/1000,0) AS assets_under_management,
    f.price_usd,
    f.weight
from {{ source("raw", "gtm_fact") }} f
join {{ source("raw", "date_dim") }} d on f.date_id = d.id
join {{ source("raw", "client_dim") }} c on f.client_id = c.id
join {{ source("raw", "campaign_dim") }} ca on f.campaign_id = ca.id
join {{ source("raw", "channel_dim") }} ch on ca.channel_id = ch.id
join {{ source("raw", "fund_dim") }} fu on f.fund_id = fu.id
