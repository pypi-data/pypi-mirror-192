"""
HealthCare: this is a benefit for health care.

https://schema.org/HealthCare
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class HealthCareInheritedProperties(TypedDict):
    """HealthCare: this is a benefit for health care.

    References:
        https://schema.org/HealthCare
    Note:
        Model Depth 5
    Attributes:
    """

    


class HealthCareProperties(TypedDict):
    """HealthCare: this is a benefit for health care.

    References:
        https://schema.org/HealthCare
    Note:
        Model Depth 5
    Attributes:
    """

    

#HealthCareInheritedPropertiesTd = HealthCareInheritedProperties()
#HealthCarePropertiesTd = HealthCareProperties()


class AllProperties(HealthCareInheritedProperties , HealthCareProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[HealthCareProperties, HealthCareInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "HealthCare"
    return model
    

HealthCare = create_schema_org_model()