GET_CAMPAIGNS_LIST = """
SELECT campaign.id, campaign.name FROM campaign ORDER BY campaign.id
"""

# To get what the UI shows in the Campaigns tab
GET_CAMPAIGNS_UI = """
SELECT campaign.name,
  campaign_budget.amount_micros,
  campaign.status,
  campaign.optimization_score,
  campaign.advertising_channel_type,
  metrics.clicks,
  metrics.impressions,
  metrics.ctr,
  metrics.average_cpc,
  metrics.cost_micros,
  campaign.bidding_strategy_type
FROM campaign
WHERE segments.date DURING LAST_7_DAYS
  AND campaign.status != 'REMOVED'
"""
