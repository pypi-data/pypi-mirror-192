"""
SoundtrackAlbum.

https://schema.org/SoundtrackAlbum
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SoundtrackAlbumInheritedProperties(TypedDict):
    """SoundtrackAlbum.

    References:
        https://schema.org/SoundtrackAlbum
    Note:
        Model Depth 5
    Attributes:
    """

    


class SoundtrackAlbumProperties(TypedDict):
    """SoundtrackAlbum.

    References:
        https://schema.org/SoundtrackAlbum
    Note:
        Model Depth 5
    Attributes:
    """

    

#SoundtrackAlbumInheritedPropertiesTd = SoundtrackAlbumInheritedProperties()
#SoundtrackAlbumPropertiesTd = SoundtrackAlbumProperties()


class AllProperties(SoundtrackAlbumInheritedProperties , SoundtrackAlbumProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SoundtrackAlbumProperties, SoundtrackAlbumInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "SoundtrackAlbum"
    return model
    

SoundtrackAlbum = create_schema_org_model()