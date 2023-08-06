"""
SpokenWordAlbum.

https://schema.org/SpokenWordAlbum
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SpokenWordAlbumInheritedProperties(TypedDict):
    """SpokenWordAlbum.

    References:
        https://schema.org/SpokenWordAlbum
    Note:
        Model Depth 5
    Attributes:
    """

    


class SpokenWordAlbumProperties(TypedDict):
    """SpokenWordAlbum.

    References:
        https://schema.org/SpokenWordAlbum
    Note:
        Model Depth 5
    Attributes:
    """

    

#SpokenWordAlbumInheritedPropertiesTd = SpokenWordAlbumInheritedProperties()
#SpokenWordAlbumPropertiesTd = SpokenWordAlbumProperties()


class AllProperties(SpokenWordAlbumInheritedProperties , SpokenWordAlbumProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SpokenWordAlbumProperties, SpokenWordAlbumInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "SpokenWordAlbum"
    return model
    

SpokenWordAlbum = create_schema_org_model()