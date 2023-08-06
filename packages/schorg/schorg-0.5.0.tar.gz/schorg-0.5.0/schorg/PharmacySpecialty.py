"""
The practice or art and science of preparing and dispensing drugs and medicines.

https://schema.org/PharmacySpecialty
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PharmacySpecialtyInheritedProperties(TypedDict):
    """The practice or art and science of preparing and dispensing drugs and medicines.

    References:
        https://schema.org/PharmacySpecialty
    Note:
        Model Depth 6
    Attributes:
    """

    


class PharmacySpecialtyProperties(TypedDict):
    """The practice or art and science of preparing and dispensing drugs and medicines.

    References:
        https://schema.org/PharmacySpecialty
    Note:
        Model Depth 6
    Attributes:
    """

    

#PharmacySpecialtyInheritedPropertiesTd = PharmacySpecialtyInheritedProperties()
#PharmacySpecialtyPropertiesTd = PharmacySpecialtyProperties()


class AllProperties(PharmacySpecialtyInheritedProperties , PharmacySpecialtyProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PharmacySpecialtyProperties, PharmacySpecialtyInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PharmacySpecialty"
    return model
    

PharmacySpecialty = create_schema_org_model()