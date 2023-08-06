"""
Item is a pharmaceutical (e.g., a prescription or OTC drug) or a restricted medical device.

https://schema.org/HealthcareConsideration
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class HealthcareConsiderationInheritedProperties(TypedDict):
    """Item is a pharmaceutical (e.g., a prescription or OTC drug) or a restricted medical device.

    References:
        https://schema.org/HealthcareConsideration
    Note:
        Model Depth 5
    Attributes:
    """

    


class HealthcareConsiderationProperties(TypedDict):
    """Item is a pharmaceutical (e.g., a prescription or OTC drug) or a restricted medical device.

    References:
        https://schema.org/HealthcareConsideration
    Note:
        Model Depth 5
    Attributes:
    """

    

#HealthcareConsiderationInheritedPropertiesTd = HealthcareConsiderationInheritedProperties()
#HealthcareConsiderationPropertiesTd = HealthcareConsiderationProperties()


class AllProperties(HealthcareConsiderationInheritedProperties , HealthcareConsiderationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[HealthcareConsiderationProperties, HealthcareConsiderationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "HealthcareConsideration"
    return model
    

HealthcareConsideration = create_schema_org_model()