"""
A toy store.

https://schema.org/ToyStore
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ToyStoreInheritedProperties(TypedDict):
    """A toy store.

    References:
        https://schema.org/ToyStore
    Note:
        Model Depth 5
    Attributes:
    """

    


class ToyStoreProperties(TypedDict):
    """A toy store.

    References:
        https://schema.org/ToyStore
    Note:
        Model Depth 5
    Attributes:
    """

    

#ToyStoreInheritedPropertiesTd = ToyStoreInheritedProperties()
#ToyStorePropertiesTd = ToyStoreProperties()


class AllProperties(ToyStoreInheritedProperties , ToyStoreProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ToyStoreProperties, ToyStoreInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ToyStore"
    return model
    

ToyStore = create_schema_org_model()