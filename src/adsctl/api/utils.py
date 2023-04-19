from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers


def mask_operation(operation, updated, client: GoogleAdsClient):
    # Create a field mask using the updated campaign.
    field_mask = protobuf_helpers.field_mask(None, updated)

    # Copy the field mask onto the operation's update_mask field.
    client.copy_from(operation.update_mask, field_mask)
    client.copy_from(operation.update_mask, field_mask)
