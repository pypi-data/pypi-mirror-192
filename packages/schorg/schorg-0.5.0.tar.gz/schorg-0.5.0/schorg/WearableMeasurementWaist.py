"""
Measurement of the waist section, for example of pants

https://schema.org/WearableMeasurementWaist
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableMeasurementWaistInheritedProperties(TypedDict):
    """Measurement of the waist section, for example of pants

    References:
        https://schema.org/WearableMeasurementWaist
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableMeasurementWaistProperties(TypedDict):
    """Measurement of the waist section, for example of pants

    References:
        https://schema.org/WearableMeasurementWaist
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableMeasurementWaistInheritedPropertiesTd = WearableMeasurementWaistInheritedProperties()
#WearableMeasurementWaistPropertiesTd = WearableMeasurementWaistProperties()


class AllProperties(WearableMeasurementWaistInheritedProperties , WearableMeasurementWaistProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableMeasurementWaistProperties, WearableMeasurementWaistInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableMeasurementWaist"
    return model
    

WearableMeasurementWaist = create_schema_org_model()