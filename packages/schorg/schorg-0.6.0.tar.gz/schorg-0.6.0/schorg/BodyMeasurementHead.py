"""
Maximum girth of head above the ears. Used, for example, to fit hats.

https://schema.org/BodyMeasurementHead
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class BodyMeasurementHeadInheritedProperties(TypedDict):
    """Maximum girth of head above the ears. Used, for example, to fit hats.

    References:
        https://schema.org/BodyMeasurementHead
    Note:
        Model Depth 6
    Attributes:
    """

    


class BodyMeasurementHeadProperties(TypedDict):
    """Maximum girth of head above the ears. Used, for example, to fit hats.

    References:
        https://schema.org/BodyMeasurementHead
    Note:
        Model Depth 6
    Attributes:
    """

    

#BodyMeasurementHeadInheritedPropertiesTd = BodyMeasurementHeadInheritedProperties()
#BodyMeasurementHeadPropertiesTd = BodyMeasurementHeadProperties()


class AllProperties(BodyMeasurementHeadInheritedProperties , BodyMeasurementHeadProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[BodyMeasurementHeadProperties, BodyMeasurementHeadInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "BodyMeasurementHead"
    return model
    

BodyMeasurementHead = create_schema_org_model()