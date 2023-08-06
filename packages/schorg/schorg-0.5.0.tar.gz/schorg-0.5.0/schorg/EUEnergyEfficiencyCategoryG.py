"""
Represents EU Energy Efficiency Class G as defined in EU energy labeling regulations.

https://schema.org/EUEnergyEfficiencyCategoryG
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class EUEnergyEfficiencyCategoryGInheritedProperties(TypedDict):
    """Represents EU Energy Efficiency Class G as defined in EU energy labeling regulations.

    References:
        https://schema.org/EUEnergyEfficiencyCategoryG
    Note:
        Model Depth 6
    Attributes:
    """

    


class EUEnergyEfficiencyCategoryGProperties(TypedDict):
    """Represents EU Energy Efficiency Class G as defined in EU energy labeling regulations.

    References:
        https://schema.org/EUEnergyEfficiencyCategoryG
    Note:
        Model Depth 6
    Attributes:
    """

    

#EUEnergyEfficiencyCategoryGInheritedPropertiesTd = EUEnergyEfficiencyCategoryGInheritedProperties()
#EUEnergyEfficiencyCategoryGPropertiesTd = EUEnergyEfficiencyCategoryGProperties()


class AllProperties(EUEnergyEfficiencyCategoryGInheritedProperties , EUEnergyEfficiencyCategoryGProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[EUEnergyEfficiencyCategoryGProperties, EUEnergyEfficiencyCategoryGInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "EUEnergyEfficiencyCategoryG"
    return model
    

EUEnergyEfficiencyCategoryG = create_schema_org_model()