"""
A car wash business.

https://schema.org/AutoWash
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AutoWashInheritedProperties(TypedDict):
    """A car wash business.

    References:
        https://schema.org/AutoWash
    Note:
        Model Depth 5
    Attributes:
    """

    


class AutoWashProperties(TypedDict):
    """A car wash business.

    References:
        https://schema.org/AutoWash
    Note:
        Model Depth 5
    Attributes:
    """

    

#AutoWashInheritedPropertiesTd = AutoWashInheritedProperties()
#AutoWashPropertiesTd = AutoWashProperties()


class AllProperties(AutoWashInheritedProperties , AutoWashProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AutoWashProperties, AutoWashInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "AutoWash"
    return model
    

AutoWash = create_schema_org_model()