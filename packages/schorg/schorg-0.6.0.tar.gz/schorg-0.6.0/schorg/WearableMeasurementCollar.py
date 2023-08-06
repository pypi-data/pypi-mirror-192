"""
Measurement of the collar, for example of a shirt

https://schema.org/WearableMeasurementCollar
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableMeasurementCollarInheritedProperties(TypedDict):
    """Measurement of the collar, for example of a shirt

    References:
        https://schema.org/WearableMeasurementCollar
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableMeasurementCollarProperties(TypedDict):
    """Measurement of the collar, for example of a shirt

    References:
        https://schema.org/WearableMeasurementCollar
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableMeasurementCollarInheritedPropertiesTd = WearableMeasurementCollarInheritedProperties()
#WearableMeasurementCollarPropertiesTd = WearableMeasurementCollarProperties()


class AllProperties(WearableMeasurementCollarInheritedProperties , WearableMeasurementCollarProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableMeasurementCollarProperties, WearableMeasurementCollarInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableMeasurementCollar"
    return model
    

WearableMeasurementCollar = create_schema_org_model()