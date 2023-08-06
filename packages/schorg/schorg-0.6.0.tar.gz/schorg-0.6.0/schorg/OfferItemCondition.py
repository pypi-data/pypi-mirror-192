"""
A list of possible conditions for the item.

https://schema.org/OfferItemCondition
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OfferItemConditionInheritedProperties(TypedDict):
    """A list of possible conditions for the item.

    References:
        https://schema.org/OfferItemCondition
    Note:
        Model Depth 4
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class OfferItemConditionProperties(TypedDict):
    """A list of possible conditions for the item.

    References:
        https://schema.org/OfferItemCondition
    Note:
        Model Depth 4
    Attributes:
    """

    

#OfferItemConditionInheritedPropertiesTd = OfferItemConditionInheritedProperties()
#OfferItemConditionPropertiesTd = OfferItemConditionProperties()


class AllProperties(OfferItemConditionInheritedProperties , OfferItemConditionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OfferItemConditionProperties, OfferItemConditionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "OfferItemCondition"
    return model
    

OfferItemCondition = create_schema_org_model()