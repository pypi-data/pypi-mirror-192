"""
Measurement of the sleeve length, for example of a shirt

https://schema.org/WearableMeasurementSleeve
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableMeasurementSleeveInheritedProperties(TypedDict):
    """Measurement of the sleeve length, for example of a shirt

    References:
        https://schema.org/WearableMeasurementSleeve
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableMeasurementSleeveProperties(TypedDict):
    """Measurement of the sleeve length, for example of a shirt

    References:
        https://schema.org/WearableMeasurementSleeve
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableMeasurementSleeveInheritedPropertiesTd = WearableMeasurementSleeveInheritedProperties()
#WearableMeasurementSleevePropertiesTd = WearableMeasurementSleeveProperties()


class AllProperties(WearableMeasurementSleeveInheritedProperties , WearableMeasurementSleeveProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableMeasurementSleeveProperties, WearableMeasurementSleeveInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableMeasurementSleeve"
    return model
    

WearableMeasurementSleeve = create_schema_org_model()