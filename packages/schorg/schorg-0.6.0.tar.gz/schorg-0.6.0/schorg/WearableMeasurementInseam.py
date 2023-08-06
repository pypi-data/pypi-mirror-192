"""
Measurement of the inseam, for example of pants

https://schema.org/WearableMeasurementInseam
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableMeasurementInseamInheritedProperties(TypedDict):
    """Measurement of the inseam, for example of pants

    References:
        https://schema.org/WearableMeasurementInseam
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableMeasurementInseamProperties(TypedDict):
    """Measurement of the inseam, for example of pants

    References:
        https://schema.org/WearableMeasurementInseam
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableMeasurementInseamInheritedPropertiesTd = WearableMeasurementInseamInheritedProperties()
#WearableMeasurementInseamPropertiesTd = WearableMeasurementInseamProperties()


class AllProperties(WearableMeasurementInseamInheritedProperties , WearableMeasurementInseamProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableMeasurementInseamProperties, WearableMeasurementInseamInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableMeasurementInseam"
    return model
    

WearableMeasurementInseam = create_schema_org_model()