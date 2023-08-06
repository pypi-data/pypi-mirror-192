"""
Text representing an XPath (typically but not necessarily version 1.0).

https://schema.org/XPathType
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class XPathTypeInheritedProperties(TypedDict):
    """Text representing an XPath (typically but not necessarily version 1.0).

    References:
        https://schema.org/XPathType
    Note:
        Model Depth 6
    Attributes:
    """

    


class XPathTypeProperties(TypedDict):
    """Text representing an XPath (typically but not necessarily version 1.0).

    References:
        https://schema.org/XPathType
    Note:
        Model Depth 6
    Attributes:
    """

    

#XPathTypeInheritedPropertiesTd = XPathTypeInheritedProperties()
#XPathTypePropertiesTd = XPathTypeProperties()


class AllProperties(XPathTypeInheritedProperties , XPathTypeProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[XPathTypeProperties, XPathTypeInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "XPathType"
    return model
    

XPathType = create_schema_org_model()