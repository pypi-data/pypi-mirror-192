"""
Content about common misconceptions and myths that are related to a topic.

https://schema.org/MisconceptionsHealthAspect
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MisconceptionsHealthAspectInheritedProperties(TypedDict):
    """Content about common misconceptions and myths that are related to a topic.

    References:
        https://schema.org/MisconceptionsHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    


class MisconceptionsHealthAspectProperties(TypedDict):
    """Content about common misconceptions and myths that are related to a topic.

    References:
        https://schema.org/MisconceptionsHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    

#MisconceptionsHealthAspectInheritedPropertiesTd = MisconceptionsHealthAspectInheritedProperties()
#MisconceptionsHealthAspectPropertiesTd = MisconceptionsHealthAspectProperties()


class AllProperties(MisconceptionsHealthAspectInheritedProperties , MisconceptionsHealthAspectProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MisconceptionsHealthAspectProperties, MisconceptionsHealthAspectInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MisconceptionsHealthAspect"
    return model
    

MisconceptionsHealthAspect = create_schema_org_model()