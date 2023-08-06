"""
UnemploymentSupport: this is a benefit for unemployment support.

https://schema.org/UnemploymentSupport
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class UnemploymentSupportInheritedProperties(TypedDict):
    """UnemploymentSupport: this is a benefit for unemployment support.

    References:
        https://schema.org/UnemploymentSupport
    Note:
        Model Depth 5
    Attributes:
    """

    


class UnemploymentSupportProperties(TypedDict):
    """UnemploymentSupport: this is a benefit for unemployment support.

    References:
        https://schema.org/UnemploymentSupport
    Note:
        Model Depth 5
    Attributes:
    """

    

#UnemploymentSupportInheritedPropertiesTd = UnemploymentSupportInheritedProperties()
#UnemploymentSupportPropertiesTd = UnemploymentSupportProperties()


class AllProperties(UnemploymentSupportInheritedProperties , UnemploymentSupportProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[UnemploymentSupportProperties, UnemploymentSupportInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "UnemploymentSupport"
    return model
    

UnemploymentSupport = create_schema_org_model()