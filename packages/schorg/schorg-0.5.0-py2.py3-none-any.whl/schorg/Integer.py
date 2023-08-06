"""
Data type: Integer.

https://schema.org/Integer
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class IntegerInheritedProperties(TypedDict):
    """Data type: Integer.

    References:
        https://schema.org/Integer
    Note:
        Model Depth 6
    Attributes:
    """

    


class IntegerProperties(TypedDict):
    """Data type: Integer.

    References:
        https://schema.org/Integer
    Note:
        Model Depth 6
    Attributes:
    """

    

#IntegerInheritedPropertiesTd = IntegerInheritedProperties()
#IntegerPropertiesTd = IntegerProperties()


class AllProperties(IntegerInheritedProperties , IntegerProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[IntegerProperties, IntegerInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Integer"
    return model
    

Integer = create_schema_org_model()