"""
A branch of medicine that is involved in the dental care.

https://schema.org/Dentistry
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DentistryInheritedProperties(TypedDict):
    """A branch of medicine that is involved in the dental care.

    References:
        https://schema.org/Dentistry
    Note:
        Model Depth 6
    Attributes:
    """

    


class DentistryProperties(TypedDict):
    """A branch of medicine that is involved in the dental care.

    References:
        https://schema.org/Dentistry
    Note:
        Model Depth 6
    Attributes:
    """

    

#DentistryInheritedPropertiesTd = DentistryInheritedProperties()
#DentistryPropertiesTd = DentistryProperties()


class AllProperties(DentistryInheritedProperties , DentistryProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DentistryProperties, DentistryInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Dentistry"
    return model
    

Dentistry = create_schema_org_model()