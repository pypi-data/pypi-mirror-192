"""
Used to indicate whether a product is EnergyStar certified.

https://schema.org/EnergyStarEnergyEfficiencyEnumeration
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class EnergyStarEnergyEfficiencyEnumerationInheritedProperties(TypedDict):
    """Used to indicate whether a product is EnergyStar certified.

    References:
        https://schema.org/EnergyStarEnergyEfficiencyEnumeration
    Note:
        Model Depth 5
    Attributes:
    """

    


class EnergyStarEnergyEfficiencyEnumerationProperties(TypedDict):
    """Used to indicate whether a product is EnergyStar certified.

    References:
        https://schema.org/EnergyStarEnergyEfficiencyEnumeration
    Note:
        Model Depth 5
    Attributes:
    """

    

#EnergyStarEnergyEfficiencyEnumerationInheritedPropertiesTd = EnergyStarEnergyEfficiencyEnumerationInheritedProperties()
#EnergyStarEnergyEfficiencyEnumerationPropertiesTd = EnergyStarEnergyEfficiencyEnumerationProperties()


class AllProperties(EnergyStarEnergyEfficiencyEnumerationInheritedProperties , EnergyStarEnergyEfficiencyEnumerationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[EnergyStarEnergyEfficiencyEnumerationProperties, EnergyStarEnergyEfficiencyEnumerationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "EnergyStarEnergyEfficiencyEnumeration"
    return model
    

EnergyStarEnergyEfficiencyEnumeration = create_schema_org_model()