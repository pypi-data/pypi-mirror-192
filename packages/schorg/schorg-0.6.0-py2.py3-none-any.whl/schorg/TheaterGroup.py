"""
A theater group or company, for example, the Royal Shakespeare Company or Druid Theatre.

https://schema.org/TheaterGroup
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class TheaterGroupInheritedProperties(TypedDict):
    """A theater group or company, for example, the Royal Shakespeare Company or Druid Theatre.

    References:
        https://schema.org/TheaterGroup
    Note:
        Model Depth 4
    Attributes:
    """

    


class TheaterGroupProperties(TypedDict):
    """A theater group or company, for example, the Royal Shakespeare Company or Druid Theatre.

    References:
        https://schema.org/TheaterGroup
    Note:
        Model Depth 4
    Attributes:
    """

    

#TheaterGroupInheritedPropertiesTd = TheaterGroupInheritedProperties()
#TheaterGroupPropertiesTd = TheaterGroupProperties()


class AllProperties(TheaterGroupInheritedProperties , TheaterGroupProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[TheaterGroupProperties, TheaterGroupInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "TheaterGroup"
    return model
    

TheaterGroup = create_schema_org_model()