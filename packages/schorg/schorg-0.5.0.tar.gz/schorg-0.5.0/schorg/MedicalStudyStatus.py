"""
The status of a medical study. Enumerated type.

https://schema.org/MedicalStudyStatus
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MedicalStudyStatusInheritedProperties(TypedDict):
    """The status of a medical study. Enumerated type.

    References:
        https://schema.org/MedicalStudyStatus
    Note:
        Model Depth 5
    Attributes:
    """

    


class MedicalStudyStatusProperties(TypedDict):
    """The status of a medical study. Enumerated type.

    References:
        https://schema.org/MedicalStudyStatus
    Note:
        Model Depth 5
    Attributes:
    """

    

#MedicalStudyStatusInheritedPropertiesTd = MedicalStudyStatusInheritedProperties()
#MedicalStudyStatusPropertiesTd = MedicalStudyStatusProperties()


class AllProperties(MedicalStudyStatusInheritedProperties , MedicalStudyStatusProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MedicalStudyStatusProperties, MedicalStudyStatusInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MedicalStudyStatus"
    return model
    

MedicalStudyStatus = create_schema_org_model()