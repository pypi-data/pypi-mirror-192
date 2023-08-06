"""
A florist.

https://schema.org/Florist
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class FloristInheritedProperties(TypedDict):
    """A florist.

    References:
        https://schema.org/Florist
    Note:
        Model Depth 5
    Attributes:
    """

    


class FloristProperties(TypedDict):
    """A florist.

    References:
        https://schema.org/Florist
    Note:
        Model Depth 5
    Attributes:
    """

    

#FloristInheritedPropertiesTd = FloristInheritedProperties()
#FloristPropertiesTd = FloristProperties()


class AllProperties(FloristInheritedProperties , FloristProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[FloristProperties, FloristInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Florist"
    return model
    

Florist = create_schema_org_model()