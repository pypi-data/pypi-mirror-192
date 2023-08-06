"""
A legislative building&#x2014;for example, the state capitol.

https://schema.org/LegislativeBuilding
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class LegislativeBuildingInheritedProperties(TypedDict):
    """A legislative building&#x2014;for example, the state capitol.

    References:
        https://schema.org/LegislativeBuilding
    Note:
        Model Depth 5
    Attributes:
    """

    


class LegislativeBuildingProperties(TypedDict):
    """A legislative building&#x2014;for example, the state capitol.

    References:
        https://schema.org/LegislativeBuilding
    Note:
        Model Depth 5
    Attributes:
    """

    

#LegislativeBuildingInheritedPropertiesTd = LegislativeBuildingInheritedProperties()
#LegislativeBuildingPropertiesTd = LegislativeBuildingProperties()


class AllProperties(LegislativeBuildingInheritedProperties , LegislativeBuildingProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[LegislativeBuildingProperties, LegislativeBuildingInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "LegislativeBuilding"
    return model
    

LegislativeBuilding = create_schema_org_model()