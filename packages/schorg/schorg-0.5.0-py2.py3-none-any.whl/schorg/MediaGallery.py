"""
Web page type: Media gallery page. A mixed-media page that can contain media such as images, videos, and other multimedia.

https://schema.org/MediaGallery
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MediaGalleryInheritedProperties(TypedDict):
    """Web page type: Media gallery page. A mixed-media page that can contain media such as images, videos, and other multimedia.

    References:
        https://schema.org/MediaGallery
    Note:
        Model Depth 5
    Attributes:
    """

    


class MediaGalleryProperties(TypedDict):
    """Web page type: Media gallery page. A mixed-media page that can contain media such as images, videos, and other multimedia.

    References:
        https://schema.org/MediaGallery
    Note:
        Model Depth 5
    Attributes:
    """

    

#MediaGalleryInheritedPropertiesTd = MediaGalleryInheritedProperties()
#MediaGalleryPropertiesTd = MediaGalleryProperties()


class AllProperties(MediaGalleryInheritedProperties , MediaGalleryProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MediaGalleryProperties, MediaGalleryInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MediaGallery"
    return model
    

MediaGallery = create_schema_org_model()