"""
Indicates that a document has no particular or special standing (e.g. a republication of a law by a private publisher).

https://schema.org/UnofficialLegalValue
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class UnofficialLegalValueInheritedProperties(TypedDict):
    """Indicates that a document has no particular or special standing (e.g. a republication of a law by a private publisher).

    References:
        https://schema.org/UnofficialLegalValue
    Note:
        Model Depth 5
    Attributes:
    """

    


class UnofficialLegalValueProperties(TypedDict):
    """Indicates that a document has no particular or special standing (e.g. a republication of a law by a private publisher).

    References:
        https://schema.org/UnofficialLegalValue
    Note:
        Model Depth 5
    Attributes:
    """

    

#UnofficialLegalValueInheritedPropertiesTd = UnofficialLegalValueInheritedProperties()
#UnofficialLegalValuePropertiesTd = UnofficialLegalValueProperties()


class AllProperties(UnofficialLegalValueInheritedProperties , UnofficialLegalValueProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[UnofficialLegalValueProperties, UnofficialLegalValueInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "UnofficialLegalValue"
    return model
    

UnofficialLegalValue = create_schema_org_model()