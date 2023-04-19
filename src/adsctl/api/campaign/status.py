from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

from adsctl.application import Application


def mutate(status, campaign_id, app: Application):
    client = app.client

    campaign_service = client.get_service("CampaignService")
    campaign_operation = client.get_type("CampaignOperation")

    resource_name = campaign_service.campaign_path(app.customer_id, campaign_id)

    updated = campaign_operation.update
    updated.resource_name = resource_name

    # Changes
    enum = statusToEnum(status, client)
    if enum is None:
        raise ValueError(f"Invalid status: {status}")

    updated.status = enum

    # Create a field mask using the updated campaign.
    field_mask = protobuf_helpers.field_mask(None, updated)

    # Copy the field mask onto the operation's update_mask field.
    client.copy_from(campaign_operation.update_mask, field_mask)

    response = campaign_service.mutate_campaigns(
        customer_id=app.customer_id, operations=[campaign_operation]
    )

    return response


def statusToEnum(status, client: GoogleAdsClient):
    enums = client.enums.CampaignStatusEnum.CampaignStatus

    if status == "enabled":
        return enums.ENABLED
    elif status == "paused":
        return enums.PAUSED
    else:
        return None
