"""
Measurement of the cup, for example of a bra

https://schema.org/WearableMeasurementCup
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableMeasurementCupInheritedProperties(TypedDict):
    """Measurement of the cup, for example of a bra

    References:
        https://schema.org/WearableMeasurementCup
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableMeasurementCupProperties(TypedDict):
    """Measurement of the cup, for example of a bra

    References:
        https://schema.org/WearableMeasurementCup
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableMeasurementCupInheritedPropertiesTd = WearableMeasurementCupInheritedProperties()
#WearableMeasurementCupPropertiesTd = WearableMeasurementCupProperties()


class AllProperties(WearableMeasurementCupInheritedProperties , WearableMeasurementCupProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableMeasurementCupProperties, WearableMeasurementCupInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableMeasurementCup"
    return model
    

WearableMeasurementCup = create_schema_org_model()