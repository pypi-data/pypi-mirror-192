"""
MixtapeAlbum.

https://schema.org/MixtapeAlbum
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MixtapeAlbumInheritedProperties(TypedDict):
    """MixtapeAlbum.

    References:
        https://schema.org/MixtapeAlbum
    Note:
        Model Depth 5
    Attributes:
    """

    


class MixtapeAlbumProperties(TypedDict):
    """MixtapeAlbum.

    References:
        https://schema.org/MixtapeAlbum
    Note:
        Model Depth 5
    Attributes:
    """

    

#MixtapeAlbumInheritedPropertiesTd = MixtapeAlbumInheritedProperties()
#MixtapeAlbumPropertiesTd = MixtapeAlbumProperties()


class AllProperties(MixtapeAlbumInheritedProperties , MixtapeAlbumProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MixtapeAlbumProperties, MixtapeAlbumInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MixtapeAlbum"
    return model
    

MixtapeAlbum = create_schema_org_model()