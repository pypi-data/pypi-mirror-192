"""
Content that discusses practical and policy aspects for getting access to specific kinds of healthcare (e.g. distribution mechanisms for vaccines).

https://schema.org/GettingAccessHealthAspect
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class GettingAccessHealthAspectInheritedProperties(TypedDict):
    """Content that discusses practical and policy aspects for getting access to specific kinds of healthcare (e.g. distribution mechanisms for vaccines).

    References:
        https://schema.org/GettingAccessHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    


class GettingAccessHealthAspectProperties(TypedDict):
    """Content that discusses practical and policy aspects for getting access to specific kinds of healthcare (e.g. distribution mechanisms for vaccines).

    References:
        https://schema.org/GettingAccessHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    

#GettingAccessHealthAspectInheritedPropertiesTd = GettingAccessHealthAspectInheritedProperties()
#GettingAccessHealthAspectPropertiesTd = GettingAccessHealthAspectProperties()


class AllProperties(GettingAccessHealthAspectInheritedProperties , GettingAccessHealthAspectProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[GettingAccessHealthAspectProperties, GettingAccessHealthAspectInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "GettingAccessHealthAspect"
    return model
    

GettingAccessHealthAspect = create_schema_org_model()