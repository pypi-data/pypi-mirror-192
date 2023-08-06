"""
Represents the length, for example of a dress

https://schema.org/WearableMeasurementLength
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableMeasurementLengthInheritedProperties(TypedDict):
    """Represents the length, for example of a dress

    References:
        https://schema.org/WearableMeasurementLength
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableMeasurementLengthProperties(TypedDict):
    """Represents the length, for example of a dress

    References:
        https://schema.org/WearableMeasurementLength
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableMeasurementLengthInheritedPropertiesTd = WearableMeasurementLengthInheritedProperties()
#WearableMeasurementLengthPropertiesTd = WearableMeasurementLengthProperties()


class AllProperties(WearableMeasurementLengthInheritedProperties , WearableMeasurementLengthProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableMeasurementLengthProperties, WearableMeasurementLengthInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableMeasurementLength"
    return model
    

WearableMeasurementLength = create_schema_org_model()