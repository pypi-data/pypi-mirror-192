"""
Medical researchers.

https://schema.org/MedicalResearcher
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MedicalResearcherInheritedProperties(TypedDict):
    """Medical researchers.

    References:
        https://schema.org/MedicalResearcher
    Note:
        Model Depth 6
    Attributes:
    """

    


class MedicalResearcherProperties(TypedDict):
    """Medical researchers.

    References:
        https://schema.org/MedicalResearcher
    Note:
        Model Depth 6
    Attributes:
    """

    

#MedicalResearcherInheritedPropertiesTd = MedicalResearcherInheritedProperties()
#MedicalResearcherPropertiesTd = MedicalResearcherProperties()


class AllProperties(MedicalResearcherInheritedProperties , MedicalResearcherProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MedicalResearcherProperties, MedicalResearcherInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MedicalResearcher"
    return model
    

MedicalResearcher = create_schema_org_model()