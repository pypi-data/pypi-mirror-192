"""
Text representing a CSS selector.

https://schema.org/CssSelectorType
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class CssSelectorTypeInheritedProperties(TypedDict):
    """Text representing a CSS selector.

    References:
        https://schema.org/CssSelectorType
    Note:
        Model Depth 6
    Attributes:
    """

    


class CssSelectorTypeProperties(TypedDict):
    """Text representing a CSS selector.

    References:
        https://schema.org/CssSelectorType
    Note:
        Model Depth 6
    Attributes:
    """

    

#CssSelectorTypeInheritedPropertiesTd = CssSelectorTypeInheritedProperties()
#CssSelectorTypePropertiesTd = CssSelectorTypeProperties()


class AllProperties(CssSelectorTypeInheritedProperties , CssSelectorTypeProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[CssSelectorTypeProperties, CssSelectorTypeInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "CssSelectorType"
    return model
    

CssSelectorType = create_schema_org_model()