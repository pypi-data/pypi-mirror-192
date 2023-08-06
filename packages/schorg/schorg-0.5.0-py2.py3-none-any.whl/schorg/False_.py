"""
The boolean value false.

https://schema.org/False
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class False_InheritedProperties(TypedDict):
    """The boolean value false.

    References:
        https://schema.org/False
    Note:
        Model Depth 6
    Attributes:
    """

    


class False_Properties(TypedDict):
    """The boolean value false.

    References:
        https://schema.org/False
    Note:
        Model Depth 6
    Attributes:
    """

    

#False_InheritedPropertiesTd = False_InheritedProperties()
#False_PropertiesTd = False_Properties()


class AllProperties(False_InheritedProperties , False_Properties, TypedDict):
    pass


def create_schema_org_model(type_: Union[False_Properties, False_InheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "False_"
    return model
    

False_ = create_schema_org_model()