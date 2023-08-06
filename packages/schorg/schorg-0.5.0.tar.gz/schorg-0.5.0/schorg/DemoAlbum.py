"""
DemoAlbum.

https://schema.org/DemoAlbum
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DemoAlbumInheritedProperties(TypedDict):
    """DemoAlbum.

    References:
        https://schema.org/DemoAlbum
    Note:
        Model Depth 5
    Attributes:
    """

    


class DemoAlbumProperties(TypedDict):
    """DemoAlbum.

    References:
        https://schema.org/DemoAlbum
    Note:
        Model Depth 5
    Attributes:
    """

    

#DemoAlbumInheritedPropertiesTd = DemoAlbumInheritedProperties()
#DemoAlbumPropertiesTd = DemoAlbumProperties()


class AllProperties(DemoAlbumInheritedProperties , DemoAlbumProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DemoAlbumProperties, DemoAlbumInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DemoAlbum"
    return model
    

DemoAlbum = create_schema_org_model()