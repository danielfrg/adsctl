from adsctl.application import Application


def get_rn(id, app: Application):
    """Get the Resource Name for a campaign."""

    query = f"""
        SELECT campaign.resource_name, campaign.id
        FROM campaign
        WHERE campaign.id = {id}
    """

    response = app.search(query)
    for row in response:
        return row.campaign.resource_name
    return None
    return None
