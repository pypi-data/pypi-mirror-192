"""
Systems of medical practice.

https://schema.org/MedicineSystem
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MedicineSystemInheritedProperties(TypedDict):
    """Systems of medical practice.

    References:
        https://schema.org/MedicineSystem
    Note:
        Model Depth 5
    Attributes:
    """

    


class MedicineSystemProperties(TypedDict):
    """Systems of medical practice.

    References:
        https://schema.org/MedicineSystem
    Note:
        Model Depth 5
    Attributes:
    """

    

#MedicineSystemInheritedPropertiesTd = MedicineSystemInheritedProperties()
#MedicineSystemPropertiesTd = MedicineSystemProperties()


class AllProperties(MedicineSystemInheritedProperties , MedicineSystemProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MedicineSystemProperties, MedicineSystemInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MedicineSystem"
    return model
    

MedicineSystem = create_schema_org_model()