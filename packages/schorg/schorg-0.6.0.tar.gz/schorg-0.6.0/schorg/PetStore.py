"""
A pet store.

https://schema.org/PetStore
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PetStoreInheritedProperties(TypedDict):
    """A pet store.

    References:
        https://schema.org/PetStore
    Note:
        Model Depth 5
    Attributes:
    """

    


class PetStoreProperties(TypedDict):
    """A pet store.

    References:
        https://schema.org/PetStore
    Note:
        Model Depth 5
    Attributes:
    """

    

#PetStoreInheritedPropertiesTd = PetStoreInheritedProperties()
#PetStorePropertiesTd = PetStoreProperties()


class AllProperties(PetStoreInheritedProperties , PetStoreProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PetStoreProperties, PetStoreInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PetStore"
    return model
    

PetStore = create_schema_org_model()