"""
A day spa.

https://schema.org/DaySpa
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DaySpaInheritedProperties(TypedDict):
    """A day spa.

    References:
        https://schema.org/DaySpa
    Note:
        Model Depth 5
    Attributes:
    """

    


class DaySpaProperties(TypedDict):
    """A day spa.

    References:
        https://schema.org/DaySpa
    Note:
        Model Depth 5
    Attributes:
    """

    

#DaySpaInheritedPropertiesTd = DaySpaInheritedProperties()
#DaySpaPropertiesTd = DaySpaProperties()


class AllProperties(DaySpaInheritedProperties , DaySpaProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DaySpaProperties, DaySpaInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DaySpa"
    return model
    

DaySpa = create_schema_org_model()