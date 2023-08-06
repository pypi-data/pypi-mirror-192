"""
An enumeration that describes different types of medical procedures.

https://schema.org/MedicalProcedureType
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MedicalProcedureTypeInheritedProperties(TypedDict):
    """An enumeration that describes different types of medical procedures.

    References:
        https://schema.org/MedicalProcedureType
    Note:
        Model Depth 5
    Attributes:
    """

    


class MedicalProcedureTypeProperties(TypedDict):
    """An enumeration that describes different types of medical procedures.

    References:
        https://schema.org/MedicalProcedureType
    Note:
        Model Depth 5
    Attributes:
    """

    

#MedicalProcedureTypeInheritedPropertiesTd = MedicalProcedureTypeInheritedProperties()
#MedicalProcedureTypePropertiesTd = MedicalProcedureTypeProperties()


class AllProperties(MedicalProcedureTypeInheritedProperties , MedicalProcedureTypeProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MedicalProcedureTypeProperties, MedicalProcedureTypeInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MedicalProcedureType"
    return model
    

MedicalProcedureType = create_schema_org_model()