from google.ads.googleads.client import GoogleAdsClient

from adsctl.api.utils import mask_operation
from adsctl.application import Application


def get_rn(campaign_id, app: Application) -> str:
    campaign_service = app.client.get_service("CampaignService")
    return campaign_service.campaign_path(app.customer_id, campaign_id)


def mutate(status, campaign_id, app: Application):
    client = app.client

    campaign_service = client.get_service("CampaignService")
    campaign_operation = client.get_type("CampaignOperation")

    resource_name = get_rn(campaign_id, app)

    updated = campaign_operation.update
    updated.resource_name = resource_name

    # Changes
    enum = statusToEnum(status, client)
    if enum is None:
        raise ValueError(f"Invalid status: {status}")

    updated.status = enum

    mask_operation(campaign_operation, updated, client)

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
