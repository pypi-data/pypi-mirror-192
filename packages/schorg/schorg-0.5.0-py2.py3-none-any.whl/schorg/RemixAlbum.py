"""
RemixAlbum.

https://schema.org/RemixAlbum
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class RemixAlbumInheritedProperties(TypedDict):
    """RemixAlbum.

    References:
        https://schema.org/RemixAlbum
    Note:
        Model Depth 5
    Attributes:
    """

    


class RemixAlbumProperties(TypedDict):
    """RemixAlbum.

    References:
        https://schema.org/RemixAlbum
    Note:
        Model Depth 5
    Attributes:
    """

    

#RemixAlbumInheritedPropertiesTd = RemixAlbumInheritedProperties()
#RemixAlbumPropertiesTd = RemixAlbumProperties()


class AllProperties(RemixAlbumInheritedProperties , RemixAlbumProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[RemixAlbumProperties, RemixAlbumInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "RemixAlbum"
    return model
    

RemixAlbum = create_schema_org_model()