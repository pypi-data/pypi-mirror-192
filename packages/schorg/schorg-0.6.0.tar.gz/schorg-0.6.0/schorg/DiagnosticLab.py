"""
A medical laboratory that offers on-site or off-site diagnostic services.

https://schema.org/DiagnosticLab
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DiagnosticLabInheritedProperties(TypedDict):
    """A medical laboratory that offers on-site or off-site diagnostic services.

    References:
        https://schema.org/DiagnosticLab
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
    


class DiagnosticLabProperties(TypedDict):
    """A medical laboratory that offers on-site or off-site diagnostic services.

    References:
        https://schema.org/DiagnosticLab
    Note:
        Model Depth 4
    Attributes:
        availableTest: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A diagnostic test or procedure offered by this lab.
    """

    availableTest: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#DiagnosticLabInheritedPropertiesTd = DiagnosticLabInheritedProperties()
#DiagnosticLabPropertiesTd = DiagnosticLabProperties()


class AllProperties(DiagnosticLabInheritedProperties , DiagnosticLabProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DiagnosticLabProperties, DiagnosticLabInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DiagnosticLab"
    return model
    

DiagnosticLab = create_schema_org_model()