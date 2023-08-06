"""
Indicates that the item is damaged.

https://schema.org/DamagedCondition
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DamagedConditionInheritedProperties(TypedDict):
    """Indicates that the item is damaged.

    References:
        https://schema.org/DamagedCondition
    Note:
        Model Depth 5
    Attributes:
    """

    


class DamagedConditionProperties(TypedDict):
    """Indicates that the item is damaged.

    References:
        https://schema.org/DamagedCondition
    Note:
        Model Depth 5
    Attributes:
    """

    

#DamagedConditionInheritedPropertiesTd = DamagedConditionInheritedProperties()
#DamagedConditionPropertiesTd = DamagedConditionProperties()


class AllProperties(DamagedConditionInheritedProperties , DamagedConditionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DamagedConditionProperties, DamagedConditionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DamagedCondition"
    return model
    

DamagedCondition = create_schema_org_model()