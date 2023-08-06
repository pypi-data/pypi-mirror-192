"""
Represents EU Energy Efficiency Class B as defined in EU energy labeling regulations.

https://schema.org/EUEnergyEfficiencyCategoryB
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class EUEnergyEfficiencyCategoryBInheritedProperties(TypedDict):
    """Represents EU Energy Efficiency Class B as defined in EU energy labeling regulations.

    References:
        https://schema.org/EUEnergyEfficiencyCategoryB
    Note:
        Model Depth 6
    Attributes:
    """

    


class EUEnergyEfficiencyCategoryBProperties(TypedDict):
    """Represents EU Energy Efficiency Class B as defined in EU energy labeling regulations.

    References:
        https://schema.org/EUEnergyEfficiencyCategoryB
    Note:
        Model Depth 6
    Attributes:
    """

    

#EUEnergyEfficiencyCategoryBInheritedPropertiesTd = EUEnergyEfficiencyCategoryBInheritedProperties()
#EUEnergyEfficiencyCategoryBPropertiesTd = EUEnergyEfficiencyCategoryBProperties()


class AllProperties(EUEnergyEfficiencyCategoryBInheritedProperties , EUEnergyEfficiencyCategoryBProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[EUEnergyEfficiencyCategoryBProperties, EUEnergyEfficiencyCategoryBInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "EUEnergyEfficiencyCategoryB"
    return model
    

EUEnergyEfficiencyCategoryB = create_schema_org_model()