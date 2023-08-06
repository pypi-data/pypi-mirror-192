"""
Measurement of the outside leg, for example of pants

https://schema.org/WearableMeasurementOutsideLeg
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableMeasurementOutsideLegInheritedProperties(TypedDict):
    """Measurement of the outside leg, for example of pants

    References:
        https://schema.org/WearableMeasurementOutsideLeg
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableMeasurementOutsideLegProperties(TypedDict):
    """Measurement of the outside leg, for example of pants

    References:
        https://schema.org/WearableMeasurementOutsideLeg
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableMeasurementOutsideLegInheritedPropertiesTd = WearableMeasurementOutsideLegInheritedProperties()
#WearableMeasurementOutsideLegPropertiesTd = WearableMeasurementOutsideLegProperties()


class AllProperties(WearableMeasurementOutsideLegInheritedProperties , WearableMeasurementOutsideLegProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableMeasurementOutsideLegProperties, WearableMeasurementOutsideLegInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableMeasurementOutsideLeg"
    return model
    

WearableMeasurementOutsideLeg = create_schema_org_model()