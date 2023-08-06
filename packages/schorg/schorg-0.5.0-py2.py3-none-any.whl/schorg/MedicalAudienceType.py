"""
Target audiences types for medical web pages. Enumerated type.

https://schema.org/MedicalAudienceType
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MedicalAudienceTypeInheritedProperties(TypedDict):
    """Target audiences types for medical web pages. Enumerated type.

    References:
        https://schema.org/MedicalAudienceType
    Note:
        Model Depth 5
    Attributes:
    """

    


class MedicalAudienceTypeProperties(TypedDict):
    """Target audiences types for medical web pages. Enumerated type.

    References:
        https://schema.org/MedicalAudienceType
    Note:
        Model Depth 5
    Attributes:
    """

    

#MedicalAudienceTypeInheritedPropertiesTd = MedicalAudienceTypeInheritedProperties()
#MedicalAudienceTypePropertiesTd = MedicalAudienceTypeProperties()


class AllProperties(MedicalAudienceTypeInheritedProperties , MedicalAudienceTypeProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MedicalAudienceTypeProperties, MedicalAudienceTypeInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MedicalAudienceType"
    return model
    

MedicalAudienceType = create_schema_org_model()