"""
Data type: URL.

https://schema.org/URL
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class URLInheritedProperties(TypedDict):
    """Data type: URL.

    References:
        https://schema.org/URL
    Note:
        Model Depth 6
    Attributes:
    """

    


class URLProperties(TypedDict):
    """Data type: URL.

    References:
        https://schema.org/URL
    Note:
        Model Depth 6
    Attributes:
    """

    

#URLInheritedPropertiesTd = URLInheritedProperties()
#URLPropertiesTd = URLProperties()


class AllProperties(URLInheritedProperties , URLProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[URLProperties, URLInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "URL"
    return model
    

URL = create_schema_org_model()