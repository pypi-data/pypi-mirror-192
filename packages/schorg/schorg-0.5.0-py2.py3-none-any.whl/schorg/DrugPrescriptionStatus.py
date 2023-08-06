"""
Indicates whether this drug is available by prescription or over-the-counter.

https://schema.org/DrugPrescriptionStatus
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DrugPrescriptionStatusInheritedProperties(TypedDict):
    """Indicates whether this drug is available by prescription or over-the-counter.

    References:
        https://schema.org/DrugPrescriptionStatus
    Note:
        Model Depth 5
    Attributes:
    """

    


class DrugPrescriptionStatusProperties(TypedDict):
    """Indicates whether this drug is available by prescription or over-the-counter.

    References:
        https://schema.org/DrugPrescriptionStatus
    Note:
        Model Depth 5
    Attributes:
    """

    

#DrugPrescriptionStatusInheritedPropertiesTd = DrugPrescriptionStatusInheritedProperties()
#DrugPrescriptionStatusPropertiesTd = DrugPrescriptionStatusProperties()


class AllProperties(DrugPrescriptionStatusInheritedProperties , DrugPrescriptionStatusProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DrugPrescriptionStatusProperties, DrugPrescriptionStatusInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DrugPrescriptionStatus"
    return model
    

DrugPrescriptionStatus = create_schema_org_model()