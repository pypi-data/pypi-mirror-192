"""
A pharmacy or drugstore.

https://schema.org/Pharmacy
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PharmacyInheritedProperties(TypedDict):
    """A pharmacy or drugstore.

    References:
        https://schema.org/Pharmacy
    Note:
        Model Depth 4
    Attributes:
        healthPlanNetworkId: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Name or unique ID of network. (Networks are often reused across different insurance plans.)
        medicalSpecialty: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A medical specialty of the provider.
        isAcceptingNewPatients: (Optional[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]): Whether the provider is accepting new patients.
    """

    healthPlanNetworkId: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    medicalSpecialty: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    isAcceptingNewPatients: NotRequired[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]
    


class PharmacyProperties(TypedDict):
    """A pharmacy or drugstore.

    References:
        https://schema.org/Pharmacy
    Note:
        Model Depth 4
    Attributes:
    """

    

#PharmacyInheritedPropertiesTd = PharmacyInheritedProperties()
#PharmacyPropertiesTd = PharmacyProperties()


class AllProperties(PharmacyInheritedProperties , PharmacyProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PharmacyProperties, PharmacyInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Pharmacy"
    return model
    

Pharmacy = create_schema_org_model()