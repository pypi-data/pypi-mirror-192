"""
A description of costs to the patient under a given network or formulary.

https://schema.org/HealthPlanCostSharingSpecification
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class HealthPlanCostSharingSpecificationInheritedProperties(TypedDict):
    """A description of costs to the patient under a given network or formulary.

    References:
        https://schema.org/HealthPlanCostSharingSpecification
    Note:
        Model Depth 3
    Attributes:
    """

    


class HealthPlanCostSharingSpecificationProperties(TypedDict):
    """A description of costs to the patient under a given network or formulary.

    References:
        https://schema.org/HealthPlanCostSharingSpecification
    Note:
        Model Depth 3
    Attributes:
        healthPlanCoinsuranceRate: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): The rate of coinsurance expressed as a number between 0.0 and 1.0.
        healthPlanCopayOption: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Whether the copay is before or after deductible, etc. TODO: Is this a closed set?
        healthPlanPharmacyCategory: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The category or type of pharmacy associated with this cost sharing.
        healthPlanCopay: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The copay amount.
        healthPlanCoinsuranceOption: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Whether the coinsurance applies before or after deductible, etc. TODO: Is this a closed set?
    """

    healthPlanCoinsuranceRate: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    healthPlanCopayOption: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    healthPlanPharmacyCategory: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    healthPlanCopay: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    healthPlanCoinsuranceOption: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    

#HealthPlanCostSharingSpecificationInheritedPropertiesTd = HealthPlanCostSharingSpecificationInheritedProperties()
#HealthPlanCostSharingSpecificationPropertiesTd = HealthPlanCostSharingSpecificationProperties()


class AllProperties(HealthPlanCostSharingSpecificationInheritedProperties , HealthPlanCostSharingSpecificationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[HealthPlanCostSharingSpecificationProperties, HealthPlanCostSharingSpecificationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "HealthPlanCostSharingSpecification"
    return model
    

HealthPlanCostSharingSpecification = create_schema_org_model()