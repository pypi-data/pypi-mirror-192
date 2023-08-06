"""
CompilationAlbum.

https://schema.org/CompilationAlbum
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class CompilationAlbumInheritedProperties(TypedDict):
    """CompilationAlbum.

    References:
        https://schema.org/CompilationAlbum
    Note:
        Model Depth 5
    Attributes:
    """

    


class CompilationAlbumProperties(TypedDict):
    """CompilationAlbum.

    References:
        https://schema.org/CompilationAlbum
    Note:
        Model Depth 5
    Attributes:
    """

    

#CompilationAlbumInheritedPropertiesTd = CompilationAlbumInheritedProperties()
#CompilationAlbumPropertiesTd = CompilationAlbumProperties()


class AllProperties(CompilationAlbumInheritedProperties , CompilationAlbumProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[CompilationAlbumProperties, CompilationAlbumInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "CompilationAlbum"
    return model
    

CompilationAlbum = create_schema_org_model()