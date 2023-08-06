"""
Body weight. Used, for example, to measure pantyhose.

https://schema.org/BodyMeasurementWeight
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class BodyMeasurementWeightInheritedProperties(TypedDict):
    """Body weight. Used, for example, to measure pantyhose.

    References:
        https://schema.org/BodyMeasurementWeight
    Note:
        Model Depth 6
    Attributes:
    """

    


class BodyMeasurementWeightProperties(TypedDict):
    """Body weight. Used, for example, to measure pantyhose.

    References:
        https://schema.org/BodyMeasurementWeight
    Note:
        Model Depth 6
    Attributes:
    """

    

#BodyMeasurementWeightInheritedPropertiesTd = BodyMeasurementWeightInheritedProperties()
#BodyMeasurementWeightPropertiesTd = BodyMeasurementWeightProperties()


class AllProperties(BodyMeasurementWeightInheritedProperties , BodyMeasurementWeightProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[BodyMeasurementWeightProperties, BodyMeasurementWeightInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "BodyMeasurementWeight"
    return model
    

BodyMeasurementWeight = create_schema_org_model()