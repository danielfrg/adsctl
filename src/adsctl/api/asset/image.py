import io
import os

from PIL import Image

from adsctl.application import Application


def create(fpath, name: str, app: Application):
    fullpath = os.path.abspath(os.path.expanduser(fpath))

    client = app.create_client()
    asset_service = client.get_service("AssetService")
    asset_operation = client.get_type("AssetOperation")

    asset = asset_operation.create
    asset.type_ = client.enums.AssetTypeEnum.IMAGE

    # image_content = open(fullpath, "rb").read()
    img = Image.open(fullpath)

    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format=img.format)
    img_byte_arr = img_byte_arr.getvalue()

    asset.image_asset.data = img_byte_arr
    asset.image_asset.file_size = len(img_byte_arr)

    mime_type_enum = client.enums.MimeTypeEnum.IMAGE_JPEG
    if img.format == "PNG":
        mime_type_enum = client.enums.MimeTypeEnum.IMAGE_PNG
    asset.image_asset.mime_type = mime_type_enum

    width, height = img.size
    asset.image_asset.full_size.height_pixels = height
    asset.image_asset.full_size.width_pixels = width

    # asset.image_asset.full_size.url = url
    asset.name = name

    response = asset_service.mutate_assets(
        customer_id=app.account.customer_id, operations=[asset_operation]
    )

    return response
