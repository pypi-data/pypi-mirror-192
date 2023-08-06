"""
Represents EU Energy Efficiency Class D as defined in EU energy labeling regulations.

https://schema.org/EUEnergyEfficiencyCategoryD
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class EUEnergyEfficiencyCategoryDInheritedProperties(TypedDict):
    """Represents EU Energy Efficiency Class D as defined in EU energy labeling regulations.

    References:
        https://schema.org/EUEnergyEfficiencyCategoryD
    Note:
        Model Depth 6
    Attributes:
    """

    


class EUEnergyEfficiencyCategoryDProperties(TypedDict):
    """Represents EU Energy Efficiency Class D as defined in EU energy labeling regulations.

    References:
        https://schema.org/EUEnergyEfficiencyCategoryD
    Note:
        Model Depth 6
    Attributes:
    """

    

#EUEnergyEfficiencyCategoryDInheritedPropertiesTd = EUEnergyEfficiencyCategoryDInheritedProperties()
#EUEnergyEfficiencyCategoryDPropertiesTd = EUEnergyEfficiencyCategoryDProperties()


class AllProperties(EUEnergyEfficiencyCategoryDInheritedProperties , EUEnergyEfficiencyCategoryDProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[EUEnergyEfficiencyCategoryDProperties, EUEnergyEfficiencyCategoryDInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "EUEnergyEfficiencyCategoryD"
    return model
    

EUEnergyEfficiencyCategoryD = create_schema_org_model()