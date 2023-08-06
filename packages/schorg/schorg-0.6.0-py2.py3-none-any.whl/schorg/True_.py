"""
The boolean value true.

https://schema.org/True
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class True_InheritedProperties(TypedDict):
    """The boolean value true.

    References:
        https://schema.org/True
    Note:
        Model Depth 6
    Attributes:
    """

    


class True_Properties(TypedDict):
    """The boolean value true.

    References:
        https://schema.org/True
    Note:
        Model Depth 6
    Attributes:
    """

    

#True_InheritedPropertiesTd = True_InheritedProperties()
#True_PropertiesTd = True_Properties()


class AllProperties(True_InheritedProperties , True_Properties, TypedDict):
    pass


def create_schema_org_model(type_: Union[True_Properties, True_InheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "True_"
    return model
    

True_ = create_schema_org_model()