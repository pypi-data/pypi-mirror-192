"""
Metric size system.

https://schema.org/SizeSystemMetric
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SizeSystemMetricInheritedProperties(TypedDict):
    """Metric size system.

    References:
        https://schema.org/SizeSystemMetric
    Note:
        Model Depth 5
    Attributes:
    """

    


class SizeSystemMetricProperties(TypedDict):
    """Metric size system.

    References:
        https://schema.org/SizeSystemMetric
    Note:
        Model Depth 5
    Attributes:
    """

    

#SizeSystemMetricInheritedPropertiesTd = SizeSystemMetricInheritedProperties()
#SizeSystemMetricPropertiesTd = SizeSystemMetricProperties()


class AllProperties(SizeSystemMetricInheritedProperties , SizeSystemMetricProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SizeSystemMetricProperties, SizeSystemMetricInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "SizeSystemMetric"
    return model
    

SizeSystemMetric = create_schema_org_model()