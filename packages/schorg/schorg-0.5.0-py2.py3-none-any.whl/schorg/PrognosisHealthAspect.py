"""
Typical progression and happenings of life course of the topic.

https://schema.org/PrognosisHealthAspect
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PrognosisHealthAspectInheritedProperties(TypedDict):
    """Typical progression and happenings of life course of the topic.

    References:
        https://schema.org/PrognosisHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    


class PrognosisHealthAspectProperties(TypedDict):
    """Typical progression and happenings of life course of the topic.

    References:
        https://schema.org/PrognosisHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    

#PrognosisHealthAspectInheritedPropertiesTd = PrognosisHealthAspectInheritedProperties()
#PrognosisHealthAspectPropertiesTd = PrognosisHealthAspectProperties()


class AllProperties(PrognosisHealthAspectInheritedProperties , PrognosisHealthAspectProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PrognosisHealthAspectProperties, PrognosisHealthAspectInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PrognosisHealthAspect"
    return model
    

PrognosisHealthAspect = create_schema_org_model()