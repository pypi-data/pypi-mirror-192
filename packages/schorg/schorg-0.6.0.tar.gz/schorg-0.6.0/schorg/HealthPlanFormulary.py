"""
For a given health insurance plan, the specification for costs and coverage of prescription drugs. 

https://schema.org/HealthPlanFormulary
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class HealthPlanFormularyInheritedProperties(TypedDict):
    """For a given health insurance plan, the specification for costs and coverage of prescription drugs. 

    References:
        https://schema.org/HealthPlanFormulary
    Note:
        Model Depth 3
    Attributes:
    """

    


class HealthPlanFormularyProperties(TypedDict):
    """For a given health insurance plan, the specification for costs and coverage of prescription drugs. 

    References:
        https://schema.org/HealthPlanFormulary
    Note:
        Model Depth 3
    Attributes:
        healthPlanCostSharing: (Optional[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]): The costs to the patient for services under this network or formulary.
        offersPrescriptionByMail: (Optional[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]): Whether prescriptions can be delivered by mail.
        healthPlanDrugTier: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The tier(s) of drugs offered by this formulary or insurance plan.
    """

    healthPlanCostSharing: NotRequired[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]
    offersPrescriptionByMail: NotRequired[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]
    healthPlanDrugTier: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    

#HealthPlanFormularyInheritedPropertiesTd = HealthPlanFormularyInheritedProperties()
#HealthPlanFormularyPropertiesTd = HealthPlanFormularyProperties()


class AllProperties(HealthPlanFormularyInheritedProperties , HealthPlanFormularyProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[HealthPlanFormularyProperties, HealthPlanFormularyInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "HealthPlanFormulary"
    return model
    

HealthPlanFormulary = create_schema_org_model()