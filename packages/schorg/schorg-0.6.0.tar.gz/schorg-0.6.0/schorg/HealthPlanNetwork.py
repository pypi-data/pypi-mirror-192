"""
A US-style health insurance plan network. 

https://schema.org/HealthPlanNetwork
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class HealthPlanNetworkInheritedProperties(TypedDict):
    """A US-style health insurance plan network. 

    References:
        https://schema.org/HealthPlanNetwork
    Note:
        Model Depth 3
    Attributes:
    """

    


class HealthPlanNetworkProperties(TypedDict):
    """A US-style health insurance plan network. 

    References:
        https://schema.org/HealthPlanNetwork
    Note:
        Model Depth 3
    Attributes:
        healthPlanNetworkTier: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The tier(s) for this network.
        healthPlanNetworkId: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Name or unique ID of network. (Networks are often reused across different insurance plans.)
        healthPlanCostSharing: (Optional[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]): The costs to the patient for services under this network or formulary.
    """

    healthPlanNetworkTier: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    healthPlanNetworkId: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    healthPlanCostSharing: NotRequired[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]
    

#HealthPlanNetworkInheritedPropertiesTd = HealthPlanNetworkInheritedProperties()
#HealthPlanNetworkPropertiesTd = HealthPlanNetworkProperties()


class AllProperties(HealthPlanNetworkInheritedProperties , HealthPlanNetworkProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[HealthPlanNetworkProperties, HealthPlanNetworkInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "HealthPlanNetwork"
    return model
    

HealthPlanNetwork = create_schema_org_model()