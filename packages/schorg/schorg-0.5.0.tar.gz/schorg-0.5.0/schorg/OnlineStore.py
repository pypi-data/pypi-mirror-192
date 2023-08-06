"""
An eCommerce site.

https://schema.org/OnlineStore
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OnlineStoreInheritedProperties(TypedDict):
    """An eCommerce site.

    References:
        https://schema.org/OnlineStore
    Note:
        Model Depth 4
    Attributes:
    """

    


class OnlineStoreProperties(TypedDict):
    """An eCommerce site.

    References:
        https://schema.org/OnlineStore
    Note:
        Model Depth 4
    Attributes:
    """

    

#OnlineStoreInheritedPropertiesTd = OnlineStoreInheritedProperties()
#OnlineStorePropertiesTd = OnlineStoreProperties()


class AllProperties(OnlineStoreInheritedProperties , OnlineStoreProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OnlineStoreProperties, OnlineStoreInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "OnlineStore"
    return model
    

OnlineStore = create_schema_org_model()