"""
A house painting service.

https://schema.org/HousePainter
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class HousePainterInheritedProperties(TypedDict):
    """A house painting service.

    References:
        https://schema.org/HousePainter
    Note:
        Model Depth 5
    Attributes:
    """

    


class HousePainterProperties(TypedDict):
    """A house painting service.

    References:
        https://schema.org/HousePainter
    Note:
        Model Depth 5
    Attributes:
    """

    

#HousePainterInheritedPropertiesTd = HousePainterInheritedProperties()
#HousePainterPropertiesTd = HousePainterProperties()


class AllProperties(HousePainterInheritedProperties , HousePainterProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[HousePainterProperties, HousePainterInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "HousePainter"
    return model
    

HousePainter = create_schema_org_model()