"""
Nonprofit501c28: Non-profit type referring to National Railroad Retirement Investment Trusts.

https://schema.org/Nonprofit501c28
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class Nonprofit501c28InheritedProperties(TypedDict):
    """Nonprofit501c28: Non-profit type referring to National Railroad Retirement Investment Trusts.

    References:
        https://schema.org/Nonprofit501c28
    Note:
        Model Depth 6
    Attributes:
    """

    


class Nonprofit501c28Properties(TypedDict):
    """Nonprofit501c28: Non-profit type referring to National Railroad Retirement Investment Trusts.

    References:
        https://schema.org/Nonprofit501c28
    Note:
        Model Depth 6
    Attributes:
    """

    

#Nonprofit501c28InheritedPropertiesTd = Nonprofit501c28InheritedProperties()
#Nonprofit501c28PropertiesTd = Nonprofit501c28Properties()


class AllProperties(Nonprofit501c28InheritedProperties , Nonprofit501c28Properties, TypedDict):
    pass


def create_schema_org_model(type_: Union[Nonprofit501c28Properties, Nonprofit501c28InheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Nonprofit501c28"
    return model
    

Nonprofit501c28 = create_schema_org_model()