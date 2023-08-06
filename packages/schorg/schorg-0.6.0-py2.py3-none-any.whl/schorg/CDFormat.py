"""
CDFormat.

https://schema.org/CDFormat
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class CDFormatInheritedProperties(TypedDict):
    """CDFormat.

    References:
        https://schema.org/CDFormat
    Note:
        Model Depth 5
    Attributes:
    """

    


class CDFormatProperties(TypedDict):
    """CDFormat.

    References:
        https://schema.org/CDFormat
    Note:
        Model Depth 5
    Attributes:
    """

    

#CDFormatInheritedPropertiesTd = CDFormatInheritedProperties()
#CDFormatPropertiesTd = CDFormatProperties()


class AllProperties(CDFormatInheritedProperties , CDFormatProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[CDFormatProperties, CDFormatInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "CDFormat"
    return model
    

CDFormat = create_schema_org_model()