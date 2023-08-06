"""
A convenience store.

https://schema.org/ConvenienceStore
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ConvenienceStoreInheritedProperties(TypedDict):
    """A convenience store.

    References:
        https://schema.org/ConvenienceStore
    Note:
        Model Depth 5
    Attributes:
    """

    


class ConvenienceStoreProperties(TypedDict):
    """A convenience store.

    References:
        https://schema.org/ConvenienceStore
    Note:
        Model Depth 5
    Attributes:
    """

    

#ConvenienceStoreInheritedPropertiesTd = ConvenienceStoreInheritedProperties()
#ConvenienceStorePropertiesTd = ConvenienceStoreProperties()


class AllProperties(ConvenienceStoreInheritedProperties , ConvenienceStoreProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ConvenienceStoreProperties, ConvenienceStoreInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ConvenienceStore"
    return model
    

ConvenienceStore = create_schema_org_model()