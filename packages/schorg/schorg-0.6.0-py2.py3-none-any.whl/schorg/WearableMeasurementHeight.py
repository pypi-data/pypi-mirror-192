"""
Measurement of the height, for example the heel height of a shoe

https://schema.org/WearableMeasurementHeight
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableMeasurementHeightInheritedProperties(TypedDict):
    """Measurement of the height, for example the heel height of a shoe

    References:
        https://schema.org/WearableMeasurementHeight
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableMeasurementHeightProperties(TypedDict):
    """Measurement of the height, for example the heel height of a shoe

    References:
        https://schema.org/WearableMeasurementHeight
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableMeasurementHeightInheritedPropertiesTd = WearableMeasurementHeightInheritedProperties()
#WearableMeasurementHeightPropertiesTd = WearableMeasurementHeightProperties()


class AllProperties(WearableMeasurementHeightInheritedProperties , WearableMeasurementHeightProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableMeasurementHeightProperties, WearableMeasurementHeightInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableMeasurementHeight"
    return model
    

WearableMeasurementHeight = create_schema_org_model()