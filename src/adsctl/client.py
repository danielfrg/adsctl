import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def get_client(config, version="v13"):
    try:
        googleads_client = GoogleAdsClient.load_from_dict(config, version=version)
        return googleads_client
    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)


def search(query, client, customer_id):
    customer_id = customer_id.replace("-", "")
    ga_service = client.get_service("GoogleAdsService")
    return ga_service.search(customer_id=customer_id, query=query)


def search_stream(query, client, customer_id):
    customer_id = customer_id.replace("-", "")
    ga_service = client.get_service("GoogleAdsService")
    return ga_service.search_stream(customer_id=customer_id, query=query)
