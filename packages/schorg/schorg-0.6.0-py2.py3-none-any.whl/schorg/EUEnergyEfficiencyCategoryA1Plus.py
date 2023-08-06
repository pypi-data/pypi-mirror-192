"""
Represents EU Energy Efficiency Class A+ as defined in EU energy labeling regulations.

https://schema.org/EUEnergyEfficiencyCategoryA1Plus
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class EUEnergyEfficiencyCategoryA1PlusInheritedProperties(TypedDict):
    """Represents EU Energy Efficiency Class A+ as defined in EU energy labeling regulations.

    References:
        https://schema.org/EUEnergyEfficiencyCategoryA1Plus
    Note:
        Model Depth 6
    Attributes:
    """

    


class EUEnergyEfficiencyCategoryA1PlusProperties(TypedDict):
    """Represents EU Energy Efficiency Class A+ as defined in EU energy labeling regulations.

    References:
        https://schema.org/EUEnergyEfficiencyCategoryA1Plus
    Note:
        Model Depth 6
    Attributes:
    """

    

#EUEnergyEfficiencyCategoryA1PlusInheritedPropertiesTd = EUEnergyEfficiencyCategoryA1PlusInheritedProperties()
#EUEnergyEfficiencyCategoryA1PlusPropertiesTd = EUEnergyEfficiencyCategoryA1PlusProperties()


class AllProperties(EUEnergyEfficiencyCategoryA1PlusInheritedProperties , EUEnergyEfficiencyCategoryA1PlusProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[EUEnergyEfficiencyCategoryA1PlusProperties, EUEnergyEfficiencyCategoryA1PlusInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "EUEnergyEfficiencyCategoryA1Plus"
    return model
    

EUEnergyEfficiencyCategoryA1Plus = create_schema_org_model()