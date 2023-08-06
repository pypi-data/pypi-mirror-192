"""
Boolean: True or False.

https://schema.org/Boolean
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class BooleanInheritedProperties(TypedDict):
    """Boolean: True or False.

    References:
        https://schema.org/Boolean
    Note:
        Model Depth 5
    Attributes:
    """

    


class BooleanProperties(TypedDict):
    """Boolean: True or False.

    References:
        https://schema.org/Boolean
    Note:
        Model Depth 5
    Attributes:
    """

    

#BooleanInheritedPropertiesTd = BooleanInheritedProperties()
#BooleanPropertiesTd = BooleanProperties()


class AllProperties(BooleanInheritedProperties , BooleanProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[BooleanProperties, BooleanInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Boolean"
    return model
    

Boolean = create_schema_org_model()