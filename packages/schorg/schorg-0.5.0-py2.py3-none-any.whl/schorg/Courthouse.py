"""
A courthouse.

https://schema.org/Courthouse
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class CourthouseInheritedProperties(TypedDict):
    """A courthouse.

    References:
        https://schema.org/Courthouse
    Note:
        Model Depth 5
    Attributes:
    """

    


class CourthouseProperties(TypedDict):
    """A courthouse.

    References:
        https://schema.org/Courthouse
    Note:
        Model Depth 5
    Attributes:
    """

    

#CourthouseInheritedPropertiesTd = CourthouseInheritedProperties()
#CourthousePropertiesTd = CourthouseProperties()


class AllProperties(CourthouseInheritedProperties , CourthouseProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[CourthouseProperties, CourthouseInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Courthouse"
    return model
    

Courthouse = create_schema_org_model()