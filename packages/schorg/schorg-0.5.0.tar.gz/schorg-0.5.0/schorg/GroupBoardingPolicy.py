"""
The airline boards by groups based on check-in time, priority, etc.

https://schema.org/GroupBoardingPolicy
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class GroupBoardingPolicyInheritedProperties(TypedDict):
    """The airline boards by groups based on check-in time, priority, etc.

    References:
        https://schema.org/GroupBoardingPolicy
    Note:
        Model Depth 5
    Attributes:
    """

    


class GroupBoardingPolicyProperties(TypedDict):
    """The airline boards by groups based on check-in time, priority, etc.

    References:
        https://schema.org/GroupBoardingPolicy
    Note:
        Model Depth 5
    Attributes:
    """

    

#GroupBoardingPolicyInheritedPropertiesTd = GroupBoardingPolicyInheritedProperties()
#GroupBoardingPolicyPropertiesTd = GroupBoardingPolicyProperties()


class AllProperties(GroupBoardingPolicyInheritedProperties , GroupBoardingPolicyProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[GroupBoardingPolicyProperties, GroupBoardingPolicyInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "GroupBoardingPolicy"
    return model
    

GroupBoardingPolicy = create_schema_org_model()