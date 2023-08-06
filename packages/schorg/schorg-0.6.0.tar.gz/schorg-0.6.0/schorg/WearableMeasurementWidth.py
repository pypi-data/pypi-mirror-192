"""
Measurement of the width, for example of shoes

https://schema.org/WearableMeasurementWidth
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableMeasurementWidthInheritedProperties(TypedDict):
    """Measurement of the width, for example of shoes

    References:
        https://schema.org/WearableMeasurementWidth
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableMeasurementWidthProperties(TypedDict):
    """Measurement of the width, for example of shoes

    References:
        https://schema.org/WearableMeasurementWidth
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableMeasurementWidthInheritedPropertiesTd = WearableMeasurementWidthInheritedProperties()
#WearableMeasurementWidthPropertiesTd = WearableMeasurementWidthProperties()


class AllProperties(WearableMeasurementWidthInheritedProperties , WearableMeasurementWidthProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableMeasurementWidthProperties, WearableMeasurementWidthInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableMeasurementWidth"
    return model
    

WearableMeasurementWidth = create_schema_org_model()