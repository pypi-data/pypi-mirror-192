"""
Design models for medical trials. Enumerated type.

https://schema.org/MedicalTrialDesign
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MedicalTrialDesignInheritedProperties(TypedDict):
    """Design models for medical trials. Enumerated type.

    References:
        https://schema.org/MedicalTrialDesign
    Note:
        Model Depth 5
    Attributes:
    """

    


class MedicalTrialDesignProperties(TypedDict):
    """Design models for medical trials. Enumerated type.

    References:
        https://schema.org/MedicalTrialDesign
    Note:
        Model Depth 5
    Attributes:
    """

    

#MedicalTrialDesignInheritedPropertiesTd = MedicalTrialDesignInheritedProperties()
#MedicalTrialDesignPropertiesTd = MedicalTrialDesignProperties()


class AllProperties(MedicalTrialDesignInheritedProperties , MedicalTrialDesignProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MedicalTrialDesignProperties, MedicalTrialDesignInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MedicalTrialDesign"
    return model
    

MedicalTrialDesign = create_schema_org_model()