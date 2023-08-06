"""
Information about how or where to find a topic. Also may contain location data that can be used for where to look for help if the topic is observed.

https://schema.org/HowOrWhereHealthAspect
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class HowOrWhereHealthAspectInheritedProperties(TypedDict):
    """Information about how or where to find a topic. Also may contain location data that can be used for where to look for help if the topic is observed.

    References:
        https://schema.org/HowOrWhereHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    


class HowOrWhereHealthAspectProperties(TypedDict):
    """Information about how or where to find a topic. Also may contain location data that can be used for where to look for help if the topic is observed.

    References:
        https://schema.org/HowOrWhereHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    

#HowOrWhereHealthAspectInheritedPropertiesTd = HowOrWhereHealthAspectInheritedProperties()
#HowOrWhereHealthAspectPropertiesTd = HowOrWhereHealthAspectProperties()


class AllProperties(HowOrWhereHealthAspectInheritedProperties , HowOrWhereHealthAspectProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[HowOrWhereHealthAspectProperties, HowOrWhereHealthAspectInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "HowOrWhereHealthAspect"
    return model
    

HowOrWhereHealthAspect = create_schema_org_model()