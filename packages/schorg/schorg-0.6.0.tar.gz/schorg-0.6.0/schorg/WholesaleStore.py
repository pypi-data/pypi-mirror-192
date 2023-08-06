"""
A wholesale store.

https://schema.org/WholesaleStore
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WholesaleStoreInheritedProperties(TypedDict):
    """A wholesale store.

    References:
        https://schema.org/WholesaleStore
    Note:
        Model Depth 5
    Attributes:
    """

    


class WholesaleStoreProperties(TypedDict):
    """A wholesale store.

    References:
        https://schema.org/WholesaleStore
    Note:
        Model Depth 5
    Attributes:
    """

    

#WholesaleStoreInheritedPropertiesTd = WholesaleStoreInheritedProperties()
#WholesaleStorePropertiesTd = WholesaleStoreProperties()


class AllProperties(WholesaleStoreInheritedProperties , WholesaleStoreProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WholesaleStoreProperties, WholesaleStoreInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WholesaleStore"
    return model
    

WholesaleStore = create_schema_org_model()