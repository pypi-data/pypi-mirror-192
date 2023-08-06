"""
A canal, like the Panama Canal.

https://schema.org/Canal
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class CanalInheritedProperties(TypedDict):
    """A canal, like the Panama Canal.

    References:
        https://schema.org/Canal
    Note:
        Model Depth 5
    Attributes:
    """

    


class CanalProperties(TypedDict):
    """A canal, like the Panama Canal.

    References:
        https://schema.org/Canal
    Note:
        Model Depth 5
    Attributes:
    """

    

#CanalInheritedPropertiesTd = CanalInheritedProperties()
#CanalPropertiesTd = CanalProperties()


class AllProperties(CanalInheritedProperties , CanalProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[CanalProperties, CanalInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Canal"
    return model
    

Canal = create_schema_org_model()