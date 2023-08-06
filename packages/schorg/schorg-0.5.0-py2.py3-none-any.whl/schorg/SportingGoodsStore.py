"""
A sporting goods store.

https://schema.org/SportingGoodsStore
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SportingGoodsStoreInheritedProperties(TypedDict):
    """A sporting goods store.

    References:
        https://schema.org/SportingGoodsStore
    Note:
        Model Depth 5
    Attributes:
    """

    


class SportingGoodsStoreProperties(TypedDict):
    """A sporting goods store.

    References:
        https://schema.org/SportingGoodsStore
    Note:
        Model Depth 5
    Attributes:
    """

    

#SportingGoodsStoreInheritedPropertiesTd = SportingGoodsStoreInheritedProperties()
#SportingGoodsStorePropertiesTd = SportingGoodsStoreProperties()


class AllProperties(SportingGoodsStoreInheritedProperties , SportingGoodsStoreProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SportingGoodsStoreProperties, SportingGoodsStoreInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "SportingGoodsStore"
    return model
    

SportingGoodsStore = create_schema_org_model()