"""
An art gallery.

https://schema.org/ArtGallery
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ArtGalleryInheritedProperties(TypedDict):
    """An art gallery.

    References:
        https://schema.org/ArtGallery
    Note:
        Model Depth 5
    Attributes:
    """

    


class ArtGalleryProperties(TypedDict):
    """An art gallery.

    References:
        https://schema.org/ArtGallery
    Note:
        Model Depth 5
    Attributes:
    """

    

#ArtGalleryInheritedPropertiesTd = ArtGalleryInheritedProperties()
#ArtGalleryPropertiesTd = ArtGalleryProperties()


class AllProperties(ArtGalleryInheritedProperties , ArtGalleryProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ArtGalleryProperties, ArtGalleryInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ArtGallery"
    return model
    

ArtGallery = create_schema_org_model()