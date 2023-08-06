"""
Represents EnergyStar certification.

https://schema.org/EnergyStarCertified
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class EnergyStarCertifiedInheritedProperties(TypedDict):
    """Represents EnergyStar certification.

    References:
        https://schema.org/EnergyStarCertified
    Note:
        Model Depth 6
    Attributes:
    """

    


class EnergyStarCertifiedProperties(TypedDict):
    """Represents EnergyStar certification.

    References:
        https://schema.org/EnergyStarCertified
    Note:
        Model Depth 6
    Attributes:
    """

    

#EnergyStarCertifiedInheritedPropertiesTd = EnergyStarCertifiedInheritedProperties()
#EnergyStarCertifiedPropertiesTd = EnergyStarCertifiedProperties()


class AllProperties(EnergyStarCertifiedInheritedProperties , EnergyStarCertifiedProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[EnergyStarCertifiedProperties, EnergyStarCertifiedInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "EnergyStarCertified"
    return model
    

EnergyStarCertified = create_schema_org_model()