"""
Maximum girth of bust. Used, for example, to fit women's suits.

https://schema.org/BodyMeasurementBust
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class BodyMeasurementBustInheritedProperties(TypedDict):
    """Maximum girth of bust. Used, for example, to fit women's suits.

    References:
        https://schema.org/BodyMeasurementBust
    Note:
        Model Depth 6
    Attributes:
    """

    


class BodyMeasurementBustProperties(TypedDict):
    """Maximum girth of bust. Used, for example, to fit women's suits.

    References:
        https://schema.org/BodyMeasurementBust
    Note:
        Model Depth 6
    Attributes:
    """

    

#BodyMeasurementBustInheritedPropertiesTd = BodyMeasurementBustInheritedProperties()
#BodyMeasurementBustPropertiesTd = BodyMeasurementBustProperties()


class AllProperties(BodyMeasurementBustInheritedProperties , BodyMeasurementBustProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[BodyMeasurementBustProperties, BodyMeasurementBustInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "BodyMeasurementBust"
    return model
    

BodyMeasurementBust = create_schema_org_model()