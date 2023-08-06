"""
Podiatry is the care of the human foot, especially the diagnosis and treatment of foot disorders.

https://schema.org/Podiatric
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PodiatricInheritedProperties(TypedDict):
    """Podiatry is the care of the human foot, especially the diagnosis and treatment of foot disorders.

    References:
        https://schema.org/Podiatric
    Note:
        Model Depth 5
    Attributes:
    """

    


class PodiatricProperties(TypedDict):
    """Podiatry is the care of the human foot, especially the diagnosis and treatment of foot disorders.

    References:
        https://schema.org/Podiatric
    Note:
        Model Depth 5
    Attributes:
    """

    

#PodiatricInheritedPropertiesTd = PodiatricInheritedProperties()
#PodiatricPropertiesTd = PodiatricProperties()


class AllProperties(PodiatricInheritedProperties , PodiatricProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PodiatricProperties, PodiatricInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Podiatric"
    return model
    

Podiatric = create_schema_org_model()