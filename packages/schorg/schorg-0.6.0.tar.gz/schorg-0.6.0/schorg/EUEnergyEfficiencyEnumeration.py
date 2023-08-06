"""
Enumerates the EU energy efficiency classes A-G as well as A+, A++, and A+++ as defined in EU directive 2017/1369.

https://schema.org/EUEnergyEfficiencyEnumeration
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class EUEnergyEfficiencyEnumerationInheritedProperties(TypedDict):
    """Enumerates the EU energy efficiency classes A-G as well as A+, A++, and A+++ as defined in EU directive 2017/1369.

    References:
        https://schema.org/EUEnergyEfficiencyEnumeration
    Note:
        Model Depth 5
    Attributes:
    """

    


class EUEnergyEfficiencyEnumerationProperties(TypedDict):
    """Enumerates the EU energy efficiency classes A-G as well as A+, A++, and A+++ as defined in EU directive 2017/1369.

    References:
        https://schema.org/EUEnergyEfficiencyEnumeration
    Note:
        Model Depth 5
    Attributes:
    """

    

#EUEnergyEfficiencyEnumerationInheritedPropertiesTd = EUEnergyEfficiencyEnumerationInheritedProperties()
#EUEnergyEfficiencyEnumerationPropertiesTd = EUEnergyEfficiencyEnumerationProperties()


class AllProperties(EUEnergyEfficiencyEnumerationInheritedProperties , EUEnergyEfficiencyEnumerationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[EUEnergyEfficiencyEnumerationProperties, EUEnergyEfficiencyEnumerationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "EUEnergyEfficiencyEnumeration"
    return model
    

EUEnergyEfficiencyEnumeration = create_schema_org_model()