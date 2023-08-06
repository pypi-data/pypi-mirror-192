"""
Web page type: Video gallery page.

https://schema.org/VideoGallery
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class VideoGalleryInheritedProperties(TypedDict):
    """Web page type: Video gallery page.

    References:
        https://schema.org/VideoGallery
    Note:
        Model Depth 6
    Attributes:
    """

    


class VideoGalleryProperties(TypedDict):
    """Web page type: Video gallery page.

    References:
        https://schema.org/VideoGallery
    Note:
        Model Depth 6
    Attributes:
    """

    

#VideoGalleryInheritedPropertiesTd = VideoGalleryInheritedProperties()
#VideoGalleryPropertiesTd = VideoGalleryProperties()


class AllProperties(VideoGalleryInheritedProperties , VideoGalleryProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[VideoGalleryProperties, VideoGalleryInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "VideoGallery"
    return model
    

VideoGallery = create_schema_org_model()