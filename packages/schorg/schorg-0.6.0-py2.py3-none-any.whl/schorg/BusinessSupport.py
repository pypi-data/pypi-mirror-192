"""
BusinessSupport: this is a benefit for supporting businesses.

https://schema.org/BusinessSupport
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class BusinessSupportInheritedProperties(TypedDict):
    """BusinessSupport: this is a benefit for supporting businesses.

    References:
        https://schema.org/BusinessSupport
    Note:
        Model Depth 5
    Attributes:
    """

    


class BusinessSupportProperties(TypedDict):
    """BusinessSupport: this is a benefit for supporting businesses.

    References:
        https://schema.org/BusinessSupport
    Note:
        Model Depth 5
    Attributes:
    """

    

#BusinessSupportInheritedPropertiesTd = BusinessSupportInheritedProperties()
#BusinessSupportPropertiesTd = BusinessSupportProperties()


class AllProperties(BusinessSupportInheritedProperties , BusinessSupportProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[BusinessSupportProperties, BusinessSupportInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "BusinessSupport"
    return model
    

BusinessSupport = create_schema_org_model()