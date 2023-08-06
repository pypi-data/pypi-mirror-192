"""
Overview of the content. Contains a summarized view of the topic with the most relevant information for an introduction.

https://schema.org/OverviewHealthAspect
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OverviewHealthAspectInheritedProperties(TypedDict):
    """Overview of the content. Contains a summarized view of the topic with the most relevant information for an introduction.

    References:
        https://schema.org/OverviewHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    


class OverviewHealthAspectProperties(TypedDict):
    """Overview of the content. Contains a summarized view of the topic with the most relevant information for an introduction.

    References:
        https://schema.org/OverviewHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    

#OverviewHealthAspectInheritedPropertiesTd = OverviewHealthAspectInheritedProperties()
#OverviewHealthAspectPropertiesTd = OverviewHealthAspectProperties()


class AllProperties(OverviewHealthAspectInheritedProperties , OverviewHealthAspectProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OverviewHealthAspectProperties, OverviewHealthAspectInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "OverviewHealthAspect"
    return model
    

OverviewHealthAspect = create_schema_org_model()