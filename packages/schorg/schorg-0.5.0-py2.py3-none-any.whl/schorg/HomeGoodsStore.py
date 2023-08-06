"""
A home goods store.

https://schema.org/HomeGoodsStore
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class HomeGoodsStoreInheritedProperties(TypedDict):
    """A home goods store.

    References:
        https://schema.org/HomeGoodsStore
    Note:
        Model Depth 5
    Attributes:
    """

    


class HomeGoodsStoreProperties(TypedDict):
    """A home goods store.

    References:
        https://schema.org/HomeGoodsStore
    Note:
        Model Depth 5
    Attributes:
    """

    

#HomeGoodsStoreInheritedPropertiesTd = HomeGoodsStoreInheritedProperties()
#HomeGoodsStorePropertiesTd = HomeGoodsStoreProperties()


class AllProperties(HomeGoodsStoreInheritedProperties , HomeGoodsStoreProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[HomeGoodsStoreProperties, HomeGoodsStoreInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "HomeGoodsStore"
    return model
    

HomeGoodsStore = create_schema_org_model()