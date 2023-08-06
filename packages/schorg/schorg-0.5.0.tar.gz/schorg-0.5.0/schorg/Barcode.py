"""
An image of a visual machine-readable code such as a barcode or QR code.

https://schema.org/Barcode
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class BarcodeInheritedProperties(TypedDict):
    """An image of a visual machine-readable code such as a barcode or QR code.

    References:
        https://schema.org/Barcode
    Note:
        Model Depth 5
    Attributes:
        caption: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The caption for this object. For downloadable machine formats (closed caption, subtitles etc.) use MediaObject and indicate the [[encodingFormat]].
        thumbnail: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Thumbnail image for an image or video.
        exifData: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): exif data for this object.
        embeddedTextCaption: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Represents textual captioning from a [[MediaObject]], e.g. text of a 'meme'.
        representativeOfPage: (Optional[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]): Indicates whether this image is representative of the content of the page.
    """

    caption: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    thumbnail: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    exifData: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    embeddedTextCaption: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    representativeOfPage: NotRequired[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]
    


class BarcodeProperties(TypedDict):
    """An image of a visual machine-readable code such as a barcode or QR code.

    References:
        https://schema.org/Barcode
    Note:
        Model Depth 5
    Attributes:
    """

    

#BarcodeInheritedPropertiesTd = BarcodeInheritedProperties()
#BarcodePropertiesTd = BarcodeProperties()


class AllProperties(BarcodeInheritedProperties , BarcodeProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[BarcodeProperties, BarcodeInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Barcode"
    return model
    

Barcode = create_schema_org_model()