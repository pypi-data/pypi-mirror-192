"""
Represents EU Energy Efficiency Class A as defined in EU energy labeling regulations.

https://schema.org/EUEnergyEfficiencyCategoryA
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class EUEnergyEfficiencyCategoryAInheritedProperties(TypedDict):
    """Represents EU Energy Efficiency Class A as defined in EU energy labeling regulations.

    References:
        https://schema.org/EUEnergyEfficiencyCategoryA
    Note:
        Model Depth 6
    Attributes:
    """

    


class EUEnergyEfficiencyCategoryAProperties(TypedDict):
    """Represents EU Energy Efficiency Class A as defined in EU energy labeling regulations.

    References:
        https://schema.org/EUEnergyEfficiencyCategoryA
    Note:
        Model Depth 6
    Attributes:
    """

    

#EUEnergyEfficiencyCategoryAInheritedPropertiesTd = EUEnergyEfficiencyCategoryAInheritedProperties()
#EUEnergyEfficiencyCategoryAPropertiesTd = EUEnergyEfficiencyCategoryAProperties()


class AllProperties(EUEnergyEfficiencyCategoryAInheritedProperties , EUEnergyEfficiencyCategoryAProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[EUEnergyEfficiencyCategoryAProperties, EUEnergyEfficiencyCategoryAInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "EUEnergyEfficiencyCategoryA"
    return model
    

EUEnergyEfficiencyCategoryA = create_schema_org_model()