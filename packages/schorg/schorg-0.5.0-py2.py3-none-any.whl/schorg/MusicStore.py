"""
A music store.

https://schema.org/MusicStore
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MusicStoreInheritedProperties(TypedDict):
    """A music store.

    References:
        https://schema.org/MusicStore
    Note:
        Model Depth 5
    Attributes:
    """

    


class MusicStoreProperties(TypedDict):
    """A music store.

    References:
        https://schema.org/MusicStore
    Note:
        Model Depth 5
    Attributes:
    """

    

#MusicStoreInheritedPropertiesTd = MusicStoreInheritedProperties()
#MusicStorePropertiesTd = MusicStoreProperties()


class AllProperties(MusicStoreInheritedProperties , MusicStoreProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MusicStoreProperties, MusicStoreInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MusicStore"
    return model
    

MusicStore = create_schema_org_model()