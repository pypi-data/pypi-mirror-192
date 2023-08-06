"""
Any medical imaging modality typically used for diagnostic purposes. Enumerated type.

https://schema.org/MedicalImagingTechnique
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MedicalImagingTechniqueInheritedProperties(TypedDict):
    """Any medical imaging modality typically used for diagnostic purposes. Enumerated type.

    References:
        https://schema.org/MedicalImagingTechnique
    Note:
        Model Depth 5
    Attributes:
    """

    


class MedicalImagingTechniqueProperties(TypedDict):
    """Any medical imaging modality typically used for diagnostic purposes. Enumerated type.

    References:
        https://schema.org/MedicalImagingTechnique
    Note:
        Model Depth 5
    Attributes:
    """

    

#MedicalImagingTechniqueInheritedPropertiesTd = MedicalImagingTechniqueInheritedProperties()
#MedicalImagingTechniquePropertiesTd = MedicalImagingTechniqueProperties()


class AllProperties(MedicalImagingTechniqueInheritedProperties , MedicalImagingTechniqueProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MedicalImagingTechniqueProperties, MedicalImagingTechniqueInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MedicalImagingTechnique"
    return model
    

MedicalImagingTechnique = create_schema_org_model()