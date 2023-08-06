"""
A randomized trial design.

https://schema.org/RandomizedTrial
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class RandomizedTrialInheritedProperties(TypedDict):
    """A randomized trial design.

    References:
        https://schema.org/RandomizedTrial
    Note:
        Model Depth 6
    Attributes:
    """

    


class RandomizedTrialProperties(TypedDict):
    """A randomized trial design.

    References:
        https://schema.org/RandomizedTrial
    Note:
        Model Depth 6
    Attributes:
    """

    

#RandomizedTrialInheritedPropertiesTd = RandomizedTrialInheritedProperties()
#RandomizedTrialPropertiesTd = RandomizedTrialProperties()


class AllProperties(RandomizedTrialInheritedProperties , RandomizedTrialProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[RandomizedTrialProperties, RandomizedTrialInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "RandomizedTrial"
    return model
    

RandomizedTrial = create_schema_org_model()