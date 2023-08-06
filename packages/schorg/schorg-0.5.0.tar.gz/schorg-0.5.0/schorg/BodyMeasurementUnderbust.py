"""
Girth of body just below the bust. Used, for example, to fit women's swimwear.

https://schema.org/BodyMeasurementUnderbust
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class BodyMeasurementUnderbustInheritedProperties(TypedDict):
    """Girth of body just below the bust. Used, for example, to fit women's swimwear.

    References:
        https://schema.org/BodyMeasurementUnderbust
    Note:
        Model Depth 6
    Attributes:
    """

    


class BodyMeasurementUnderbustProperties(TypedDict):
    """Girth of body just below the bust. Used, for example, to fit women's swimwear.

    References:
        https://schema.org/BodyMeasurementUnderbust
    Note:
        Model Depth 6
    Attributes:
    """

    

#BodyMeasurementUnderbustInheritedPropertiesTd = BodyMeasurementUnderbustInheritedProperties()
#BodyMeasurementUnderbustPropertiesTd = BodyMeasurementUnderbustProperties()


class AllProperties(BodyMeasurementUnderbustInheritedProperties , BodyMeasurementUnderbustProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[BodyMeasurementUnderbustProperties, BodyMeasurementUnderbustInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "BodyMeasurementUnderbust"
    return model
    

BodyMeasurementUnderbust = create_schema_org_model()