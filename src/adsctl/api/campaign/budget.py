from adsctl.api.utils import mask_operation
from adsctl.application import Application


def get_rn(campaign_id, app: Application):
    """Get the budget Resource Name for a campaign."""

    query = f"""
        SELECT campaign.id, campaign.campaign_budget
        FROM campaign
        WHERE campaign.id = {campaign_id}
    """

    response = app.search(query)
    for row in response:
        return row.campaign.campaign_budget
    return None


def mutate(budget, resource_name: str, app: Application):
    """Set campaign budget."""
    client = app.client

    campaign_budget_service = client.get_service("CampaignBudgetService")
    campaign_budget_operation = client.get_type("CampaignBudgetOperation")

    updated = campaign_budget_operation.update
    updated.resource_name = resource_name

    # Changes
    updated.amount_micros = int(budget * 1000000)

    # Boilerplate:
    mask_operation(campaign_budget_operation, updated, client)

    response = campaign_budget_service.mutate_campaign_budgets(
        customer_id=app.customer_id, operations=[campaign_budget_operation]
    )

    return response
