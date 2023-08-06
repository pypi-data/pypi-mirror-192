"""
The airline boards by zones of the plane.

https://schema.org/ZoneBoardingPolicy
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ZoneBoardingPolicyInheritedProperties(TypedDict):
    """The airline boards by zones of the plane.

    References:
        https://schema.org/ZoneBoardingPolicy
    Note:
        Model Depth 5
    Attributes:
    """

    


class ZoneBoardingPolicyProperties(TypedDict):
    """The airline boards by zones of the plane.

    References:
        https://schema.org/ZoneBoardingPolicy
    Note:
        Model Depth 5
    Attributes:
    """

    

#ZoneBoardingPolicyInheritedPropertiesTd = ZoneBoardingPolicyInheritedProperties()
#ZoneBoardingPolicyPropertiesTd = ZoneBoardingPolicyProperties()


class AllProperties(ZoneBoardingPolicyInheritedProperties , ZoneBoardingPolicyProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ZoneBoardingPolicyProperties, ZoneBoardingPolicyInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ZoneBoardingPolicy"
    return model
    

ZoneBoardingPolicy = create_schema_org_model()