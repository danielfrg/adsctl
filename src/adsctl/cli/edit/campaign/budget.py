from google.api_core import protobuf_helpers

from adsctl.cli import utils


def mutate(client, customer_id, resource_name, budget):
    """Set campaign budget."""

    # Retrieve Object
    query = f"""
    SELECT campaign_budget.amount_micros, campaign_budget.resource_name
    FROM campaign_budget
    WHERE campaign_budget.resource_name = "{resource_name}"
    """

    response = utils.gaql_query(client, customer_id, query)
    first = utils.get_first_row(response)

    print(first)

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
    field_mask = protobuf_helpers.field_mask(None, updated._pb)
    print(field_mask)
    # Copy the field mask onto the operation's update_mask field.
    client.copy_from(campaign_budget_operation.update_mask, field_mask)

    response = campaign_budget_service.mutate_campaign_budgets(
        customer_id=customer_id, operations=[campaign_budget_operation]
    )

    return response


def get_rn(client, customer_id, campaign_id):
    """Get the budget ID for a campaign."""

    query = f"""
        SELECT campaign.id, campaign.campaign_budget
        FROM campaign
        WHERE campaign.id = {campaign_id}
    """

    response = utils.gaql_query(client, customer_id, query)
    for row in response:
        return row.campaign.campaign_budget
    return None
