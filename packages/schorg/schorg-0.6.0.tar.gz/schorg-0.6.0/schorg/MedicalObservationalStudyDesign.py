"""
Design models for observational medical studies. Enumerated type.

https://schema.org/MedicalObservationalStudyDesign
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MedicalObservationalStudyDesignInheritedProperties(TypedDict):
    """Design models for observational medical studies. Enumerated type.

    References:
        https://schema.org/MedicalObservationalStudyDesign
    Note:
        Model Depth 5
    Attributes:
    """

    


class MedicalObservationalStudyDesignProperties(TypedDict):
    """Design models for observational medical studies. Enumerated type.

    References:
        https://schema.org/MedicalObservationalStudyDesign
    Note:
        Model Depth 5
    Attributes:
    """

    

#MedicalObservationalStudyDesignInheritedPropertiesTd = MedicalObservationalStudyDesignInheritedProperties()
#MedicalObservationalStudyDesignPropertiesTd = MedicalObservationalStudyDesignProperties()


class AllProperties(MedicalObservationalStudyDesignInheritedProperties , MedicalObservationalStudyDesignProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MedicalObservationalStudyDesignProperties, MedicalObservationalStudyDesignInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MedicalObservationalStudyDesign"
    return model
    

MedicalObservationalStudyDesign = create_schema_org_model()