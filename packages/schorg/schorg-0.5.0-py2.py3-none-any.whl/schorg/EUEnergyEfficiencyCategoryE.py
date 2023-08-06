"""
Represents EU Energy Efficiency Class E as defined in EU energy labeling regulations.

https://schema.org/EUEnergyEfficiencyCategoryE
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class EUEnergyEfficiencyCategoryEInheritedProperties(TypedDict):
    """Represents EU Energy Efficiency Class E as defined in EU energy labeling regulations.

    References:
        https://schema.org/EUEnergyEfficiencyCategoryE
    Note:
        Model Depth 6
    Attributes:
    """

    


class EUEnergyEfficiencyCategoryEProperties(TypedDict):
    """Represents EU Energy Efficiency Class E as defined in EU energy labeling regulations.

    References:
        https://schema.org/EUEnergyEfficiencyCategoryE
    Note:
        Model Depth 6
    Attributes:
    """

    

#EUEnergyEfficiencyCategoryEInheritedPropertiesTd = EUEnergyEfficiencyCategoryEInheritedProperties()
#EUEnergyEfficiencyCategoryEPropertiesTd = EUEnergyEfficiencyCategoryEProperties()


class AllProperties(EUEnergyEfficiencyCategoryEInheritedProperties , EUEnergyEfficiencyCategoryEProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[EUEnergyEfficiencyCategoryEProperties, EUEnergyEfficiencyCategoryEInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "EUEnergyEfficiencyCategoryE"
    return model
    

EUEnergyEfficiencyCategoryE = create_schema_org_model()