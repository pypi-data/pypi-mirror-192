"""
Indicates that the item is refurbished.

https://schema.org/RefurbishedCondition
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class RefurbishedConditionInheritedProperties(TypedDict):
    """Indicates that the item is refurbished.

    References:
        https://schema.org/RefurbishedCondition
    Note:
        Model Depth 5
    Attributes:
    """

    


class RefurbishedConditionProperties(TypedDict):
    """Indicates that the item is refurbished.

    References:
        https://schema.org/RefurbishedCondition
    Note:
        Model Depth 5
    Attributes:
    """

    

#RefurbishedConditionInheritedPropertiesTd = RefurbishedConditionInheritedProperties()
#RefurbishedConditionPropertiesTd = RefurbishedConditionProperties()


class AllProperties(RefurbishedConditionInheritedProperties , RefurbishedConditionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[RefurbishedConditionProperties, RefurbishedConditionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "RefurbishedCondition"
    return model
    

RefurbishedCondition = create_schema_org_model()