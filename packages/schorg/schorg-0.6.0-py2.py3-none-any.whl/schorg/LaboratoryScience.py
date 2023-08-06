"""
A medical science pertaining to chemical, hematological, immunologic, microscopic, or bacteriological diagnostic analyses or research.

https://schema.org/LaboratoryScience
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class LaboratoryScienceInheritedProperties(TypedDict):
    """A medical science pertaining to chemical, hematological, immunologic, microscopic, or bacteriological diagnostic analyses or research.

    References:
        https://schema.org/LaboratoryScience
    Note:
        Model Depth 6
    Attributes:
    """

    


class LaboratoryScienceProperties(TypedDict):
    """A medical science pertaining to chemical, hematological, immunologic, microscopic, or bacteriological diagnostic analyses or research.

    References:
        https://schema.org/LaboratoryScience
    Note:
        Model Depth 6
    Attributes:
    """

    

#LaboratoryScienceInheritedPropertiesTd = LaboratoryScienceInheritedProperties()
#LaboratorySciencePropertiesTd = LaboratoryScienceProperties()


class AllProperties(LaboratoryScienceInheritedProperties , LaboratoryScienceProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[LaboratoryScienceProperties, LaboratoryScienceInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "LaboratoryScience"
    return model
    

LaboratoryScience = create_schema_org_model()