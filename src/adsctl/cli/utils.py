

def gaql_query(client, customer_id, query):
    ga_service = client.get_service("GoogleAdsService")
    return ga_service.search(customer_id=customer_id, query=query)


def get_first_row(response):
    for row in response:
        return row
    return None

