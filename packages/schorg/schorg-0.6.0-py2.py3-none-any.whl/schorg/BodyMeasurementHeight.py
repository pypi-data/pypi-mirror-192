"""
Body height (measured between crown of head and soles of feet). Used, for example, to fit jackets.

https://schema.org/BodyMeasurementHeight
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class BodyMeasurementHeightInheritedProperties(TypedDict):
    """Body height (measured between crown of head and soles of feet). Used, for example, to fit jackets.

    References:
        https://schema.org/BodyMeasurementHeight
    Note:
        Model Depth 6
    Attributes:
    """

    


class BodyMeasurementHeightProperties(TypedDict):
    """Body height (measured between crown of head and soles of feet). Used, for example, to fit jackets.

    References:
        https://schema.org/BodyMeasurementHeight
    Note:
        Model Depth 6
    Attributes:
    """

    

#BodyMeasurementHeightInheritedPropertiesTd = BodyMeasurementHeightInheritedProperties()
#BodyMeasurementHeightPropertiesTd = BodyMeasurementHeightProperties()


class AllProperties(BodyMeasurementHeightInheritedProperties , BodyMeasurementHeightProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[BodyMeasurementHeightProperties, BodyMeasurementHeightInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "BodyMeasurementHeight"
    return model
    

BodyMeasurementHeight = create_schema_org_model()