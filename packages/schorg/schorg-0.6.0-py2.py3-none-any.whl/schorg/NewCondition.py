"""
Indicates that the item is new.

https://schema.org/NewCondition
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class NewConditionInheritedProperties(TypedDict):
    """Indicates that the item is new.

    References:
        https://schema.org/NewCondition
    Note:
        Model Depth 5
    Attributes:
    """

    


class NewConditionProperties(TypedDict):
    """Indicates that the item is new.

    References:
        https://schema.org/NewCondition
    Note:
        Model Depth 5
    Attributes:
    """

    

#NewConditionInheritedPropertiesTd = NewConditionInheritedProperties()
#NewConditionPropertiesTd = NewConditionProperties()


class AllProperties(NewConditionInheritedProperties , NewConditionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[NewConditionProperties, NewConditionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "NewCondition"
    return model
    

NewCondition = create_schema_org_model()