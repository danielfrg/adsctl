from google.api_core import protobuf_helpers

from adsctl.app import Application
from adsctl.cli import utils


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


def mutate(resource_name, budget, app: Application):
    """Set campaign budget."""

    client = app.client

    # Retrieve Object
    query = f"""
    SELECT campaign_budget.amount_micros, campaign_budget.resource_name
    FROM campaign_budget
    WHERE campaign_budget.resource_name = "{resource_name}"
    """

    response = app.search_stream(query)
    first = utils.get_first_row(response)

    if first is None:
        print(f"Budget not found for campaign {resource_name}")
        return None

    # Update Object
    campaign_budget_service = client.get_service("CampaignBudgetService")
    campaign_budget_operation = client.get_type("CampaignBudgetOperation")

    updated = campaign_budget_operation.update
    updated.resource_name = resource_name

    # Changes
    updated.amount_micros = int(budget * 1000000)

    # Create a field mask using the updated campaign.
    field_mask = protobuf_helpers.field_mask(None, updated)

    # Copy the field mask onto the operation's update_mask field.
    client.copy_from(campaign_budget_operation.update_mask, field_mask)

    response = campaign_budget_service.mutate_campaign_budgets(
        customer_id=app.customer_id, operations=[campaign_budget_operation]
    )

    return response
