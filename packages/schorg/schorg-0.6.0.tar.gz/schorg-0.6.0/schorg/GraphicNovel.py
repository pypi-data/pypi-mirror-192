"""
Book format: GraphicNovel. May represent a bound collection of ComicIssue instances.

https://schema.org/GraphicNovel
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class GraphicNovelInheritedProperties(TypedDict):
    """Book format: GraphicNovel. May represent a bound collection of ComicIssue instances.

    References:
        https://schema.org/GraphicNovel
    Note:
        Model Depth 5
    Attributes:
    """

    


class GraphicNovelProperties(TypedDict):
    """Book format: GraphicNovel. May represent a bound collection of ComicIssue instances.

    References:
        https://schema.org/GraphicNovel
    Note:
        Model Depth 5
    Attributes:
    """

    

#GraphicNovelInheritedPropertiesTd = GraphicNovelInheritedProperties()
#GraphicNovelPropertiesTd = GraphicNovelProperties()


class AllProperties(GraphicNovelInheritedProperties , GraphicNovelProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[GraphicNovelProperties, GraphicNovelInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "GraphicNovel"
    return model
    

GraphicNovel = create_schema_org_model()