"""
A plumbing service.

https://schema.org/Plumber
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PlumberInheritedProperties(TypedDict):
    """A plumbing service.

    References:
        https://schema.org/Plumber
    Note:
        Model Depth 5
    Attributes:
    """

    


class PlumberProperties(TypedDict):
    """A plumbing service.

    References:
        https://schema.org/Plumber
    Note:
        Model Depth 5
    Attributes:
    """

    

#PlumberInheritedPropertiesTd = PlumberInheritedProperties()
#PlumberPropertiesTd = PlumberProperties()


class AllProperties(PlumberInheritedProperties , PlumberProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PlumberProperties, PlumberInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Plumber"
    return model
    

Plumber = create_schema_org_model()