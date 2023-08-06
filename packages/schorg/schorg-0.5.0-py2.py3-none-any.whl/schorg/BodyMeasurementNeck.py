"""
Girth of neck. Used, for example, to fit shirts.

https://schema.org/BodyMeasurementNeck
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class BodyMeasurementNeckInheritedProperties(TypedDict):
    """Girth of neck. Used, for example, to fit shirts.

    References:
        https://schema.org/BodyMeasurementNeck
    Note:
        Model Depth 6
    Attributes:
    """

    


class BodyMeasurementNeckProperties(TypedDict):
    """Girth of neck. Used, for example, to fit shirts.

    References:
        https://schema.org/BodyMeasurementNeck
    Note:
        Model Depth 6
    Attributes:
    """

    

#BodyMeasurementNeckInheritedPropertiesTd = BodyMeasurementNeckInheritedProperties()
#BodyMeasurementNeckPropertiesTd = BodyMeasurementNeckProperties()


class AllProperties(BodyMeasurementNeckInheritedProperties , BodyMeasurementNeckProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[BodyMeasurementNeckProperties, BodyMeasurementNeckInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "BodyMeasurementNeck"
    return model
    

BodyMeasurementNeck = create_schema_org_model()