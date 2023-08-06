"""
AlbumRelease.

https://schema.org/AlbumRelease
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AlbumReleaseInheritedProperties(TypedDict):
    """AlbumRelease.

    References:
        https://schema.org/AlbumRelease
    Note:
        Model Depth 5
    Attributes:
    """

    


class AlbumReleaseProperties(TypedDict):
    """AlbumRelease.

    References:
        https://schema.org/AlbumRelease
    Note:
        Model Depth 5
    Attributes:
    """

    

#AlbumReleaseInheritedPropertiesTd = AlbumReleaseInheritedProperties()
#AlbumReleasePropertiesTd = AlbumReleaseProperties()


class AllProperties(AlbumReleaseInheritedProperties , AlbumReleaseProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AlbumReleaseProperties, AlbumReleaseInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "AlbumRelease"
    return model
    

AlbumRelease = create_schema_org_model()