"""
DJMixAlbum.

https://schema.org/DJMixAlbum
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DJMixAlbumInheritedProperties(TypedDict):
    """DJMixAlbum.

    References:
        https://schema.org/DJMixAlbum
    Note:
        Model Depth 5
    Attributes:
    """

    


class DJMixAlbumProperties(TypedDict):
    """DJMixAlbum.

    References:
        https://schema.org/DJMixAlbum
    Note:
        Model Depth 5
    Attributes:
    """

    

#DJMixAlbumInheritedPropertiesTd = DJMixAlbumInheritedProperties()
#DJMixAlbumPropertiesTd = DJMixAlbumProperties()


class AllProperties(DJMixAlbumInheritedProperties , DJMixAlbumProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DJMixAlbumProperties, DJMixAlbumInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DJMixAlbum"
    return model
    

DJMixAlbum = create_schema_org_model()