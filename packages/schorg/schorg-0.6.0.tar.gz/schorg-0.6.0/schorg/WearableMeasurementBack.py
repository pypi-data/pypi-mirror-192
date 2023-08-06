"""
Measurement of the back section, for example of a jacket

https://schema.org/WearableMeasurementBack
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableMeasurementBackInheritedProperties(TypedDict):
    """Measurement of the back section, for example of a jacket

    References:
        https://schema.org/WearableMeasurementBack
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableMeasurementBackProperties(TypedDict):
    """Measurement of the back section, for example of a jacket

    References:
        https://schema.org/WearableMeasurementBack
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableMeasurementBackInheritedPropertiesTd = WearableMeasurementBackInheritedProperties()
#WearableMeasurementBackPropertiesTd = WearableMeasurementBackProperties()


class AllProperties(WearableMeasurementBackInheritedProperties , WearableMeasurementBackProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableMeasurementBackProperties, WearableMeasurementBackInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableMeasurementBack"
    return model
    

WearableMeasurementBack = create_schema_org_model()