"""
Represents EU Energy Efficiency Class F as defined in EU energy labeling regulations.

https://schema.org/EUEnergyEfficiencyCategoryF
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class EUEnergyEfficiencyCategoryFInheritedProperties(TypedDict):
    """Represents EU Energy Efficiency Class F as defined in EU energy labeling regulations.

    References:
        https://schema.org/EUEnergyEfficiencyCategoryF
    Note:
        Model Depth 6
    Attributes:
    """

    


class EUEnergyEfficiencyCategoryFProperties(TypedDict):
    """Represents EU Energy Efficiency Class F as defined in EU energy labeling regulations.

    References:
        https://schema.org/EUEnergyEfficiencyCategoryF
    Note:
        Model Depth 6
    Attributes:
    """

    

#EUEnergyEfficiencyCategoryFInheritedPropertiesTd = EUEnergyEfficiencyCategoryFInheritedProperties()
#EUEnergyEfficiencyCategoryFPropertiesTd = EUEnergyEfficiencyCategoryFProperties()


class AllProperties(EUEnergyEfficiencyCategoryFInheritedProperties , EUEnergyEfficiencyCategoryFProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[EUEnergyEfficiencyCategoryFProperties, EUEnergyEfficiencyCategoryFInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "EUEnergyEfficiencyCategoryF"
    return model
    

EUEnergyEfficiencyCategoryF = create_schema_org_model()