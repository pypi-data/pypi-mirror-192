"""
A Research project.

https://schema.org/ResearchProject
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ResearchProjectInheritedProperties(TypedDict):
    """A Research project.

    References:
        https://schema.org/ResearchProject
    Note:
        Model Depth 4
    Attributes:
    """

    


class ResearchProjectProperties(TypedDict):
    """A Research project.

    References:
        https://schema.org/ResearchProject
    Note:
        Model Depth 4
    Attributes:
    """

    

#ResearchProjectInheritedPropertiesTd = ResearchProjectInheritedProperties()
#ResearchProjectPropertiesTd = ResearchProjectProperties()


class AllProperties(ResearchProjectInheritedProperties , ResearchProjectProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ResearchProjectProperties, ResearchProjectInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ResearchProject"
    return model
    

ResearchProject = create_schema_org_model()