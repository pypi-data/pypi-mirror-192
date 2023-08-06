"""
Enumerates energy efficiency levels (also known as "classes" or "ratings") and certifications that are part of several international energy efficiency standards.

https://schema.org/EnergyEfficiencyEnumeration
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class EnergyEfficiencyEnumerationInheritedProperties(TypedDict):
    """Enumerates energy efficiency levels (also known as "classes" or "ratings") and certifications that are part of several international energy efficiency standards.

    References:
        https://schema.org/EnergyEfficiencyEnumeration
    Note:
        Model Depth 4
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class EnergyEfficiencyEnumerationProperties(TypedDict):
    """Enumerates energy efficiency levels (also known as "classes" or "ratings") and certifications that are part of several international energy efficiency standards.

    References:
        https://schema.org/EnergyEfficiencyEnumeration
    Note:
        Model Depth 4
    Attributes:
    """

    

#EnergyEfficiencyEnumerationInheritedPropertiesTd = EnergyEfficiencyEnumerationInheritedProperties()
#EnergyEfficiencyEnumerationPropertiesTd = EnergyEfficiencyEnumerationProperties()


class AllProperties(EnergyEfficiencyEnumerationInheritedProperties , EnergyEfficiencyEnumerationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[EnergyEfficiencyEnumerationProperties, EnergyEfficiencyEnumerationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "EnergyEfficiencyEnumeration"
    return model
    

EnergyEfficiencyEnumeration = create_schema_org_model()