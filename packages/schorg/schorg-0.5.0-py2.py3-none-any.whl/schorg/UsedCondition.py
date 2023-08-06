"""
Indicates that the item is used.

https://schema.org/UsedCondition
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class UsedConditionInheritedProperties(TypedDict):
    """Indicates that the item is used.

    References:
        https://schema.org/UsedCondition
    Note:
        Model Depth 5
    Attributes:
    """

    


class UsedConditionProperties(TypedDict):
    """Indicates that the item is used.

    References:
        https://schema.org/UsedCondition
    Note:
        Model Depth 5
    Attributes:
    """

    

#UsedConditionInheritedPropertiesTd = UsedConditionInheritedProperties()
#UsedConditionPropertiesTd = UsedConditionProperties()


class AllProperties(UsedConditionInheritedProperties , UsedConditionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[UsedConditionProperties, UsedConditionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "UsedCondition"
    return model
    

UsedCondition = create_schema_org_model()