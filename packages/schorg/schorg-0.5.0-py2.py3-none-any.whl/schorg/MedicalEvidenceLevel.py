"""
Level of evidence for a medical guideline. Enumerated type.

https://schema.org/MedicalEvidenceLevel
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MedicalEvidenceLevelInheritedProperties(TypedDict):
    """Level of evidence for a medical guideline. Enumerated type.

    References:
        https://schema.org/MedicalEvidenceLevel
    Note:
        Model Depth 5
    Attributes:
    """

    


class MedicalEvidenceLevelProperties(TypedDict):
    """Level of evidence for a medical guideline. Enumerated type.

    References:
        https://schema.org/MedicalEvidenceLevel
    Note:
        Model Depth 5
    Attributes:
    """

    

#MedicalEvidenceLevelInheritedPropertiesTd = MedicalEvidenceLevelInheritedProperties()
#MedicalEvidenceLevelPropertiesTd = MedicalEvidenceLevelProperties()


class AllProperties(MedicalEvidenceLevelInheritedProperties , MedicalEvidenceLevelProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MedicalEvidenceLevelProperties, MedicalEvidenceLevelInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MedicalEvidenceLevel"
    return model
    

MedicalEvidenceLevel = create_schema_org_model()