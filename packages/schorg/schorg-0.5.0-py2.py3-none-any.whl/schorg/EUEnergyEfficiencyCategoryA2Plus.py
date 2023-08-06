"""
Represents EU Energy Efficiency Class A++ as defined in EU energy labeling regulations.

https://schema.org/EUEnergyEfficiencyCategoryA2Plus
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class EUEnergyEfficiencyCategoryA2PlusInheritedProperties(TypedDict):
    """Represents EU Energy Efficiency Class A++ as defined in EU energy labeling regulations.

    References:
        https://schema.org/EUEnergyEfficiencyCategoryA2Plus
    Note:
        Model Depth 6
    Attributes:
    """

    


class EUEnergyEfficiencyCategoryA2PlusProperties(TypedDict):
    """Represents EU Energy Efficiency Class A++ as defined in EU energy labeling regulations.

    References:
        https://schema.org/EUEnergyEfficiencyCategoryA2Plus
    Note:
        Model Depth 6
    Attributes:
    """

    

#EUEnergyEfficiencyCategoryA2PlusInheritedPropertiesTd = EUEnergyEfficiencyCategoryA2PlusInheritedProperties()
#EUEnergyEfficiencyCategoryA2PlusPropertiesTd = EUEnergyEfficiencyCategoryA2PlusProperties()


class AllProperties(EUEnergyEfficiencyCategoryA2PlusInheritedProperties , EUEnergyEfficiencyCategoryA2PlusProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[EUEnergyEfficiencyCategoryA2PlusProperties, EUEnergyEfficiencyCategoryA2PlusInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "EUEnergyEfficiencyCategoryA2Plus"
    return model
    

EUEnergyEfficiencyCategoryA2Plus = create_schema_org_model()