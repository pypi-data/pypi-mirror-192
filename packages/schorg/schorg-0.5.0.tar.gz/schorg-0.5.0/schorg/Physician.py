"""
A doctor's office.

https://schema.org/Physician
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PhysicianInheritedProperties(TypedDict):
    """A doctor's office.

    References:
        https://schema.org/Physician
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
    


class PhysicianProperties(TypedDict):
    """A doctor's office.

    References:
        https://schema.org/Physician
    Note:
        Model Depth 4
    Attributes:
        hospitalAffiliation: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A hospital with which the physician or office is affiliated.
        medicalSpecialty: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A medical specialty of the provider.
        availableService: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A medical service available from this provider.
    """

    hospitalAffiliation: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    medicalSpecialty: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    availableService: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#PhysicianInheritedPropertiesTd = PhysicianInheritedProperties()
#PhysicianPropertiesTd = PhysicianProperties()


class AllProperties(PhysicianInheritedProperties , PhysicianProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PhysicianProperties, PhysicianInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Physician"
    return model
    

Physician = create_schema_org_model()