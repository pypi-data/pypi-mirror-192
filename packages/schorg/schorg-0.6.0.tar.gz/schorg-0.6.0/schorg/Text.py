"""
Data type: Text.

https://schema.org/Text
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class TextInheritedProperties(TypedDict):
    """Data type: Text.

    References:
        https://schema.org/Text
    Note:
        Model Depth 5
    Attributes:
    """

    


class TextProperties(TypedDict):
    """Data type: Text.

    References:
        https://schema.org/Text
    Note:
        Model Depth 5
    Attributes:
    """

    

#TextInheritedPropertiesTd = TextInheritedProperties()
#TextPropertiesTd = TextProperties()


class AllProperties(TextInheritedProperties , TextProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[TextProperties, TextInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Text"
    return model
    

Text = create_schema_org_model()