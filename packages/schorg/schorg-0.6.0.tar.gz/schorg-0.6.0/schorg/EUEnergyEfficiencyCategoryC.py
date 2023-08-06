"""
Represents EU Energy Efficiency Class C as defined in EU energy labeling regulations.

https://schema.org/EUEnergyEfficiencyCategoryC
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class EUEnergyEfficiencyCategoryCInheritedProperties(TypedDict):
    """Represents EU Energy Efficiency Class C as defined in EU energy labeling regulations.

    References:
        https://schema.org/EUEnergyEfficiencyCategoryC
    Note:
        Model Depth 6
    Attributes:
    """

    


class EUEnergyEfficiencyCategoryCProperties(TypedDict):
    """Represents EU Energy Efficiency Class C as defined in EU energy labeling regulations.

    References:
        https://schema.org/EUEnergyEfficiencyCategoryC
    Note:
        Model Depth 6
    Attributes:
    """

    

#EUEnergyEfficiencyCategoryCInheritedPropertiesTd = EUEnergyEfficiencyCategoryCInheritedProperties()
#EUEnergyEfficiencyCategoryCPropertiesTd = EUEnergyEfficiencyCategoryCProperties()


class AllProperties(EUEnergyEfficiencyCategoryCInheritedProperties , EUEnergyEfficiencyCategoryCProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[EUEnergyEfficiencyCategoryCProperties, EUEnergyEfficiencyCategoryCInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "EUEnergyEfficiencyCategoryC"
    return model
    

EUEnergyEfficiencyCategoryC = create_schema_org_model()