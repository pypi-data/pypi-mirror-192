"""
Data type: Floating number.

https://schema.org/Float
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class FloatInheritedProperties(TypedDict):
    """Data type: Floating number.

    References:
        https://schema.org/Float
    Note:
        Model Depth 6
    Attributes:
    """

    


class FloatProperties(TypedDict):
    """Data type: Floating number.

    References:
        https://schema.org/Float
    Note:
        Model Depth 6
    Attributes:
    """

    

#FloatInheritedPropertiesTd = FloatInheritedProperties()
#FloatPropertiesTd = FloatProperties()


class AllProperties(FloatInheritedProperties , FloatProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[FloatProperties, FloatInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Float"
    return model
    

Float = create_schema_org_model()