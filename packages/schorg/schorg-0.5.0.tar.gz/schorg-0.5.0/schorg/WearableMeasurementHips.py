"""
Measurement of the hip section, for example of a skirt

https://schema.org/WearableMeasurementHips
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableMeasurementHipsInheritedProperties(TypedDict):
    """Measurement of the hip section, for example of a skirt

    References:
        https://schema.org/WearableMeasurementHips
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableMeasurementHipsProperties(TypedDict):
    """Measurement of the hip section, for example of a skirt

    References:
        https://schema.org/WearableMeasurementHips
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableMeasurementHipsInheritedPropertiesTd = WearableMeasurementHipsInheritedProperties()
#WearableMeasurementHipsPropertiesTd = WearableMeasurementHipsProperties()


class AllProperties(WearableMeasurementHipsInheritedProperties , WearableMeasurementHipsProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableMeasurementHipsProperties, WearableMeasurementHipsInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableMeasurementHips"
    return model
    

WearableMeasurementHips = create_schema_org_model()