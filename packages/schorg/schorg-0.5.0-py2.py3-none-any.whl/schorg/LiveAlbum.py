"""
LiveAlbum.

https://schema.org/LiveAlbum
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class LiveAlbumInheritedProperties(TypedDict):
    """LiveAlbum.

    References:
        https://schema.org/LiveAlbum
    Note:
        Model Depth 5
    Attributes:
    """

    


class LiveAlbumProperties(TypedDict):
    """LiveAlbum.

    References:
        https://schema.org/LiveAlbum
    Note:
        Model Depth 5
    Attributes:
    """

    

#LiveAlbumInheritedPropertiesTd = LiveAlbumInheritedProperties()
#LiveAlbumPropertiesTd = LiveAlbumProperties()


class AllProperties(LiveAlbumInheritedProperties , LiveAlbumProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[LiveAlbumProperties, LiveAlbumInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "LiveAlbum"
    return model
    

LiveAlbum = create_schema_org_model()